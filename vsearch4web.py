from flask import Flask, render_template, request, escape
import vsearch
import psycopg2
from psycopg2 import Error
app = Flask(__name__)


def log_request(req: 'flask_request', res: str) -> None:
    dbconfig = {'host': '127.0.0.1',
                'user': 'vsearch',
                'password': 'vsearchpasswd',
                'database': 'vsearchlogDB',
                'port': '5432'}
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(**dbconfig)

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        _SQL = """INSERT INTO log 
        (phrase, letters, ip, browser_string, results)
        values 
        (%s, %s, %s, %s, %s);"""
        cursor.execute(_SQL, (req.form['phrase'],
                              request.form['letters'],
                              req.remote_addr,
                              str(req.user_agent).split('/')[0],
                              res, ))
        connection.commit()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    phrase = request.form['phrase']
    letters = request.form['letters']
    result = str(vsearch.search4letters(phrase, letters))
    log_request(request, result)
    return render_template('results.html', the_title='Results:', the_phrase=phrase,
                           the_letters=letters, the_results=result)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome!')


@app.route('/viewlog')
def view_the_log() -> 'html':
    contents = []
    row_titles = ('Form Data', 'Remote addr', 'User agent', 'Results')
    with open('vsearch.log') as log:
        for lg in log:
            contents.append([])
            for elem in (lg.split(' || ')):
                contents[-1].append(escape(elem))
        return render_template('viewlog.html', the_title='View Log', the_row_titles=row_titles, the_data=contents)


if __name__ == '__main__':
    app.run(debug=True)




