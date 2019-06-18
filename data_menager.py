"""
This module checks website requirements and check duration time
"""
from urllib import request, error
import ssl
import time, datetime
import platform
import file_menager


URL_COLUMN = 0
REQUIREMENT_STRING_COLUMN = 1
STATUS_CODE = 2
STATUS_MESSAGE = 3
TIME_STAMP = 4
LOAD_TIME = 5
REQUIREMENT_STATUS = 6


# requests.get("https://www.restapitutorial.com/httpstatuscodes.html").elapsed.total_seconds()

# set the headers like we are a browser,
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}


def test_urls(urls_requirements, log_file_path):
    if platform.system() == "Darwin":
        ssl._create_default_https_context = ssl._create_unverified_context
    for idx, row in enumerate(urls_requirements):
        u_r_l = row[URL_COLUMN]
        load_time, last_checked, response, check_message = check_url(u_r_l)
        # headers = resp.headers
        if response is not None:
            data = response.read()  # bytes format, need to be decoded
            html = data.decode('UTF-8')

            status_code_message = verify_resp_code(response.code)
            row.append(str(response.code))
            row.append(status_code_message)
            row.append(last_checked)
            row.append(load_time)

            string_to_find = row[REQUIREMENT_STRING_COLUMN]
            if html.find(string_to_find) == -1:
                print(string_to_find, " ----- Not found -----")
                row.append("X")
            else:
                row.append("\u2713")
                print("Found!!")
        else:
            for i in range(5):
                row.append("n/d")
            row[STATUS_MESSAGE] = check_message
    file_menager.write_to_log_file(urls_requirements, log_file_path)
    return urls_requirements


def time_it(func):
    def wrapper(*arg, **kw):
        t1 = datetime.datetime.now() # time.time()
        res, check_message = func(*arg, **kw)
        t2 = datetime.datetime.now()
        time_stamp = datetime.datetime.now().isoformat()
        print(t2-t1, type(t2-t1))
        return str(t2-t1), time_stamp, res, check_message
    return wrapper


@time_it
def check_url(url_):
    resp = None
    req = request.Request(url_)
    message = ""
    try:
        resp = request.urlopen(req)
        message = "-website-reached-"
    except error.HTTPError as err:
        print('The server couldn\'t fulfill the request.')
        print('Server error code: ', err.code)
    except error.URLError as err:
        print('We failed to reach a server.')
        print('Reason: ', err.reason)
        message = err.reason.strerror
    else:
        print('Website reached!')

    return resp, message


def verify_resp_code(status_code):
    if 100 <= status_code < 200:
        return "100x Informational"
    elif 200 <= status_code < 300:
        return "2xx Success"
    elif 300 <= status_code < 400:
        return "3xx Redirection"
    elif 400 <= status_code < 500:
        return "4xx Client Error"
    elif 500 <= status_code < 600:
        return "5xx Server Error"
    else:
        return None


