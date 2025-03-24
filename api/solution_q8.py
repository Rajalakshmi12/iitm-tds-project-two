from datetime import datetime, timedelta
import re

# Q8
def q8_extract_csv(question: str = None):
    date_matches = re.findall(, question)

 # Define the date range
    start_date = datetime(1980, 4, 16)
    end_date = datetime(2009, 2, 11)

    # Initialize a counter for Wednesdays
    wednesday_count = 0

    # Iterate through the date range
    current_date = start_date
    while current_date < end_date:
        if current_date.weekday() == 2:  # 2 represents Wednesday
            wednesday_count += 1
        current_date += timedelta(days=1)


    current_date = start_date
    while current_date < end_date:
        if current_date.weekday == 2:
            wednesday_count+1
        current_date += timedelta(days=1)
        
    # Output the total number of Wednesdays
    return {
        "answer": wednesday_count
    }

question = "How many Wednesdays are there in the date range 1980-04-16 to 2009-02-11? The dates are in the year-month-day format. Include both the start and end date in your count. You can do this using any tool (e.g. Excel, Python, JavaScript, manually)."

    