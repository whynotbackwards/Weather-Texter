# import os
import requests
from twilio.rest import Client
# from twilio.http.http_client import TwilioHttpClient
try:
    import config
except ModuleNotFoundError:
    import config_dummy as config


# Open Weather Map API Parameters
OWM_ENDPOINT = 'https://api.openweathermap.org/data/2.5/onecall'
parameters = {
    'lat': config.LAT,
    'lon': config.LONG,
    'appid': config.OMW_API_KEY,
    'units': 'imperial',
    'exclude': 'minutely,alerts',
}

response = requests.get(OWM_ENDPOINT, params=parameters)
response.raise_for_status()

weather_data = response.json()

curr_temp = round(weather_data['current']['temp'])
curr_feel = round(weather_data['current']['feels_like'])

max_temp = round(weather_data['daily'][0]['temp']['max'])
max_feel = round(weather_data['daily'][0]['feels_like']['day'])

weather_codes = [hour['weather'][0]['id'] for hour in weather_data['hourly'][:12]]

will_rain = False
will_snow = False

for code in weather_codes:
    if code < 600:
        will_rain = True
    if 600 <= code < 700:
        will_snow = True

weather_msg = f".\n\n🌡 Current Temp = {curr_temp} (feels like {curr_feel})\n" \
              f"🔥 Today's High = {max_temp} (feels like {max_feel})"

if will_rain or will_snow:
    weather_msg += "\n\n☔ \"IT'S GONNA RAIN!\" -Ollie Williams" * will_rain + \
                   "\n\n❄ Let it snow, let it snow, let it snow!" * will_snow

# Add http proxy client when running in PythonAnywhere:
# proxy_client = TwilioHttpClient()
# proxy_client.session.proxies = {'https': os.environ['https_proxy']}

client = Client(config.TWILIO_ACCT_SID, config.TWILIO_AUTH_TOKEN)  # , http_client=proxy_client)
message = client.messages.create(
    body=weather_msg,
    from_=config.FROM_PHONE,
    to=config.TO_PHONE
)

# print(message.sid)
