from datetime import datetime, timezone
from garminconnect import Garmin
from notion_client import Client
from dotenv import load_dotenv
import pytz
import os

from datetime import date, datetime
from garminconnect import Garmin
from notion_client import Client
import os

from datetime import date, timedelta
from garminconnect import Garmin
from notion_client import Client
from dotenv import load_dotenv
import os

from datetime import datetime
from garminconnect import Garmin
from notion_client import Client
from dotenv import load_dotenv, dotenv_values
import pytz
import os

# Constants
local_tz = pytz.timezone("Europe/Amsterdam")

# Load environment variables
load_dotenv()
CONFIG = dotenv_values()

def get_hrv_data(garmin):
    today = datetime.today().date()
    return garmin.get_hrv_data(today.isoformat())

def get_womens_health_data(garmin):
    """Retrieve women's health related data."""
    today = datetime.today().date()
    
    # Date range for menstrual data
    start_date = today - timedelta(days=90)  # Last 90 days
    end_date = today + timedelta(days=30)    # 30 days into the future
    
    try:
        # Get pregnancy summary
        print("\nRetrieving pregnancy summary data...")
        try:
            pregnancy_data = garmin.get_pregnancy_summary()
        except Exception as e:
            print(f"Could not retrieve pregnancy data: {e}")
            
        # Get menstrual data for today
        print("\nRetrieving menstrual data for today...")
        try:
            menstrual_data = garmin.get_menstrual_data_for_date(today.isoformat())
        except Exception as e:
            print(f"Could not retrieve menstrual data for today: {e}")
            
        # Get menstrual calendar data for date range
        print(f"\nRetrieving menstrual calendar data from {start_date.isoformat()} to {end_date.isoformat()}...")
        try:
            menstrual_calendar = garmin.get_menstrual_calendar_data(start_date.isoformat(), end_date.isoformat())
        except Exception as e:
            print(f"Could not retrieve menstrual calendar data: {e}")
            
    except (GarminConnectConnectionError, GarminConnectAuthenticationError, 
            GarminConnectTooManyRequestsError, requests.exceptions.HTTPError) as err:
        logger.error(f"Error retrieving women's health data: {err}")
    return menstrual_data

def main():
    load_dotenv()

    # Initialize Garmin and Notion clients using environment variables
    garmin_email = "kattelijn@boumail.com"
    garmin_password = "abcd1234#Garmin"
    notion_token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("NOTION_SLEEP_DB_ID")

    # Initialize Garmin client and login
    garmin = Garmin(garmin_email, garmin_password)
    garmin.login()
    client = Client(auth=notion_token)

    data1 = get_womens_health_data(garmin)
    data2 = get_hrv_data(garmin)
    today = datetime.today().date()
    print(garmin.get_heart_rates(today.isoformat()))
    print()
    print(garmin.get_training_readiness(today.isoformat()))
    print()
    print(data1)
    print()
    print(data2)
    print()
    print(garmin.get_training_status(today.isoformat()))
    print()
    print(garmin.get_rhr_day(today.isoformat()))
    print()
    print(garmin.get_race_predictions())
    print()
    print(garmin.get_all_day_events(today.isoformat()))
    # if data:
    #     sleep_date = data.get('dailySleepDTO', {}).get('calendarDate')
    #     if sleep_date and not sleep_data_exists(client, database_id, sleep_date):
    #         create_sleep_data(client, database_id, data, skip_zero_sleep=True)

if __name__ == '__main__':
    main()