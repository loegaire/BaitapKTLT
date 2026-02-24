from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd

ANSWER_KEY = np.array(
    "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D".split(","),
    dtype=str,
)
STUDENT_ID_RE = re.compile(r"^N\d{8}$")


def prompt_for_class_file(data_dir: Path) -> tuple[Path, list[str]]:
    """Prompt until a readable class file is provided.

    The user may type `class1` or `class1.txt`. The file is searched relative to
    `data_dir` (where this script lives).
    """

    while True:
        user_value = input(
            "Enter a class to grade (e.g. class1, class10, 10, or class1.txt): "
        ).strip()

        if not user_value:
            continue

        # Flexible inputs:
        # - "class10" -> class10.txt (in data_dir)
        # - "10" -> class10.txt (in data_dir)
        # - "foo.txt" -> foo.txt (in data_dir)
        # - "./somewhere/foo.txt" or "/abs/foo.txt" -> use as-is
        if "/" in user_value or "\\" in user_value:
            candidate = Path(user_value)
            file_path = candidate if candidate.is_absolute() else (data_dir / candidate)
        else:
            if user_value.lower().endswith(".txt"):
                filename = user_value
            elif user_value.isdigit():
                filename = f"class{user_value}.txt"
            else:
                filename = f"{user_value}.txt"
            file_path = data_dir / filename

        try:
            lines = file_path.read_text(encoding="utf-8").splitlines()
        except FileNotFoundError:
            print("File cannot be found.")
            continue
        except OSError:
            print("File cannot be found.")
            continue

        print(f"Successfully opened {file_path.name}")
        print()
        return file_path, lines


def is_valid_student_id(student_id: str) -> bool:
    return bool(STUDENT_ID_RE.match(student_id))


def analyze_lines(lines: list[str]) -> tuple[list[tuple[str, list[str]]], int]:
    """Validate each line and return (valid_records, invalid_count)."""

    valid_records: list[tuple[str, list[str]]] = []
    invalid_count = 0

    print("**** ANALYZING ****")
    print()

    for raw_line in lines:
        line = raw_line.strip()

        values = line.split(",")
        if len(values) != 26:
            print("Invalid line of data: does not contain exactly 26 values:")
            print(line)
            print()
            invalid_count += 1
            continue

        student_id = values[0]
        if not is_valid_student_id(student_id):
            print("Invalid line of data: N# is invalid")
            print(line)
            print()
            invalid_count += 1
            continue

        answers = values[1:]
        valid_records.append((student_id, answers))

    if invalid_count == 0:
        print("No errors found!")
        print()

    print("**** REPORT ****")
    print()
    print(f"Total valid lines of data: {len(valid_records)}")
    print(f"Total invalid lines of data: {invalid_count}")
    print()

    return valid_records, invalid_count


def score_answers(answers: list[str]) -> int:
    """Score one student's answers using the project rubric."""

    answers_arr = np.array(answers, dtype=str)
    skipped = answers_arr == ""
    correct = answers_arr == ANSWER_KEY

    per_question = np.where(skipped, 0, np.where(correct, 4, -1))
    return int(per_question.sum())


def compute_median_score(scores: list[int]) -> int | float:
    """Median as required by the assignment/expected output.

    - Odd number of students: middle value (int)
    - Even number of students: average of two middle values (float)
    """

    sorted_scores = sorted(scores)
    n = len(sorted_scores)
    if n == 0:
        return 0

    mid = n // 2
    if n % 2 == 1:
        return sorted_scores[mid]

    return (sorted_scores[mid - 1] + sorted_scores[mid]) / 2


def report_statistics(scores: list[int]) -> None:
    if not scores:
        print("Mean (average) score: 0.00")
        print("Highest score: 0")
        print("Lowest score: 0")
        print("Range of scores: 0")
        print("Median score: 0")
        return

    scores_np = np.array(scores, dtype=float)

    mean = float(scores_np.mean())
    highest = int(scores_np.max())
    lowest = int(scores_np.min())
    score_range = highest - lowest
    median = compute_median_score(scores)

    print(f"Mean (average) score: {mean:.2f}")
    print(f"Highest score: {highest}")
    print(f"Lowest score: {lowest}")
    print(f"Range of scores: {score_range}")

    if isinstance(median, float):
        print(f"Median score: {median:.1f}")
    else:
        print(f"Median score: {median}")


def write_grade_file(input_file: Path, grades: list[tuple[str, int]]) -> Path:
    """Write `<class>_grades.txt` (no header), one line: `student_id,score`."""

    output_path = input_file.with_name(f"{input_file.stem}_grades.txt")
    df = pd.DataFrame(grades, columns=["student_id", "score"])
    df.to_csv(output_path, index=False, header=False)
    return output_path


def main() -> None:
    data_dir = Path(__file__).resolve().parent

    input_path, lines = prompt_for_class_file(data_dir)
    valid_records, _invalid_count = analyze_lines(lines)

    grades: list[tuple[str, int]] = []
    scores: list[int] = []

    for student_id, answers in valid_records:
        score = score_answers(answers)
        grades.append((student_id, score))
        scores.append(score)

    report_statistics(scores)
    write_grade_file(input_path, grades)


if __name__ == "__main__":
    main()
