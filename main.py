import os
import datetime
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from collections import defaultdict


import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


FILE_NAME_EXCEL = os.environ['FILE_NAME_EXCEL']


def main():
    day_the_week = datetime.datetime.today()
    this_year = day_the_week.year
    year = 1920
    age = this_year-year
    reading_file = pandas.read_excel(FILE_NAME_EXCEL, na_values=['N/A', 'NA'], keep_default_na=False).to_dict(orient='record')
    file = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = file.get_template('template.html')
    wines_group = defaultdict(list)
    for reading_files in reading_file:
        wines_group[reading_files['Категория']].append(reading_files)
    rendered_page = template.render(
        age=age,
        group_wines= wines_group
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()