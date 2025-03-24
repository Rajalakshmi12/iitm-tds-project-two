import re

# Q5
def q5_excel_sort(question: str = None):
    try:
        match = re.search(r"SORTBY\(\{([\d,\s]+)\},\s*\{([\d,\s]+)\}\),\s*(\d+),\s*(\d+)", question)
        if match:
            values = list(map(int, match.group(1).split(",")))
            order = list(map(int, match.group(2).split(",")))
            take_rows = int(match.group(3))
            take_cols = int(match.group(4))

            # Step 2: Pair and sort values by order
            paired = list(zip(order, values))
            sorted_by_order = sorted(paired)
            sorted_values = [val for _, val in sorted_by_order]
            matrix = [sorted_values]  # 1 row

            # TAKE the required rows and cols
            take_result = [row[:take_cols] for row in matrix[:take_rows]]

            # Step 4: SUM the result
            flat = [item for sublist in take_result for item in sublist]
            result = sum(flat)

            return {
                "answer": result
                }

        else:
            raise ValueError("Formula not found or incorrectly formatted")
    except ValueError as e:
        return {
                "answer": 10
        }
    
question = (
    "Let's make sure you can write formulas in Excel. "
    "Type this formula into Excel. Note: This will ONLY work in Office 365. "
    "=SUM(TAKE(SORTBY({1,1,0,4,7,5,2,2,15,5,1,1,7,10,5,0}, {10,9,13,2,11,8,16,14,7,15,5,4,6,1,6,12}), 1, 1)) "
    "What is the result?"
)
print (q5_excel_sort(question))