from flask import Flask, render_template, request, escape, session
import vsearch
from DBcm import UseDatabase
from checker import check_logged_in
app = Flask(__name__)

app.config['dbconfig'] = {'host': '127.0.0.1',
                'user': 'vsearch',
                'password': 'vsearchpasswd',
                'database': 'vsearchlogDB',
                'port': '5432'}


def log_request(req: 'flask_request', res: str) -> None:

    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """INSERT INTO log 
        (phrase, letters, ip, browser_string, results)
        values 
        (%s, %s, %s, %s, %s);"""
        cursor.execute(_SQL, (req.form['phrase'],
                              request.form['letters'],
                              req.remote_addr,
                              str(req.user_agent).split('/')[0],
                              res, ))


@app.route('/search4', methods=['POST'])
@check_logged_in
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
@check_logged_in
def view_the_log() -> 'html':
    with UseDatabase(app.config['dbconfig']) as cursor:
        _SQL = """ select phrase, letters, ip, browser_string, results from log"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
    row_titles = ('Phrase', 'Letters', 'Remote addr', 'User agent', 'Results')
    return render_template('viewlog.html', the_title='View Log', the_row_titles=row_titles, the_data=contents)


@app.route('/login')
def do_logout() -> str:
    session['logged_in'] = True
    return 'You are now logged in'


@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are now logged out'


app.secret_key = 'You will never guess'

if __name__ == '__main__':
    app.run(debug=True)




