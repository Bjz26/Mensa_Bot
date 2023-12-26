import requests
from bs4 import BeautifulSoup
import re
from datetime import date, timedelta
import holidays


def get_vegan_meals_for_date(input_date: date):
    
    if input_date.weekday() == 6 or input_date in holidays.Germany():
        return f'Am {input_date.strftime("%d.%m.%Y")} hat die Mensa geschlossen, da es ein Sonntag oder Feiertag ist.'


    # Send a GET request to the website
    response = requests.get(f'https://www.studentenwerk-leipzig.de/mensen-cafeterien/speiseplan?location=all&date={input_date.strftime("%Y-%m-%d")}&criteria=&meal_type=all')

    # Create a BeautifulSoup object and parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all h3 headers with class 'title-prim' and text 'Veganes Gericht'
    headers = soup.find_all('h3', class_='title-prim', string='Veganes Gericht')

    todays_date_german = input_date.strftime("%d.%m.%Y")
    return_string = f'Am {todays_date_german} gibt es folgende vegane Hauptgerichte in den Leipziger Mensen:\n\n'


    # For each header, find the next division which should contain the prices and compounds
    for header in headers:
        division = header.find_next_sibling()
        prices = division.find('p', class_='meals__price').text.strip()
        first_price = re.search(r'(\d+,\d+)\s€', prices).group(1)
        # Extract the meal's name
        meals_name = division.find('h4', class_='meals__name').text.strip()

        # Find the h2 tag that precedes the h3 tag
        restaurant_name = header.find_previous('h2').text.strip()

        # Add the strings to the return_string
        return_string += restaurant_name + '\n'
        return_string += 'Veganes Essen: ' + meals_name + '\n'
        return_string += 'Preis: ' + first_price + '\n\n'

    return return_string

if __name__ == '__main__':
    print(get_vegan_meals_for_date(date.today()))
