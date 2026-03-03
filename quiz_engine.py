# 3/1/26 – archived py_pracy.py bc gui-cli conflict. Py has ast import for data-oriented code.  
# PYTHON QUIZ 1 for Teledex app

questions = [

    {
        "question": "Which letter represents 'wrapper'?",
        "code": """def decorator(f):
    def wrapper(b):
        a = 'Hello'
        return a + f(b)
    return wrapper

@decorator
def g(b):
    return b

print(g('world!'))""",
        "answer": "g"
    },

    {
        "question": "What is the print output?",
        "code": """def decorator(f):
    def wrapper(b):
        a = 'Hello'
        return a + f(b)
    return wrapper

@decorator
def g(b):
    return b

print(g('world!'))""",
        "answer": "hello world!"
    },

    {
        "question": "Which letter represents 'world!'?",
        "code": """def decorator(f):
    def wrapper(b):
        a = 'Hello'
        return a + f(b)
    return wrapper

@decorator
def g(b):
    return b""",
        "answer": "b"
    },

    {
        "question": "Which word best describes what @ does?",
        "code": """a) apply
b) paste
c) try
d) assign""",
        "answer": "a"
    }

]


def check_answer(index, user_input):
    return user_input.strip().lower() == questions[index]["answer"]