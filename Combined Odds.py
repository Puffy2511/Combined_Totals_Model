
import requests

API_key = "????" # <-- Go to The Odds.api and make an account, copypaste your api key to put there
sport = "aussierules_afl"
region = "au"
bookmaker = "pointsbetau"
market = "player_disposals,player_disposals_over"
odds_format = "decimal"


def get_events():

    url = f"https://api.the-odds-api.com/v4/sports/{sport}/events"
    params = {"api_key": API_key}

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None

    events = response.json()

    if not events:
        print("No events")
        return None

    print("AFL Games: \n")
    for i, event in enumerate(events):
        print(f"[{i}]: {event['home_team']} vs {event['away_team']}")

    index = int(input("Choose an event: "))
    return events[index]['id'], events[index]['home_team'], events[index]['away_team']



