from flask import Flask, request, render_template, jsonify
from model import MovesDB
from configparser import ConfigParser
import os


config = ConfigParser()
config.read('config/config.ini')
mdb = MovesDB(config['sqlite']['location'])
app = Flask(__name__)


@app.route('/recommend_one', methods=['GET'])
def recommend_one():
    user_id = int(request.args.get('user_id'))
    result = mdb.recommend_one(user_id)
    print(result)
    return '<p> {}   {} </p>'.format(result[0][1], result[0][2]) if result is not None else """
                                                                    <p> There are no user {} </p>""".format(user_id)


@app.route('/recommend', methods=['GET'])
def recommend():
    user_id = int(request.args.get('user_id'))
    n = int(request.args.get('n'))
    result = mdb.recommend(user_id, n)
    data = {r[0]: {'title': r[1], 'genre': r[2]} for r in result}
    return jsonify(data)
    # return render_template('recommend.html', movie_list=result)


@app.route('/add_new_film', methods=['GET', 'POST'])
def add_new_film():
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        genre = request.form.get('genre')
        mdb.add_film(title, year, genre)
        return '''
                <h1>Successful add new film {} ({}) {}</h1>'''.format(title, year, genre)
    return '''
           <form method="POST">
               <div><label>Movie title: <input type="text" name="title"></label></div>
               <div><label>Year: <input type="text" name="year"></label></div>
               <div><label>Genres: <input type="text" name="genre"></label></div>
               <input type="submit" value="Submit">
           </form>'''


@app.route('/')
def index():
    return 'FIRST PAGE'


if __name__ == '__main__':
    app.run(debug=True)
