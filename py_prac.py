# Documents > Coding_Prac > py_prac.py 
# Han's personal self-study quizzes/review on Python coding. 

# ================================
# Part 1 — Quiz Interface
# ================================

def run_quiz():

    print("# Exercise 1:")
    print("# Let d(g(f(b))) represent the following code:\n")

    print("def decorator(f):")  # Outer function.
    print("    def wrapper(b):")  # Inner function.
    print("        a = 'Hello'")  # combine a + result of g below.  
    print("        return a + f(b)")  # Must use f('str') to concatenate.
    print("    return wrapper")
    print("")
    print("@decorator")
    print("def g(b):")  # 'world' binds to b.  
    print("    return b")  # g now returns b explicitly.
    print("")
    print("print(g('world!'))")

    print("\n--- Answer The Questions ---\n")

    score = 0

    # Q1
    q1 = input("Q1: Which letter references 'wrapper'? ")
    if q1.strip().lower() == "g":
        print("Correct!")
        score += 1
    else:
        print("Incorrect. The correct answer is: g")

    print()

    # Q2
    q2 = input("Q2: What is the print output? ")
    if q2.strip().lower() == "hello world!":
        print("Correct!")
        score += 1
    else:
        print("Incorrect. The correct answer is: Hello world!")

    print()

    # Q3
    q3 = input("Q3: Which letter represents 'world!'? ")
    if q3.strip().lower() == "b":
        print("Correct!")
        score += 1
    else:
        print("Incorrect. The correct answer is: b")

    print()

    # Q4 Multiple Choice
    print("Q4: Which word best describes what @ does?")
    print("a) apply")
    print("b) paste")
    print("c) try")
    print("d) assign")

    q4 = input("Enter a, b, c, or d: ")

    if q4.strip().lower() == "a":
        print("Correct! '@' applies the decorator to the function.")
        score += 1
    else:
        print("Incorrect. The correct answer is: a) apply")

    print()

    # Q5 Multiple Choice
    print("Q5: After decoration, what does g reference?")

    print("a) original function")
    print("b) wrapper")
    print("c) decorator")
    print("d) string")

    q5 = input("Enter a, b, c, or d: ")

    if q5.strip().lower() == "b":
        print("Correct! g now references the wrapper function.")
        score += 1
    else:
        print("Incorrect. The correct answer is: b) wrapper")

    print(f"\nFinal Score: {score}/5")

    return score


# ================================
# Part 2 — Teacher Notes (UNCHANGED)
# ================================
#  d          decorator, the outermost function
#  g	      wrapper: inner function of d, 'Hello' + f(x)
#  f          Function of x. 
#  x          x='world!' str assigned to param x in wrapper, the arg  passed to g when g('world!') is called.     
#  s          s is the str value, 'world!', assigned to parameter x of wrapper. 
#  print:     Hello world!


# ================================
# Part 3 — Program Entry Point
# ================================

if __name__ == "__main__":
    run_quiz()