import os
import datetime
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from collections import defaultdict


import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


FILE_NAME_EXCEL = os.environ['FILE_NAME_EXCEL']


def find_date_foundation():
    day_the_week = datetime.datetime.today()
    year_foundation = 1920
    age = day_the_week.year-year_foundation
    return age


def split_file_into_categories():
    list_of_wines = pandas.read_excel(FILE_NAME_EXCEL, na_values=['N/A', 'NA'], keep_default_na=False).to_dict(orient='record')
    wines_group = defaultdict(list)
    for reading_files in list_of_wines:
        wines_group[reading_files['Категория']].append(reading_files)
    return wines_group


def main():
    file = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = file.get_template('template.html')
    rendered_page = template.render(
        age=find_date_foundation(),
        group_wines=split_file_into_categories()
    )
    
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
        
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
