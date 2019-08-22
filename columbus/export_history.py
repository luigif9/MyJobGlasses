import os
import json as js

from cleaning.cleaning import clean, export_history_file

if __name__ == "__main__":
    # Cleannig Events File
    print('Cleaning files')
    dict_user, dict_pro, data_f = clean(False)

    print('Exporting history file')
    export_history_file(dict_user)