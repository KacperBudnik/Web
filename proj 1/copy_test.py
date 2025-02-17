from bs4 import BeautifulSoup
import time
import requests
from typing import List
import csv
from sys import argv

# wyciąganie kwoty z tekstu w formacie $123 456 789
def get_money_amount(money_string):
    return int(money_string.split("$")[1].replace(" ", ""))


class FilmDetailed:
    def __init__(self, title: str, year: int, genre: str, award_amount: int, box_office: int | None, budget: int | None, time_mins: int | None, reviews: List[int]):
        self.title = title
        self.year = year
        self.genre = genre
        self.award_amount = award_amount
        self.box_office = box_office
        self.budget = budget
        self.time_mins = time_mins
        self.reviews = reviews


def save_detailed_films_to_csv(films: List[FilmDetailed], filename: str, new_file: bool):
    headers = ["Title", "Year", "Genre", "Award Amount", "Box Office", "Budget", "Time (mins)", "Reviews"]
    if new_file:
        mode = "w"
    else:
        mode = "a"

    # żeby nie trzeba było zamykać potem pliku
    with open(filename, mode=mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)

        if new_file:
            writer.writerow(headers)

        for film in films:
            if film.box_office is None:
                box_office = "-"
            else:
                box_office = film.box_office

            if film.budget is None:
                budget = "-"
            else:
                budget = film.budget

            if film.time_mins is None:
                time = "-"
            else:
                time = film.time_mins
            writer.writerow([
                film.title,
                film.year,
                film.genre,
                film.award_amount,
                box_office,
                budget,
                time,
                f'"{",".join(map(str, film.reviews))}"'
            ])


class Film:
    def __init__(self, title: str, year: int, genre: str, award_amount: int, box_office: int | None, budget: int | None, time_mins: int, score_avg: float | None):
        self.title = title
        self.year = year
        self.genre = genre
        self.award_amount = award_amount
        self.box_office = box_office
        self.budget = budget
        self.time_mins = time_mins
        self.score_avg = score_avg


def save_films_to_csv(films: List[Film], filename: str, new_file: bool):
    headers = ["Title", "Year", "Genre", "Award Amount", "Box Office", "Budget", "Time (mins)", "Score"]
    if (new_file):
        mode = "w"
    else:
        mode = "a"

    with open(filename, mode=mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)

        if new_file:
            writer.writerow(headers)

        for film in films:

            if film.box_office is None:
                box_office = "-"
            else:
                box_office = film.box_office

            if film.budget is None:
                film_budget = "-"
            else:
                film_budget = film.budget
                
            if film.time_mins is None:
                film_time = "-"
            else:
                film_time = film.time_mins

            if film.score_avg is None:
                film_score = "-"
            else:
                # 2 miejsca po przecinku
                film_score = "{:.2f}".format(film.score_avg)
                
            writer.writerow([
                film.title,
                film.year,
                film.genre,
                film.award_amount,
                box_office,
                film_budget,
                film_time,
                film_score
            ])


base_url = "https://www.filmweb.pl"

def url_films_on_page(pageNum: int):
    return base_url + "/films/search?page=" + str(pageNum)


films_detailed = []
films = []
max_page = 1000

# z argumentów linii komend można podać numer strony, od której zacząć, oraz maksymalną ilość stron do przeszukania
# zabezpieczenie jakby się program wywalił
if len(argv) > 1:
    if argv[1]:
        page = int(argv[1])
        film_count = (page-1)*10
    else:
        if len(argv) > 2:
            max_page = int(argv[2])
        page = 1
        film_count = 1
    if "--file-created" in argv:
        created_films_csv = True
    else:
        created_films_csv = False
else:
    page = 1
    film_count = 1


