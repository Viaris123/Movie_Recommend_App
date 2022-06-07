from component.sqlite_core import SQLiteCore
from recsys import rating_predict as rp
import datetime
from configparser import ConfigParser


class MovesDB(SQLiteCore):

    def __init__(self, db_location):
        super().__init__(db_location)
        self._predict_model = rp.RatingPredict(db_location)

    def select_user_film_rating(self, user_id, movie_id):
        query = 'SELECT rating FROM ratings WHERE userId == {} AND movieId == {};'.format(user_id, movie_id)
        result = self.select(query)
        return result[0][0]

    def select_movie_name(self, movie_id):
        query = """SELECT title FROM movies WHERE movieId == {}""".format(movie_id)
        result = self.select(query)
        return result[0][0]

    def select_movie_genre(self, movie_id):
        query = """SELECT genres FROM movies WHERE movieId == {};""".format(movie_id)
        result = self.select(query)
        return result[0][0]

    def update_rating_for_movie(self, user_id, movie_id, rating):
        query = """UPDATE ratings SET rating = {} 
        WHERE userId == {} AND movieId == {};""".format(rating, user_id, movie_id)
        self.update(query)

    def add_rating_for_user(self, rating, movie_id, user_id):
        timestamp = datetime.datetime.utcnow().timestamp()
        query = """INSERT INTO ratings (userId, movieId, rating, timestamp) 
        VALUES ({}, {}, {}, {})""".format(user_id, movie_id, rating, timestamp)
        self.insert(query)

    def add_film(self, name, year, genre):
        get_last_id_query = """SELECT MAX(movieId) FROM movies"""
        new_id = self.select(get_last_id_query)[0][0] + 1
        title = '{} ({})'.format(name, year)
        insert_query = """INSERT INTO movies (movieId, title, genres) VALUES ({},'{}','{}');""".format(new_id, title,
                                                                                                       genre)
        self.insert(insert_query)

    def recommend(self, user_id, n=10):
        return self._predict_model.predict(user_id, number_of_films=n, debug=False)

    def recommend_one(self, user_id):
        return self._predict_model.predict_one(user_id, debug=False)


def main():
    config = ConfigParser()
    config.read('config/config.ini')
    mdb = MovesDB(config['sqlite']['location'])
    # print(mdb.select_user_film_rating(555, 1320))
    # print(mdb.select_movie_name(1320))
    # mdb.update_rating_for_movie(555, 1320, 3.0)
    # print(mdb.select_movie_genre(1320))
    # print(mdb.select_user_film_rating(555, 1320))
    # mdb.add_film('Afro Samurai', 2005, 'Action|Drama|Animation')
    # mdb.recommend(2)
    # mdb.recommend(610)
    # mdb.recommend(619)
    print(mdb.recommend(619))
    print(mdb.recommend_one(2), mdb.recommend_one(3))
    del mdb


if __name__ == '__main__':
    main()
