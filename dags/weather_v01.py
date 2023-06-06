from bs4 import BeautifulSoup
import requests



def weather_now():
    url = "https://www.meteoprog.pl/en/weather/Tychy/"

    result = requests.get(url).text
    doc = BeautifulSoup(result, "html.parser")
    weather = {}
    time = doc.find(class_="page-columns-wrapper").time['datetime']
    current_temperature = doc.find(class_="current-temperature").span.text
    feels_like = doc.find(class_="feels-like").b.text
    sky = doc.find(class_="page-columns-wrapper").h3.text
    chance_of_precipitation = doc.find(class_="atmosphere-spec").b.text
    wind = doc.find_all(class_="atmosphere-spec")[1].b.text
    pressure = doc.find_all(class_="atmosphere-spec")[2].b.text
    uv_index = doc.find_all(class_="atmosphere-spec")[3].b.text
    humidity = doc.find_all(class_="atmosphere-spec")[4].b.text
    precipitation = doc.find_all(class_="atmosphere-spec")[5].b.text
    weather = {
        "time": time,
        "current_temperature": current_temperature,
        "feels_like": feels_like,
        "sky": sky,
        "chance_of_precipitation": chance_of_precipitation,
        "wind": wind,
        "pressure": pressure,
        "uv_index": uv_index,
        "humidity": humidity,
        "precipitation": precipitation,
        "timestamps": time[0:10]
    }


    return weather




