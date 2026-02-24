import pandas as pd
import numpy as np
import re
import sys
import os

def grade_exam():
    """
    Main function to run the grade exam application.
    Prompts user for a filename, processes the file, calculates grades,
    and generates a report.
    """
    while True:
        try:
            filename_input = input("Enter a class file to grade (i.e. class1 for class1.txt): ")
        except EOFError:
            # Handle end of input for automated testing
            break

        if not filename_input:
            continue

        # Handle cases where user might or might not include extension
        if filename_input.endswith('.txt'):
            filename = filename_input
            base_name = filename_input[:-4]
        else:
            filename = filename_input + '.txt'
            base_name = filename_input

        try:
            # Task 1: Open external text files
            # Using pandas to read the file line by line as a single column to satisfy "Use Pandas"
            # sep='|' assumes | is not in the file, which is safe for this dataset.
            # quoting=3 (csv.QUOTE_NONE) ensures no quoting behavior interferes.
            # engine='python' allows sep=None or multi-char, but here we use '|' to read whole line.
            df_raw = pd.read_csv(filename, sep='|', header=None, names=['line'], engine='python', quoting=3)
            print(f"Successfully opened {filename}")

            print("**** ANALYZING ****")
            print() # Blank line

            valid_lines = []
            invalid_count = 0

            # Task 2: Scan line by line and validate
            # We iterate over the dataframe rows
            for index, row in df_raw.iterrows():
                line = row['line']
                parts = line.split(',')

                # Check 1: Must contain exactly 26 values
                if len(parts) != 26:
                    print("Invalid line of data: does not contain exactly 26 values:")
                    print(line)
                    print() # Blank line after error
                    invalid_count += 1
                    continue

                # Check 2: N# is valid (N followed by 8 digits)
                student_id = parts[0]
                if not re.match(r'^N\d{8}$', student_id):
                    print("Invalid line of data: N# is invalid")
                    print(line)
                    print() # Blank line after error
                    invalid_count += 1
                    continue

                # Valid line
                valid_lines.append(parts)

            valid_count = len(valid_lines)

            print("**** REPORT ****")
            print()
            print(f"Total valid lines of data: {valid_count}")
            print(f"Total invalid lines of data: {invalid_count}")
            print() # Blank line

            # Task 3: Calculate grades and stats
            if valid_count > 0:
                # Create DataFrame for valid data
                # Columns: ID, Q1, Q2, ..., Q25
                columns = ['ID'] + [f'Q{i}' for i in range(1, 26)]
                df_data = pd.DataFrame(valid_lines, columns=columns)

                answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D".split(',')

                # Calculate scores
                # Extract answers (iloc[:, 1:])
                student_answers = df_data.iloc[:, 1:].values

                # Vectorized scoring
                # Correct answers (+4)
                correct_mask = (student_answers == answer_key)
                scores = np.sum(correct_mask, axis=1) * 4

                # Wrong answers (-1)
                # Wrong means: not correct AND not empty
                # Empty string implies skipped question (0 points)
                # Note: 'student_answers' contains strings.
                empty_mask = (student_answers == '')
                # Also handle None/NaN if any
                if np.issubdtype(student_answers.dtype, np.object_):
                     empty_mask = (student_answers == '') | (pd.isnull(student_answers))

                wrong_mask = (~correct_mask) & (~empty_mask)
                scores += np.sum(wrong_mask, axis=1) * -1

                df_data['Score'] = scores

                # Statistics
                mean_score = df_data['Score'].mean()
                max_score = df_data['Score'].max()
                min_score = df_data['Score'].min()
                range_score = max_score - min_score
                median_score = df_data['Score'].median()

                # Formatting Output
                print(f"Mean (average) score: {mean_score:.2f}")
                print(f"Highest score: {int(max_score)}")
                print(f"Lowest score: {int(min_score)}")
                print(f"Range of scores: {int(range_score)}")

                # Median formatting
                if valid_count % 2 == 1:
                    print(f"Median score: {int(median_score)}")
                else:
                    print(f"Median score: {median_score}")

                # Task 4: Generate result file
                output_filename = f"{base_name}_grades.txt"
                # Write headerless CSV: ID,Score
                df_data[['ID', 'Score']].to_csv(output_filename, index=False, header=False)

            # Exit after processing one file
            break

        except FileNotFoundError:
            print("File cannot be found.")
            # Loop again to ask for filename
        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    grade_exam()
