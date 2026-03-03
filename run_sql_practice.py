from sql_practice_engine import SQLPracticeEngine


def main():
    engine = SQLPracticeEngine()

    print("\n=== SQL Practice Mode ===")
    print("Type your SQL query and press Enter.")
    print("Type 'exit' anytime to quit.\n")

    while not engine.is_finished():

        question = engine.get_current_question()
        print(question)

        print("\nEnter SQL query:")
        user_input = input(">>> ")

        if user_input.lower() == "exit":
            break

        correct, message = engine.check_answer(user_input)

        print("\n" + message)
        print("-" * 40)

    score, total = engine.get_score()
    print(f"\nFinal Score: {score}/{total}")
    print("Practice complete.\n")


if __name__ == "__main__":
    main()