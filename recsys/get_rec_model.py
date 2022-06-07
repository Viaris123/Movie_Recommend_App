import scipy.sparse as sparse
import implicit
import numpy as np
import pandas as pd
from component.sqlite_core import SQLiteCore
import joblib
from configparser import ConfigParser


class PredictModel:

    def __init__(self, db_location):
        self._sql_core = SQLiteCore(db_location)
        self._scr_item_user, self._scr_user_item = self._set_scr_matrix()
        self.model = implicit.als.AlternatingLeastSquares(factors=20, regularization=0.01, iterations=20, num_threads=5)
        self._fit()

    def _prepare_data(self):
        """ Get data from DB and convert it to Data Frame"""

        select_query = """SELECT userId, movieId, rating FROM ratings;"""
        ratings = self._sql_core.select(select_query)

        data = pd.DataFrame(ratings, columns=['user_id', 'movie_id', 'rating'])
        return data

    def _fit(self):
        # Configure and train our model
        data_conf = (self._scr_item_user * 40).astype('double')
        self.model.fit(data_conf)

    def _set_scr_matrix(self):
        data = self._prepare_data()

        # Get matrix from users and items
        scr_item_user = sparse.csr_matrix((data['rating'], (data['movie_id'], data['user_id'])))
        scr_user_item = sparse.csr_matrix((data['rating'], (data['user_id'], data['movie_id'])))
        return scr_item_user, scr_user_item

    def get_user_item_matrix(self):
        return self._scr_user_item

    def get_item_user_matrix(self):
        return self._scr_item_user

    def get_model(self):
        return self.model


def main():
    config = ConfigParser()
    config.read(r'config/config.ini')
    prm = PredictModel(config['sqlite']['location'])
    joblib.dump(prm.get_model(), 'recsys/data/finalized_model.sav')
    joblib.dump(prm.get_user_item_matrix(), 'recsys/data/user_item.sav')
    joblib.dump(prm.get_item_user_matrix(), 'recsys/data/item_user.sav')


if __name__ == '__main__':
    main()
