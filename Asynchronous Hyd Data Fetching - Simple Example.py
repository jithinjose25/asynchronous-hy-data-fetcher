import asyncio
import httpx
import pandas as pd 

api_url = "https://api.weather.gc.ca/collections/hydrometric-daily-mean/items"


async def fetch_hydrometric_data(client, start, end, station):

    hyd_results_dict_list = []

    params = {"f": "json", "datetime": f"{start}/{end}", "STATION_NUMBER" :  station, "limit": 10000}

    response = await client.get(url = api_url, params = params, timeout = 20)
    response.raise_for_status()
    response_dict = response.json()
    features = response_dict.get("features")
    for feature in features:
        prop = feature.get("properties")
        discharge = prop.get("DISCHARGE")
        wl = prop.get("LEVEL")
        st_name = prop.get("STATION_NAME")
        st_num = prop.get("STATION_NUMBER")   
        date = prop.get("DATE")
        row = {"Date": date, "Station Name": st_name, "Station Number": st_num, "Disharge" : discharge, "Water Level": wl}
        hyd_results_dict_list.append(row)

    results_one_station_df = pd.DataFrame(hyd_results_dict_list)

    return results_one_station_df
    



async def main():

    start_timestamp = input("Enter the start date in ISO format: ")
    end_timestamp = input("Enter the end date in ISO format : ")

    station_input = input("Enter the station numbers you want to retrieve the hyd data for (comma separated): ")

    stations = [s.strip().upper() for s in station_input.split(",") if s.strip()]

    async with httpx.AsyncClient() as client:
        tasks = [fetch_hydrometric_data(client, start_timestamp, end_timestamp,station) for station in stations]
        results = await asyncio.gather(*tasks)

    all_station_results_df = pd.concat(results, ignore_index=True)
    print(all_station_results_df)





if __name__ == "__main__":
    asyncio.run(main())