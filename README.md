## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method not allowed
- 422: Not Processable 
- 500: Server error

### Endpoints 
#### GET /questions
- General:
    - Returns a list of a list of questions, a category object containing the question categories, the current category,the success value and the total number of questions.
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions`

``` {
  "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
  },
  "current_category": null,
  "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
        },
            {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        }
  ],
  "success": true,
  "total_questions": 24
}
```
#### POST /questions
- General:
    - Creates a new question using the submitted question, answer, difficulty and category. Returns the success value, id of the created question, current questions, total number of questions and categories to update the frontend. 
- `curl http://127.0.0.1:5000/questions?page=3 -X POST -H "Content-Type: application/json" --request POST --data '{"question":"Leanardo da Vinci is best known for which of his work?", "answer":"Mona Lisa", "difficulty":"5", "category":"2"}'`
```
{
    "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "deleted": 39,
  "questions": [
    {
      "answer": "Astatine",
      "category": 5,
      "difficulty": 1,
      "id": 37,
      "question": "What is the rarest chemical element on earth?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 5,
      "id": 38,
      "question": "Leanardo da Vinci is best known for which of his work? "
    }
  ],
  "success": true,
  "total_questions": 22
}
```

#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the success value,  id of the deleted question, available questions,and total number of available questions to update the frontend. 
- `curl -X DELETE http://127.0.0.1:5000/questions/39?page=3`
```
{
  "deleted": 38,
  "questions": [
    {
      "answer": "Astatine",
      "category": 5,
      "difficulty": 1,
      "id": 37,
      "question": "What is the rarest chemical element on earth?"
    }
  ],
  "success": true,
  "total_questions": 21
}
```

#### GET /categories/{category_id}/questions
-   General:
    - Returns the success value, current category of the question, the total number of questions in the category and a list of question objects.
```
{
  "Success": true,
  "current_category": "Entertainment",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "total_questions": 2
}
```

