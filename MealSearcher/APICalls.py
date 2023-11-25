from pathlib import Path

import requests


# API:
# https://www.themealdb.com/api.php

def search_by_name(name: str):
    response = requests.get(f"https://www.themealdb.com/api/json/v1/1/search.php?s={name}")
    if response.status_code == 200:
        return response.json().get('meals')
    return None


def search_by_main_ingredient(main_ingredient: str):
    response = requests.get(f"https://www.themealdb.com/api/json/v1/1/filter.php?i={main_ingredient}")
    if response.status_code == 200:
        print(response.json())
        return response.json().get('meals')
    return None


def search_by_category(name: str):
    response = requests.get(f"https://www.themealdb.com/api/json/v1/1/filter.php?c={name}")
    if response.status_code == 200:
        print(response.json())
        return response.json().get('meals')
    return None


def search_by_area(name: str):
    response = requests.get(f"https://www.themealdb.com/api/json/v1/1/filter.php?a={name}")
    if response.status_code == 200:
        print(response.json())
        return response.json().get('meals')
    return None


def get_random_meals():
    meals = []
    for i in range(10):
        response = requests.get("https://www.themealdb.com/api/json/v1/1/random.php")
        meals.append(response.json().get('meals')[0])
    return meals


def get_meal_by_id(meal_id: str):
    response = requests.get(f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}")
    return response.json().get('meals', [None])[0]


def download_picture(pic_url):
    Path("./temp").mkdir(exist_ok=True)
    with open('./temp/picture.jpg', 'wb') as file:
        response = requests.get(pic_url)
        if not response.ok:
            print(response)
            return False

        for block in response.iter_content(1024):
            if not block:
                break
            file.write(block)
        return True
