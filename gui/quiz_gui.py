from dearpygui.dearpygui import *
import json, random, os

JSON_PATH = "utils/study_cards_v2.json"

# Load questions
if not os.path.exists(JSON_PATH):
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump([], f)

with open(JSON_PATH, "r", encoding="utf-8") as f:
    questions = json.load(f)

random.shuffle(questions)

# Quiz state
state = {"card_index": 0, "qa_index": 0, "score": 0}

# -------------------- Quiz Functions --------------------
def start_quiz(sender=None, app_data=None, user_data=None):
    if does_item_exist("quiz_window"):
        delete_item("quiz_window")

    state.update({"card_index":0, "qa_index":0, "score":0})
    random.shuffle(questions)

    with window(label="Quiz", tag="quiz_window", width=900, height=600):
        # Code block
        add_text("", tag="quiz_code")
        bind_item_font("quiz_code", code_font)
        add_spacing(count=1)

        # Question
        add_text("", tag="quiz_question", color=[255,255,255])
        add_spacing(count=2)

        # Answer input
        add_input_text(tag="quiz_answer", multiline=True, height=120,
                       on_enter=True, callback=submit_answer)
        add_spacing(count=1)

        # Buttons
        add_button(label="Submit", callback=submit_answer)
        add_same_line()
        add_button(label="Next", callback=next_question)
        add_spacing(count=1)

        # Feedback
        add_text("", tag="quiz_feedback", color=[255,255,0])

    update_question()

def submit_answer(sender=None, app_data=None, user_data=None):
    if state["card_index"] >= len(questions):
        return
    card = questions[state["card_index"]]
    qa_list = card.get("qa", [])
    if state["qa_index"] >= len(qa_list):
        return

    correct = qa_list[state["qa_index"]].get("answer","")
    user = get_value("quiz_answer").strip()

    if not correct:
        set_value("quiz_feedback","[No answer defined]")
        configure_item("quiz_feedback", color=[255,255,0])
    elif user.lower() == correct.lower():
        state["score"] += 1
        set_value("quiz_feedback","[Correct]")
        configure_item("quiz_feedback", color=[0,255,0])
    else:
        set_value("quiz_feedback",f"[Wrong] Correct: {correct}")
        configure_item("quiz_feedback", color=[255,0,0])

def next_question(sender=None, app_data=None, user_data=None):
    state["qa_index"] += 1
    update_question()

def update_question():
    if state["card_index"] >= len(questions):
        total = sum(len(c.get("qa",[])) for c in questions)
        set_value("quiz_question", f"Quiz finished! Score: {state['score']} / {total}")
        set_value("quiz_code","")
        set_value("quiz_feedback","")
        if does_item_exist("quiz_answer"):
            delete_item("quiz_answer")
        return

    card = questions[state["card_index"]]
    qa_list = card.get("qa",[])
    if not qa_list or state["qa_index"] >= len(qa_list):
        state["card_index"] += 1
        state["qa_index"] = 0
        update_question()
        return

    question = qa_list[state["qa_index"]].get("question","No question")
    set_value("quiz_code", card.get("code",""))
    set_value("quiz_question", question)
    set_value("quiz_answer","")
    set_value("quiz_feedback","")
    focus_item("quiz_answer")

# -------------------- CRUD Functions --------------------
def save_json():
    with open(JSON_PATH,"w",encoding="utf-8") as f:
        json.dump(questions,f,indent=2)

# Add Card
def add_card(sender=None, app_data=None, user_data=None):
    if does_item_exist("add_card_window"):
        delete_item("add_card_window")
    with window(label="Add Card", tag="add_card_window", width=600, height=500):
        add_text("Enter code snippet:", color=[255,255,255])
        add_input_text(tag="new_code", multiline=True, height=120)
        bind_item_font("new_code", code_font)
        add_spacing(count=1)

        add_text("Enter question:", color=[255,255,255])
        add_input_text(tag="new_question", multiline=True, height=150)
        add_spacing(count=1)

        add_text("Enter answer:", color=[255,255,255])
        add_input_text(tag="new_answer", multiline=True, height=120)
        add_spacing(count=1)

        add_button(label="Save Card", callback=save_new_card)

