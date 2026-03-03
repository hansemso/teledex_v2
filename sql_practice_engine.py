import sqlite3
from sql_practice_db import create_connection, setup_database


class SQLPracticeEngine:

    def __init__(self):
        self.conn = create_connection()
        setup_database(self.conn)
        self.questions = self._load_questions()
        self.index = 0
        self.score = 0

    def _load_questions(self):
        return [
            {
                "question": "1) Select all customers.",
                "answer_query": "SELECT * FROM customers"
            },
            {
                "question": "2) Select all customers from New York.",
                "answer_query": "SELECT * FROM customers WHERE city = 'New York'"
            },
            {
                "question": "3) Select all orders above 100.",
                "answer_query": "SELECT * FROM orders WHERE amount > 100"
            },
            {
                "question": """4) Show customer name and order amount
using a JOIN between customers and orders.""",
                "answer_query": """
                    SELECT customers.name, orders.amount
                    FROM customers
                    JOIN orders ON customers.id = orders.customer_id
                """
            },
            {
                "question": """5) Show total order amount per customer.
(Hint: GROUP BY)""",
                "answer_query": """
                    SELECT customers.name, SUM(orders.amount)
                    FROM customers
                    JOIN orders ON customers.id = orders.customer_id
                    GROUP BY customers.name
                """
            }
        ]

    def get_current_question(self):
        if self.index < len(self.questions):
            return self.questions[self.index]["question"]
        return None

    def execute_query(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result

    def check_answer(self, user_query):
        if self.index >= len(self.questions):
            return False, "Quiz finished."

        try:
            correct_query = self.questions[self.index]["answer_query"]

            correct_result = self.execute_query(correct_query)
            user_result = self.execute_query(user_query)

            # Normalize order (important for comparison)
            correct_sorted = sorted(correct_result)
            user_sorted = sorted(user_result)

            if correct_sorted == user_sorted:
                self.score += 1
                self.index += 1
                return True, "Correct!"
            else:
                self.index += 1
                return False, f"Incorrect.\nExpected: {correct_sorted}\nGot: {user_sorted}"

        except sqlite3.Error as e:
            return False, f"SQL Error: {e}"

    def is_finished(self):
        return self.index >= len(self.questions)

    def get_score(self):
        return self.score, len(self.questions)
    