import pandas as pd
import requests
import time

# Enter your EBIRD API key
api_key = 'YOUR-API-KEY'

# Base URL for eBird API 2.0
EBIRD_URL = 'https://ebird.org/ws2.0/data/obs'
# Set to search for Arizona locations
LOC_ID = 'US-AZ'

def find_observations(lat, lng, radius, start_date, end_date, output_file="observations.csv"):
    num_days = (end_date - start_date).days + 1
    obs_dates = pd.date_range(start_date, periods=num_days, freq='D')

    # Create a list to hold the individual dictionaries of observationsrint(f)
    observations = []

    # Get results for each date in the range separately
    for d in obs_dates:
        time.sleep(0.5) # time delay between requests to avoid flooding the server
        ymd = '{}/{}/{}'.format(d.year, d.month, d.day)

        # Build the URL
        url_fmt = "{}/{}/historic/{}?rank=mrec&detail=full&cat=species&lat={}&lng={}&dist={}"

        url_obs = url_fmt.format(
            EBIRD_URL,
            LOC_ID,
            ymd,
            lat,
            lng,
            radius
        )

        # Get the observations for one location and date
        obs = requests.get(url_obs,
        headers={"X-eBirdApiToken":api_key})

        # Append the new observations to the master list
        #print(obs.status_code)
        #print(obs.json())
        #print('')
        observations.extend(obs.json())

    # Convert the list of dictionaries to a pandas dataframe
    obs_df = pd.DataFrame(observations)

    # Quickly verify the structure of the dataframe
    print(obs_df.info())

    summ = obs_df[['userDisplayName','locName','lat','lng','speciesCode','howMany']]
    # Check out the species counts of the first few rows
    print(summ[['speciesCode','howMany']].head())
    # Export the dataframe to a csv file
    summ.to_csv(output_file, index=False)

start_date = pd.Timestamp('20181216')
end_date = pd.Timestamp('20181216')
Lat = 31.0408
Long = -111.086
Radius = 10

find_observations( Lat, Long, Radius, start_date, end_date)