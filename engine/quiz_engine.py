import json
from dearpygui.dearpygui import *

# -------------------------------
# State tracking
# -------------------------------
state = {"index": 0, "score": 0}

# -------------------------------
# Load questions from JSON
# -------------------------------
with open("utils/study_cards_v2.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

# -------------------------------
# Function to check answers
# -------------------------------
def check_answer(index, user_answer):
    correct = questions[index]["answer"].strip().lower()
    return user_answer.strip().lower() == correct

# -------------------------------
# DearPyGui quiz functions
# -------------------------------
def start_quiz():
    with window("Python Quiz", width=500, height=500):
        add_text("", tag="quiz_question")
        add_input_text(tag="quiz_answer")
        add_button(label="Submit", callback=check)
        update_question()

def update_question():
    if state["index"] < len(questions):
        q = questions[state["index"]]
        set_value("quiz_question", q["question"])
        set_value("quiz_answer", "")
    else:
        set_value("quiz_question", f"Quiz finished! Score: {state['score']}/{len(questions)}")
        delete_item("quiz_answer")
        delete_item("Submit")

def check(sender, app_data, user_data):
    ans = get_value("quiz_answer").strip().lower()
    if check_answer(state["index"], ans):
        state["score"] += 1
        print("Correct")
    else:
        correct = questions[state["index"]]["answer"]
        print(f"Wrong, correct answer: {correct}")
    state["index"] += 1
    update_question()