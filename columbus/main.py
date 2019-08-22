# -*- coding: utf-8 -*-
from tests.csv_test import *
from tests.crossvalidation import cross_validation
from config import columbus
from config import basic_config

import json as js
import os
import time
import postprocessing.recommendation_wrapper as wrapper
from recommendationv2 import recommendationv2
from recommendationv1 import recommendationv1

if __name__ == "__main__":
    columbus.current_config = basic_config.ConfigHolder()
    current_config = basic_config.ConfigHolder()
    departure_time = time.time()

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', dest='reimport', default = False,
        action='store_true',
        help = 'Download a new version of events.json file'
    )
    parser.add_argument('-nb', dest='PredictionNumber', default = 2,
        help='Set the maximum number of prediction for each user. Default = 2'
    )

    parser.add_argument('-u', dest='upload', default = False,
        action='store_true',
        help='upload the recommandation.json file to AWS'
    )
    parser.add_argument('-debugging', dest='debugging', default = False,
        action='store_true', help='compute test file'
    )
    parser.add_argument('-o', dest='output',
        action='store', type=str, help='output file name'
    )
    parser.add_argument('-env', dest='environment', default = 'development',
        action='store', type=str,
        help='Webapp Environment (development, test, production, etc.) used for namespacing'
    )
    parser.add_argument('-cv', dest='crossvalidation', default = False,
        action='store_true',
        help='Run the crossvalidation of the selected algorithm'
    )
    parser.add_argument('-v2', dest='version', default = False , # TODO refactor, allow choosing any "v."
        action='store_true',
        help='Choose the version of the algorithm')

    args = parser.parse_args()

    # Set environment
    columbus.current_config['RAILS_ENV'] = args.environment

    # Cleannig Events File
    print('Cleaning files')
    dict_user, dict_pro, data_f = clean(args.reimport)

    # Running recommending algorithm
    print('Computing recommendations')

    if args.version:
        recommendations = recommendationv2.recommend(dict_user, dict_pro, 100, int(args.PredictionNumber))
    else:
        recommendations = recommendationv1.recommend(dict_user, dict_pro, 2, int(args.PredictionNumber))

    # Rendering test file to test if recommendations are coherent
    if args.debugging:
        print('Computing test file')
        render('tests/input.txt', recommendation, dict_user)
    if args.crossvalidation:
        print('Computing Crossvalidation')
        score = cross_validation(dict_user, dict_pro, 50, args.PredictionNumber, args.version)
        print('Crossvalidation score = {0:.2f}'.format(score))
    arrival_time = time.time()
    delta = arrival_time - departure_time

    print('Running time {0:.2f} seconds'.format(delta))

    # Add metadata
    wrapped = wrapper.wrap_with_metadata(recommendations)

    # Uploading file
    local_output_file = os.path.join(columbus.data,'columbus-recommendation.json')
    with open(local_output_file,'w') as f:
        js.dump(wrapped,f, indent = 2,sort_keys=True, separators=(',', ':'),ensure_ascii=False)

    if args.upload:
        data=time.localtime()
        filename = "columbus_recommandation_v1_" + str(data.tm_year) + "_" + str(data.tm_mon) + "_" + str(data.tm_mday) + "_" + str(data.tm_hour) +"_" + str(data.tm_min)+'.json'
        if args.version:
            filename = "columbus_recommandation_v2_" + str(data.tm_year) + "_" + str(data.tm_mon) + "_" + str(data.tm_mday) + "_" + str(data.tm_hour) +"_" + str(data.tm_min)+'.json'
        push_recommendation_file(local_output_file, filename)
    else:
        print('File not uploaded')

