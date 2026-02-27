print("DEBUG: File is executing")
def run_quiz():

    print("# Exercise 1:")
    print("# Let d(g(f(x(s)))) represent the following code:\n")

    print("def decorator(f):")
    print("    def wrapper(x):")
    print("        return 'Hello ' + f(x)")  # Must use f('str') to concatenate.
    print("    return wrapper")
    print("")
    print("@decorator")
    print("def g(x):")  # 'world' binds to x.  
    print("    return x")
    print("")
    print("print(g('world!'))")

    print("\n--- Answer The Questions ---\n")

    score = 0

    # Q1
    q1 = input("Q1: Which letter represents 'wrapper'? ")
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
    if q3.strip().lower() == "x":
        print("Correct!")
        score += 1
    else:
        print("Incorrect. The correct answer is: x")

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

    print(f"\nFinal Score: {score}/4")

    return score

if __name__ == "__main__":
        run_quiz()