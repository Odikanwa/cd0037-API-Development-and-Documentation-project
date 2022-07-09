import os
import json
from urllib import response
from flask import Flask, request, abort, jsonify, url_for, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. 
    Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization, true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, PUT, POST, PATCH, DELETE, OPTIONS"
        )
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def get_categories():
        try:
            selection = Category.query.order_by(Category.type).all()
            if selection == None:
                abort(404)
            categories = {category.id: category.type for category in selection}

            return jsonify(
                {
                    "success": True,
                    "categories": categories
                }
            )
        except:
            abort(500)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.type).all()
        current_questions = paginate_questions(request, questions)

        if len(current_questions) == 0:
            abort(404)

        return(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(questions),
                "categories": {category.id: category.type for category in categories},
                "current_category": None
            }
        )
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            available_questions = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, available_questions)

            # TODO: correct errors when the only question on a page is deleted

            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "questions": current_questions,
                    "total_questions": len(available_questions),
                }
            )
        except:
            abort(422)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def create_question():
        try:
            body = request.get_json()
            new_question = body.get("question", None)
            new_answer = body.get("answer", None)
            new_difficulty = body.get("difficulty", None)
            new_category = body.get("category", None)
            # search = body.get("search", None)

            if (new_question == None) or (new_answer == None) or (
                new_difficulty == None) or (new_category == None):
                    abort(405)

            question = Question(question=new_question, answer=new_answer,
                                category=new_category, difficulty=new_difficulty)
            question.insert()

            questions = Question.query.order_by(Question.id).all()
            categories = Category.query.order_by(Category.type).all()
            current_questions = paginate_questions(request, questions)
            category_obj = {
                category.id: category.type for category in categories}

            return jsonify(
                {
                    "success": True,
                    "created": question.id,
                    "questions": current_questions,
                    "total_questions": len(questions),
                    "categories": category_obj
                    # "total_questions": len(Question.query.all()),
                }
            )

        except:
            abort(400)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/search", methods=["POST"])
    def search_question():
        try:
            body = request.get_json()
            search = body.get("searchTerm", None)
            allowed_search_chars = set("abcdefghijklmnopqrstuvwxyz! .")

            if search and allowed_search_chars.issuperset(search):
                questions = Question.query.filter(
                    Question.question.ilike("%{}%".format(search))
                ).all()
            else:
                abort(400)

            current_questions = [question.format() for question in questions]

            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(questions)
                }
            )
        except:
            abort(400)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_categories(category_id):
        try:
            questions = Question.query.filter(
                    Question.category == category_id).all()
            question_list = [question.format() for question in questions]
            current_questions = question_list[0:]

            question = question_list[0]
            question_category = question['category'] #saved as ID of the category

            categories = Category.query.filter(Category.id == question_category).all()
            category = categories[0]
            current_category = category.type

            if questions == None:
                abort(404)

            return jsonify(
                {
                    "Success": True,
                    "questions": current_questions,
                    "total_questions": len(questions),
                    "current_category": current_category
                }
            )
        except:
            abort(500)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        try:
            body = request.get_json()
            previous_questions = body.get("previous_questions", None)
            quiz_category = body.get("quiz_category", None)
            # print(quiz_category['id'])

            if (previous_questions == None) and (quiz_category == None):
                abort(422)
            
            category = Category.query.all()

            if quiz_category:
                # Filter by ID not in previous questions and by categories
                available_questions  = Question.query.filter(Question.id.notin_((previous_questions))).filter(
                    Question.category == quiz_category['id']).all()
                
                # If All category is selected
                if quiz_category['id'] == 0:
                    available_questions = Question.query.filter(Question.id.notin_((previous_questions))).all()
                
                question_list = [question.format() for question in available_questions]
                questions = question_list[0:]  
            
                if len(questions) > 0:
                    random_questions = random.choice(questions)
                else:
                    random_questions = None

            return jsonify(
                {
                    "success": True,
                    "question": random_questions
                        
                }
            )
        except:
            abort(500)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "Bad request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404,
                    "message": "resource not found"}),
            404,
        )

    @app.errorhandler(405)
    def not_allowed(error):
        return (
            jsonify({"success": False, "error": 405,
                    "message": "method not allowed"}),
            405,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422,
                    "message": "Request could not be processed"}),
            422,
        )

    @app.errorhandler(500)
    def not_allowed(error):
        return (
            jsonify({"success": False, "error": 500, "message": "Server error"}),
            500,
        )

    return app
