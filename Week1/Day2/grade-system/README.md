# Student Grade Manager

A simple Python program that accepts a student's mark and converts it into a grade based on a predefined grading scale.

## Grading Scale

| Mark Range | Grade |
|------------|-------|
| 90 - 100   | A     |
| 80 - 89    | B     |
| 70 - 79    | C     |
| 60 - 69    | D     |
| Below 60   | E     |

## Concepts Used

- `input()` – Gets the mark from the user.
- `float()` – Converts the input into a number.
- **Variables** – Stores values such as `mark` and `grade`.
- `while` loop – Repeats the program when invalid input is entered.
- `if / elif / else` – Determines the appropriate grade.
- **Comparison operators** – Checks conditions such as `mark >= 90`.
- `or` – Combines multiple conditions.
- `try / except` – Handles invalid user input safely.
- `ValueError` – Handles input that cannot be converted into a number.
- `continue` – Restarts the loop after invalid input.
- `break` – Stops the loop after valid input.
- `print()` – Displays the result.
- **f-string** – Displays variables inside formatted text.

## Program Flow

1. Ask the user to enter a mark.
2. Convert the input to a number.
3. Check whether the mark is between 0 and 100.
4. If the input is invalid, display an error message and ask again.
5. Determine the grade using the grading scale.
6. Display the mark and grade.
7. End the program.

## Example

```text
Enter a mark (0-100): 85
Mark: 85.0
Grade: B