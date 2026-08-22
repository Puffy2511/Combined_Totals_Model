
import requests
import json
import math
import numpy as np
import scipy as sp

API_key = '???' #<- Go to The Odds Api, create your account and sub your perso API key 
sport = 'aussierules_afl'
region = 'au'
bookmaker = 'pointsbetau'
market = 'player_disposals,player_disposals_over'
odds_format = 'decimal'


def get_events():

    url = f"https://api.the-odds-api.com/v4/sports/{sport}/events"
    params = {'api_key': API_key}

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code}:{response.text}")
        return None

    events = response.json()

    if not events:
        print("No events")
        return None

    print("AFL Games: \n")
    for i, event in enumerate(events):
        print(f"[{i}]: {event['home_team']} vs {event['away_team']}")

    index = int(input("Choose an event: "))
    return events[index]['id']


def fetch_data(event_id):

    url = f"https://api.the-odds-api.com/v4/sports/{sport}/events/{event_id}/odds"

    # params although they are lax on apikey and format
    params = {
        'api_key': API_key,
        'format': odds_format,
        'regions': region,
        'markets': market,
        'bookmakers': bookmaker
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code}:{response.text}")

    event_data = response.json()

    if 'bookmakers' not in event_data:
        print(f" No data (yet?) in {bookmaker}")
        return None

    # because of the two markets, you merge them into one big list so you can see both over/under and alt
    outcomes = []
    for m in event_data['bookmakers'][0]['markets']:
        outcomes.extend(m['outcomes'])

    #Organise player profiles using the key as the player's name
    player_profiles = {}
    for o in outcomes:
        p_name = o['description']
        if p_name not in player_profiles:
            player_profiles[p_name] = []
        player_profiles[p_name].append(o)

    final_market = {}
    for player, lines in player_profiles.items():
        disposals = {}
        for l in lines:
            p = l['point']
            disposals[p] = disposals.get(p, 0) + 1

        fifty_fifty =[p for p, count in disposals.items() if count ==2 ]

        # Could be a bench player so there could be no 50 50 lines for them, hence this safeguard
        if fifty_fifty:
            fifty_fifty_val = fifty_fifty[0]
        else:
            closest_fifty = min(lines, key = lambda x: abs(x['price']-1.87))
            fifty_fifty_val = closest_fifty['point']

        fifty_fifty_over = next((l['price'] for l in lines if l['point'] == fifty_fifty_val and l['name'] == 'Over'),None)

        if fifty_fifty_over:
            final_market[player] = {
                'mean_disposals':fifty_fifty_val,
                'mean_odds': fifty_fifty_over,
                'alt_lines':lines
            }

    return final_market

def devig(final_market):

    cleaned_market = {}

    for player, info in final_market.items():

        fifty_prob = 1 / info['mean_odds']

        k = math.log(0.5)/math.log(fifty_prob)

        player_cdf_disp = []

        for line in info['alt_lines']:
            odds = line['price']
            disp  = line['point']
            side = line['name']

            implied_p = 1/odds

            fair_p = math.pow(implied_p,k)

            if side == 'Over':
                cdf_val = 1- fair_p

            else:
                cdf_val = fair_p

            player_cdf_disp.append({
                'line': disp,
                'cdf': cdf_val
            })

        cleaned_market[player] = {
            'mean': info['mean_disposals'],
            'vig_factor': k,
            'cdf_pts': player_cdf_disp
        }

    return cleaned_market
    
def normal_params(cleaned_market):

    params = {}

    for player, info in cleaned_market.items():
        mu = info['mean']
        points = info['cdf_pts']

        # continuity correction cause o22.5 = 23
        x_pts = np.array([p['line']-0.5 for p in points])
        y_targets = np.array([p['cdf'] for p in points])

        def residual(sigma):
            if sigma <= 0:
                return np.ones_like(y_targets) * 1e6
            return sp.stats.norm.cdf(x_pts,mu,sigma) - y_targets

        if len(x_pts) >= 2:
            res = sp.optimize.least_squares(residual, x0 = 6.0, bounds = (2.0,15.0))
            sigma = res.x[0]
        else:
            # Guessing rn but might update with a check later idk
            sigma = 0.2 * mu

        params[player]={
            'mu': mu,
            'sigma': sigma
        }
    return params

#-------------------
event_id = get_events()

if event_id:
    raw_market = fetch_data(event_id)

    if raw_market:
        cleaned_market = devig(raw_market)
        
        if cleaned_market:
            player_params = normal_params(cleaned_market)
            print(json.dumps(cleaned_market, indent=4))
