from datetime import datetime, timedelta


def is_more_than_two_weeks_away(date_string):
    # Parse the input date string
    input_date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')

    # Calculate the current date
    current_date = datetime.utcnow()

    # Calculate the difference between the input date and the current date
    date_difference = input_date - current_date

    # Define a timedelta of two weeks
    two_weeks = timedelta(weeks=2)

    # Compare the difference with two weeks
    return date_difference < two_weeks