# główna pętla która idzie po stronach najpopularniejszych filmów
while page <= max_page:
    print(f"Page: {page}")

    start = time.time()
    film_list_response = requests.get(url_films_on_page(page))
    film_list_html = BeautifulSoup(film_list_response.text)
    film_list_element = film_list_html.select_one('.searchApp__results.previewHolder.hasBorder.isSmall.hasRatings.hasBadge.showGenres.showCast.showExtra.showOriginalTitle')
    if film_list_element:
        film_links = film_list_element.select(".preview__link")
        for link in film_links:
            film_page_response = requests.get(base_url + link["href"])
            response_html = BeautifulSoup(film_page_response.text)
            title = response_html.select_one(".filmCoverSection__title").text
            print(f"Film nr {film_count}: {title}")
            year = int(response_html.select_one(".filmCoverSection__year").text)
            runtime_el = response_html.select_one(".filmCoverSection__duration")

            if runtime_el:
                # wyciąga ilość minut z czasu trwania filmu
                runtime = runtime_el.text
                if "h" in runtime:
                    hours = int(runtime.split("h")[0])
                else:
                    hours = 0

                if "m" in runtime:
                    minutes = int(runtime.split(" ")[-1].split("m")[0])
                else:
                    minutes = 0
                runtime_mins = hours*60+minutes
            else:
                runtime_mins = None

            genre_el = response_html.find("span", class_="linkButton__label", itemprop="genre")
            if genre_el:
                genre = genre_el.text
            else:
                genre = "-"

            boxoffice_all = response_html.select_one("span.filmInfo__info.filmInfo__info--column")
            if boxoffice_all:
                boxoffice_world_els = [box_el for box_el in boxoffice_all.children if "na świecie" in box_el.text]
                if len(boxoffice_world_els) > 0:
                    boxoffice_gross_el = boxoffice_world_els[0]
                    boxoffice_gross = get_money_amount(boxoffice_gross_el.text.split("na świecie")[0])
                else:
                    boxoffice_usa_els = [box_el for box_el in boxoffice_all.children if "w USA" in box_el.text]
                    if len(boxoffice_usa_els) > 0:
                        boxoffice_usa_el = boxoffice_usa_els[0]
                        boxoffice_gross = get_money_amount(boxoffice_usa_el.text.split("w USA")[0])
                    else:
                        boxoffice_gross = None
            else:
                boxoffice_gross = None
            
            budget_element = response_html.find("span", string="budżet")
            if budget_element:
                sibling = budget_element.find_next_sibling("span", class_='filmInfo__info')
                budget_el = sibling.select_one("span")
                budget = get_money_amount(budget_el.text)
            else:
                budget = None


            awards_element = response_html.select_one("a.awardsSection__link")
            if awards_element:
                # przejście do strony z nagrodami (liczymy też nominacje)
                awards_link = awards_element["href"]
                awards_response = requests.get(base_url + awards_link)
                awards_html = BeautifulSoup(awards_response.text)
                award_amount = int(awards_html.select_one("span.page__headerCounter").text)
            else:
                award_amount = 0

            # dla szczegółowych filmów pobieramy też oceny
            if page == 1:
                # reviews
                film_reviews = []
                forum_page = 1
                forum_response = requests.get(base_url + link["href"] + "/discussion?page=" + str(forum_page))
                forum_html = BeautifulSoup(forum_response.text)

                # szuka ile jest stron na forum
                pagination_elements = forum_html.select("ul.pagination__list")
                pagination_element = pagination_elements[-1]
                #print("pagination element")
                #print(pagination_element)
                pagination_buttons = [
                    li for li in pagination_element.find_all('li', class_='pagination__item')
                    if 'pagination__item--next' not in li.get('class', [])
                ]
                pages_amount = int(pagination_buttons[-1].select_one("a").text)
                print(f"Visiting {pages_amount} forum pages...")


                while forum_page <= pages_amount:
                    print(f"forum page: {forum_page}")
                    topics_list = forum_html.select_one("div.forumTopicsList__items")
                    for forum_topic in topics_list.findChildren("div", recursive=False):
                        topic_review = forum_topic.select_one("span.forumTopic__starsNo")
                        if topic_review:
                            review = int(topic_review.text)
                            film_reviews.append(review)
                    forum_page += 1
                    forum_response = requests.get(base_url + link["href"] + "/discussion?page=" + str(forum_page))
                    forum_html = BeautifulSoup(forum_response.text)
                films_detailed.append(FilmDetailed(title, year, genre, award_amount, boxoffice_gross, budget, runtime_mins, film_reviews))
            # dla zwykłych filmów
            else:
                score_el = response_html.select_one("div.filmRating.filmRating--filmRate.filmRating--hasPanel")
                if score_el:
                    score = float(response_html.select_one("div.filmRating.filmRating--filmRate.filmRating--hasPanel")["data-rate"])
                else:
                    score = None
                films.append(Film(title, year, genre, award_amount, boxoffice_gross, budget, runtime_mins, score))
            film_count += 1
    # koniec danej strony

    # mierzymy czas wykonania strony
    end = time.time()
    print(f"Page {page} finished, took {end-start} s")

    # zapisywanie szczegółowych filmów
    if page == 15:
        print("Saving detailed films to csv!")
        save_detailed_films_to_csv(films_detailed, "./films_detailed.csv", True)

    # zapisywanie zwykłych filmów co 10 stron
    elif page % 10 == 0:
        print("Saving films to csv!")
        save_films_to_csv(films, "./films.csv", not created_films_csv)
        created_films_csv = True
        films = []
    page += 1


