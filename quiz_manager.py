import json
import re
from ai_service import ask_ai


def generate_quiz(topic, level, num_questions=5):

    prompt = f"""
    Generate {num_questions} multiple-choice questions.

    Topic: {topic}
    Level: {level}

    Return ONLY valid JSON in this format:

    [
      {{
        "question": "What is Python?",
        "options": [
          "Programming Language",
          "Database",
          "Browser",
          "Operating System"
        ],
        "answer": "Programming Language"
      }}
    ]

    Do not include markdown or extra text.
    """

    response = ask_ai(prompt)

    try:
        response = re.sub(r"```(?:json)?|```", "", response).strip()
        questions = json.loads(response)

        if not isinstance(questions, list) or not questions:
            return []

        for q in questions:
            if not all(k in q for k in ["question", "options", "answer"]):
                return []

            if q["answer"] not in q["options"]:
                return []

        return questions

    except (json.JSONDecodeError, TypeError):
        return []


def evaluate_quiz(questions, user_answers):

    score = 0
    results = []

    for i, question in enumerate(questions):

        correct_answer = question["answer"]
        user_answer = user_answers.get(i, "")

        is_correct = user_answer == correct_answer

        if is_correct:
            score += 1

        results.append({
            "question": question["question"],
            "your_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        })

    return score, len(questions), results