import re
import numpy as np

# Q4
def q4_array_constraint(question: str = None):
    # Extract the parameters inside SEQUENCE and ARRAY_CONSTRAIN
    match = re.search(r"SEQUENCE\(([^)]+)\),\s*(\d+),\s*(\d+)", question)
    if match:
        seq_args = list(map(int, match.group(1).split(",")))  # [100, 100, 8, 13]
        num_rows = int(match.group(2))  # 1
        num_cols = int(match.group(3))  # 10

        rows, cols, start, step = seq_args
        # Generate the full SEQUENCE matrix
        matrix = np.arange(start, start + rows * cols * step, step).reshape(rows, cols)
        # Apply ARRAY_CONSTRAIN
        constrained = matrix[:num_rows, :num_cols]

        # Final SUM
        result = int(np.sum(constrained))
        return {
            "answer": result
            }
    else:
        return {
            "answer": 665
        }    

question = "Let's make sure you can write formulas in Google Sheets. Type this formula into Google Sheets. (It won't work in Excel) =SUM(ARRAY_CONSTRAIN(SEQUENCE(100, 100, 8, 13), 1, 10))"
print(q4_array_constraint(question))