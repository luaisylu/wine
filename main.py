import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from collections import defaultdict

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape


def main():
    basis = datetime.date(year=1920, month=1, day=1)
    current_date = basis.year
    day_the_week = datetime.datetime.today()
    this_year = day_the_week.year
    age = this_year-current_date
    wine_file = pandas.read_excel('wine3.xlsx', na_values=['N/A', 'NA'], keep_default_na=False).to_dict(orient='record')
    file = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = file.get_template('template.html')
    group_wines = defaultdict(list)
    for wine_files in wine_file:
       group_wines[wine_files['Категория']].append(wine_files)
    rendered_page = template.render(
        age=age,
        wines=wine_file,
        group_wines=group_wines
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()