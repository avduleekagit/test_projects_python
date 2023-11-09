import datetime

def get_working_days(start_date, end_date):
    # Create a list of weekdays to exclude (Saturday and Sunday)
    weekdays_to_exclude = [5, 6]  # 5=Saturday, 6=Sunday

    # Create a datetime object for the start and end dates
    start_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    # Create an empty list to store the working days
    working_days = []

    # Loop through each day between the start and end dates
    current_date = start_date_obj
    while current_date <= end_date_obj:
        # Check if the day is a weekday (not in the list of weekdays to exclude)
        if current_date.weekday() not in weekdays_to_exclude:
            # Add the current date to the list of working days
            working_days.append(current_date.strftime('%Y-%m-%d'))

        # Increment the current date by one day
        current_date += datetime.timedelta(days=1)

    # Return the list of working days
    return working_days