def save_new_card(sender, app_data, user_data):
    new_card = {
        "code": get_value("new_code"),
        "qa": [{"question": get_value("new_question"), "answer": get_value("new_answer")}]
    }
    questions.append(new_card)
    save_json()
    delete_item("add_card_window")

# Edit Card
def edit_card(sender=None, app_data=None, user_data=None):
    if does_item_exist("edit_card_window"):
        delete_item("edit_card_window")
    with window(label="Edit Card", tag="edit_card_window", width=600, height=550):
        add_combo([f"{i}: {c.get('code','Card')}" for i,c in enumerate(questions)],
                  tag="edit_select", label="Select Card")
        add_button(label="Load Card", callback=load_edit_card)
        add_spacing(count=1)

        add_text("Edit question:", color=[255,255,255])
        add_input_text(tag="edit_question", multiline=True, height=150)
        add_spacing(count=1)

        add_text("Edit answer:", color=[255,255,255])
        add_input_text(tag="edit_answer", multiline=True, height=120)
        add_spacing(count=1)

        add_button(label="Save Changes", callback=save_edit_card)

def load_edit_card(sender, app_data, user_data):
    idx = int(get_value("edit_select").split(":")[0])
    card = questions[idx]
    qa = card.get("qa",[{}])[0]
    set_value("edit_question", qa.get("question",""))
    set_value("edit_answer", qa.get("answer",""))

def save_edit_card(sender, app_data, user_data):
    idx = int(get_value("edit_select").split(":")[0])
    card = questions[idx]
    card["qa"][0]["question"] = get_value("edit_question")
    card["qa"][0]["answer"] = get_value("edit_answer")
    save_json()
    delete_item("edit_card_window")

# Delete Card
def delete_card(sender=None, app_data=None, user_data=None):
    if does_item_exist("delete_card_window"):
        delete_item("delete_card_window")
    with window(label="Delete Card", tag="delete_card_window", width=400, height=200):
        add_text("Select a card to delete:", color=[255,255,255])
        add_combo([f"{i}: {c.get('code','Card')}" for i,c in enumerate(questions)],
                  tag="delete_select", label="Select Card")
        add_spacing(count=1)
        add_button(label="Delete", callback=confirm_delete)

def confirm_delete(sender, app_data, user_data):
    idx = int(get_value("delete_select").split(":")[0])
    questions.pop(idx)
    save_json()
    delete_item("delete_card_window")

# -------------------- Main Window --------------------
def build_frame():
    if does_item_exist("main_window"):
        delete_item("main_window")
    with window(label="Learning Tools", tag="main_window", width=500, height=400):
        add_text("Welcome to Teledex", color=[255,255,255])
        add_spacing(count=2)
        add_button(label="Start Quiz", width=200, height=50, callback=start_quiz)
        add_spacing(count=1)
        add_button(label="Add Card", width=200, height=50, callback=add_card)
        add_spacing(count=1)
        add_button(label="Edit Card", width=200, height=50, callback=edit_card)
        add_spacing(count=1)
        add_button(label="Delete Card", width=200, height=50, callback=delete_card)
        add_spacing(count=2)
        add_text("Use the buttons above to manage cards and start learning!", wrap=400, color=[200,200,200])

def exit_app(sender, app_data, user_data):
    stop_dearpygui()  # stops the event loop immediately

# -------------------- GUI Startup --------------------

create_context()

with font_registry():
    default_font = add_font("C:/Windows/Fonts/segoeui.ttf", 18)
    code_font = add_font("C:/Windows/Fonts/consola.ttf", 16)

bind_font(default_font)
build_frame()

create_viewport(title="Teledex", width=900, height=700)
setup_dearpygui()
show_viewport()

start_dearpygui()
destroy_context()



# -------------------- Module Test aka debugger Block --------------------
if __name__ == "__main__":
    from dearpygui.dearpygui import *

    # Create context and viewport
    create_context()
    create_viewport(title="Module Test", width=800, height=600)
    setup_dearpygui()

    # Call your module's build_frame function
    build_frame()  

    # Show GUI
    show_viewport()
    start_dearpygui()
    destroy_context()