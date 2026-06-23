import random

# ─────────────────────────────────────────────
#  HELPER: display the main menu
# ─────────────────────────────────────────────
def show_menu():
    print("\n" + "=" * 40)
    print("       PYTHON DAY-1 TOOLKIT")
    print("=" * 40)
    print("  1. Calculator")
    print("  2. Number Guessing Game")
    print("  3. Text Analyzer")
    print("  0. Exit")
    print("=" * 40)


# ─────────────────────────────────────────────
#  FEATURE 1 — Calculator
#  Concepts: input(), type conversion, operators,
#             conditionals, while, break
# ─────────────────────────────────────────────
def calculator():
    print("\n── Calculator (type 'q' to quit) ──")

    while True:
        try:
            raw = input("\nEnter expression (e.g. 10 + 3): ").strip()
            if raw.lower() == "q":
                break

            # Split into three parts: number operator number
            parts = raw.split()
            if len(parts) != 3:
                print("Format: <number> <operator> <number>")
                continue

            a, op, b = parts
            a, b = float(a), float(b)   # type conversion

            if op == "+":
                result = a + b
            elif op == "-":
                result = a - b
            elif op == "*":
                result = a * b
            elif op == "/":
                if b == 0:
                    print("Error: division by zero")
                    continue
                result = a / b
            elif op == "//":
                result = a // b
            elif op == "%":
                result = a % b
            elif op == "**":
                result = a ** b
            else:
                print(f"Unknown operator: {op}")
                continue

            # f-string to display result cleanly
            print(f"  {a} {op} {b} = {result}")

        except ValueError:
            print("Please enter valid numbers.")


# ─────────────────────────────────────────────
#  FEATURE 2 — Number Guessing Game
#  Concepts: random, while, break, continue,
#             comparison operators, f-strings
# ─────────────────────────────────────────────
def guessing_game():
    print("\n── Number Guessing Game ──")

    lower, upper = 1, 100
    secret = random.randint(lower, upper)
    attempts = 0
    max_attempts = 7

    print(f"Guess the number between {lower} and {upper}.")
    print(f"You have {max_attempts} attempts.\n")

    while attempts < max_attempts:
        attempts += 1
        remaining = max_attempts - attempts + 1

        try:
            guess = int(input(f"Attempt {attempts}/{max_attempts} → "))
        except ValueError:
            print("Please enter a whole number.")
            attempts -= 1   # don't penalise bad input
            continue

        if guess < lower or guess > upper:
            print(f"Out of range! Stay between {lower} and {upper}.")
            attempts -= 1
            continue

        if guess == secret:
            print(f"\n🎉 Correct! You got it in {attempts} attempt(s).")
            break
        elif guess < secret:
            print("Too low ↑")
        else:
            print("Too high ↓")

        if remaining > 1:
            print(f"  ({remaining - 1} attempt(s) left)")
    else:
        # while…else runs when the loop finishes without break
        print(f"\nOut of attempts. The number was {secret}.")


# ─────────────────────────────────────────────
#  FEATURE 3 — Text Analyzer
#  Concepts: strings (slicing, methods), loops,
#             conditionals, operators
# ─────────────────────────────────────────────
VOWELS = set("aeiouAEIOU")

def is_palindrome(text):
    """Return True if text reads the same forwards and backwards."""
    cleaned = "".join(ch.lower() for ch in text if ch.isalpha())
    return cleaned == cleaned[::-1]   # slicing trick: reverse string

def analyze_text(text):
    words      = text.split()
    word_count = len(words)
    char_count = len(text)
    vowel_count = sum(1 for ch in text if ch in VOWELS)

    # Word frequency (manual — no Counter, keeping it to Day-1 concepts)
    freq = {}
    for word in words:
        word = word.strip(".,!?;:\"'").lower()
        freq[word] = freq.get(word, 0) + 1

    # Sort by frequency
    sorted_freq = sorted(freq.items(), key=lambda pair: pair[1], reverse=True)

    print(f"\n  Characters : {char_count}")
    print(f"  Words      : {word_count}")
    print(f"  Vowels     : {vowel_count}")
    print(f"  Palindrome : {'Yes' if is_palindrome(text) else 'No'}")

    print("\n  Top 5 words:")
    for word, count in sorted_freq[:5]:
        bar = "█" * count
        print(f"    {word:<15} {bar}  ({count})")

def text_analyzer():
    print("\n── Text Analyzer (type 'q' to quit) ──")

    while True:
        text = input("\nEnter text: ").strip()
        if text.lower() == "q":
            break
        if not text:
            print("Please enter some text.")
            continue
        analyze_text(text)


# ─────────────────────────────────────────────
#  MAIN — menu loop
# ─────────────────────────────────────────────
def main():
    print("\nWelcome to the Python Day-1 Toolkit!")

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            calculator()
        elif choice == "2":
            guessing_game()
        elif choice == "3":
            text_analyzer()
        elif choice == "0":
            print("\nGoodbye! Commit your work. 🚀")
            break
        else:
            print("Invalid choice — enter 0, 1, 2, or 3.")


if __name__ == "__main__":
    main()
