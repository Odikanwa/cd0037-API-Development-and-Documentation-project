import os
import random
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('student', 'student', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {"question": "Have you mastered python?", "answer": "Not yet", "category": 1, "difficulty": 1}
        self.incomplete_question = {"question": "Have you mastered python?", "answer": None, "category": 1, "difficulty": 1}
        self.total_questions = 0
        self.quiz_category = {'type': 'Geography', 'id': '3'}

        self.previous_questions = [13, 14]

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_200_get_categories_success(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data["categories"]), 6)
    
    def test_404_get_categories_fail(self):
        res = self.client().get("/categories/7")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


    def test_200_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    def test_404_sent_request_beyond_valid_page(self):
        res = self.client().get("/questions?page=100", json={"category": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_200_create_new_question_success(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])
        # self.assertTrue(len(data["questions"]))

    def test_400_if_form_inputs_are_incomplete(self):
        res = self.client().post("/questions", json=self.incomplete_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request")

    def test_200_delete_question_success(self):
        res = self.client().delete("/questions/17")
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 17).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 17)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertEqual(question, None)

    def test_422_if_question_does_not_exist(self):
        res = self.client().delete("/questions/100")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Request could not be processed")
    
    def test_200_question_search_success(self):
        res = self.client().post("/search", json={"searchTerm": "title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertEqual(data["total_questions"], 2)

    def test_400_search_is_invalid(self):
        res = self.client().post("/search", json={"search": "<>"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Bad request")
    
    def test_200_get_questions_by_categories_success(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["Success"], True)
        self.assertTrue(data["questions"], 5)
        self.assertTrue(data["total_questions"])

    def test_500_get_questions_by_categories_fail(self):
        res = self.client().get("/categories/45/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Server error")

    def test_200_play_quiz_success(self):
        res = self.client().post("/quizzes")
        data = json.loads(res.data)

        quiz_category = data.get("quiz_category", None)

        if quiz_category:
        
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data["success"], True)
            self.assertEqual(data["question"])

    def test_500_play_quiz_fail(self):
        res = self.client().post("/quizzes")
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Server error")



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()