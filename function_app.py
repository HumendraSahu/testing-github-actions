import azure.functions as func
import logging
from datetime import date, timedelta
import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

def get_16th_working_days_for_year():
    today = date.today()
    year = today.year
    result_dates = []

    for month in range(1, 13):
        working_days = []
        day = date(year, month, 1)

        while day.month == month:
            if day.weekday() < 5:  # Monday to Friday
                working_days.append(day)
            day += timedelta(days=1)

        if len(working_days) >= 16:
            result_dates.append(working_days[15].isoformat())
        else:
            result_dates.append(None)  # or skip, or add a placeholder like "N/A"

    return result_dates

@app.route(route="http_trigger_calc_working_days")
def http_trigger_calc_working_days(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    dates = get_16th_working_days_for_year()
    print("dates----", dates)

        # Get today's date in ISO format (YYYY-MM-DD)
    today_str = date.today().isoformat()

    # Check if today is in the list of 16th working days
    is_today_16th_working_day = today_str in dates

    print("Is today the 16th working day of the month?:", is_today_16th_working_day)
    response_body = {
        "dates": dates,
        "is_today_16th_working_day": is_today_16th_working_day
    }
    return func.HttpResponse(
        body=json.dumps(response_body),
        status_code=200,
        mimetype="application/json"
    )
