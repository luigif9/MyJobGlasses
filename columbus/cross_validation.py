import os
import json as js
import time
import matplotlib.pyplot as plt
import numpy as np

from cleaning.cleaning import clean, export_history_file
from tests.crossvalidation import cross_validation


if __name__ == "__main__":
    departure_time = time.time()

    # Cleaning Events File and outputing the history for cross_validation
    print('Cleaning files')
    dict_user, dict_pro, data_f = clean(False)

    score = cross_validation(dict_user, dict_pro, 10, 2)
    print("The score given by the cross-validation is {:.1f} %".format(score*100))
    print("The closer the score is to 1, the better the predictions are")
    arrival_time = time.time()
    delta = arrival_time - departure_time
    print("Cross validation executed in {:.1f} seconds".format(delta))