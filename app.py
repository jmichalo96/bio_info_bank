from flask import Flask, render_template, request, redirect, make_response, url_for
import os
import file_menager
from data_menager import test_urls #, URL_COLUMN, REQUIREMENT_STATUS, STATUS_MESSAGE, STATUS_CODE, TIME_STAMP, LOAD_TIME, REQUIREMENT_STRING_COLUMN


# zmieniłem INTERPRETER w ustawieniach


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
requirement_file_path = 'files/content_requirements.csv'
log_file_path = 'files/log_file.txt'


# app.secret_key = os.urandom(24)
# app.config.update(SECRET_KEY=os.urandom(24))
# SECRET_KEY = os.environ.get("SECRET_KEY", default=None)


@app.route('/', methods=['GET'])
def home_page():
    urls_with_requirements = file_menager.open_file(requirement_file_path)
    urls_with_requirements = test_urls(urls_with_requirements, log_file_path)
    # urls_list = [row[URL_COLUMN] for row in urls_with_requirements]
    return render_template("main_page.html", urls_list=urls_with_requirements)


if __name__ == '__main__':
    app.run()
