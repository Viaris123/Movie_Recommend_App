import logging
import scipy.sparse as sparse
import implicit
import numpy as np
from component.sqlite_core import SQLiteCore
import joblib


class RatingPredict:

    def __init__(self, db_location):
        self._sql_core = SQLiteCore(db_location)
        self._scr_item_user = joblib.load('recsys/data/item_user.sav')
        self._scr_user_item = joblib.load('recsys/data/user_item.sav')
        self.model = joblib.load('recsys/data/finalized_model.sav')

    def predict_one(self, user_id, debug=False):
        try:
            recommend = self.model.recommend(user_id, self._scr_user_item[user_id],
                                             filter_already_liked_items=False,
                                             N=1)
            recommended_list = recommend[0].tolist()
        except IndexError:
            logging.debug(f'There are no user with "User_id" {user_id}')
            return None
        if debug:
            print(recommended_list)
        get_recommended_query = """SELECT * FROM movies WHERE movieId == {}""".format(recommended_list[0])
        result = self._sql_core.select(get_recommended_query)
        if debug:
            print(result[0][1], result[0][2])
        return result

    def predict(self, user_id, number_of_films=10, debug=False):
        """Return N films, that could be liked by user."""
        recommend = self.model.recommend(user_id, self._scr_user_item[user_id],
                                         filter_already_liked_items=False,
                                         N=number_of_films)

        if debug:
            print(recommend)

        recommended_list = recommend[0].tolist()

        # Get titles from Data Base
        get_recommended_query = """SELECT * FROM movies WHERE movieId IN {}""".format(tuple(recommended_list))
        result = self._sql_core.select(get_recommended_query)

        if debug:
            print(f"For user {user_id}, I recommend to watch:\n")
            for movie in result:
                print(f"{movie[1]} {movie[2]}")

        return result
