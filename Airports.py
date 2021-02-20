import requests
import json
from bs4 import BeautifulSoup


def get_airport_data():
    # get ICAO, status, city, state and country for each airport
    # and saves the data to a json file

    json_file = "Airport_details.json"

    base_url = "https://airportnavfinder.com/index.php?op=airportlist&page="
    page = int(0)
    dictionary = {}
    # loop over all pages
    for i in range(690):
        page += 1
        url = base_url + str(page)
        side = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
            },
        )
        soup = BeautifulSoup(side.content, "html.parser")
        table = soup.find_all("div", attrs={"class": "aplist-row"})

        # loop over all rows in table
        for i in table:
            ICAO = i.find("a", href=True).text
            status = i.find("div", attrs={"class": "aplist-name"}).text
            city_state = i.find("div", attrs={"class": "aplist-lo"}).text
            city, *state = city_state.split(
                ","
            )  # state will be a list and will be empty if no state is available
            country = i.find("div", attrs={"class": "aplist-co"}).text

            # create sub dictionary
            sub_dict = {}
            sub_dict["ICAO"] = ICAO
            sub_dict["status"] = status
            sub_dict["city"] = city
            sub_dict["state"] = state
            sub_dict["country"] = country

            # add to dictionary
            dictionary[ICAO] = sub_dict

    # write dictionary to json
    with open(json_file, "w") as f:
        json.dump(dictionary, f)

    return dictionary
