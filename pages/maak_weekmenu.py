#Hier maken we het mogelijk om een weekmenu samen te stellen

from utils import get_all_ingredients_in_month, get_all_recipe_names
from pages.ingredient_form import select_ingredient
from datetime import date

maanden = {
    1: 'jan',
    2: 'feb',
    3: 'maa',
    4: 'apr',
    5: 'mei',
    6: 'jun',
    7: 'jul',
    8: 'aug',
    9: 'sep',
    10: 'okt',
    11: 'nov',
    12: 'dcbr',
}

def maak_weekmenu():
    today = date.today()
    today_month = today.month
    today_day = today.day
    month = maanden[today_month]
    # als we in de eerste helft van de maand zitten dan worden de groenten van de vorige maand erbij genomen
    # als we in de tweede helft van de maand zitten dan nemen we de groenten van de volgende maand erbij
    if today_day < 16:
        closest_month = -1
    else:
        closest_month = 1

    if today_month + closest_month in range(1,13):
        extra_month = maanden[today_month + closest_month]
    elif today_month + closest_month == 0:
        extra_month = maanden[12]
    elif today_month + closest_month == 13:
        extra_month = maanden[1]
    ingredients_thismonth = get_all_ingredients_in_month(month)
    ingredients_extramonth = get_all_ingredients_in_month(extra_month)
    ingredients_extra = [item for item in ingredients_extramonth if item not in ingredients_thismonth]
    ingredient_all = sorted(ingredients_thismonth + ingredients_extra)
    select_ingredient(ingredients_this_month = ingredient_all)


if __name__ == "__main__":
    maak_weekmenu()
