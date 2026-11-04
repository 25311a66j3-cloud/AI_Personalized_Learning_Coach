from ai_service import ask_ai


def generate_study_plan(name, subject, level, daily_hours, goal):

    prompt = f"""
    You are an AI Personalized Learning Coach.

    Student Name: {name}
    Subject: {subject}
    Current Level: {level}
    Daily Study Hours: {daily_hours}
    Learning Goal: {goal}

    Create a personalized 7-day study plan.

    Include:
    1. Daily topics
    2. Study activities
    3. Practice exercises
    4. Revision schedule
    5. Improvement suggestions

    Use simple English.
    Make the plan beginner-friendly.
    """

    result = ask_ai(prompt)

    return result