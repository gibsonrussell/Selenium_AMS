# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 07:40:53 2020

@author: GibsonRussell
"""


### General Imports ###
import os
import json
import pandas as pd
import pathlib
import sys

### User Modules ###
from Test_Scripts import *

def datetime_handler(x):
    """Purpose:  To handle times in writing out to JSON file
        Args:
            x (datetime.datetime Obj.):  The time we want to capture in JSON
        Returns:
            Unknown Type.
    """
    """Used to handle times for writing out to JSON"""
    import datetime
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

def save_to_json(dct):
    """Purpose:  To write out data to JSON file.
        Args:
            dct (Dictionary):  Dictionary representing the data we want to write out
        Returns:
            None.
    """
    ### Location to store
    path = pathlib.Path(__file__).parent.absolute() / "Data" / "JS" / "populate.json"

    with open(str(path), 'w') as f:
        json.dump(d, f, ensure_ascii = False, default = datetime_handler)



### Define Paths ###
var_path = pathlib.Path(__file__).parent.absolute() / "Variables"
py_path = pathlib.Path(__file__).parent.absolute() / "Test_Scripts"
var_files = os.listdir(var_path)
py_files = os.listdir(py_path)

### Remove Variables ###
d = {}
for file in var_files:
    full_path = var_path / file
    df = pd.read_excel(full_path)
    key = "AMS Ticket " + str(file).split(".")[0]
    d[key] = {df.loc[i, "Variable"] : df.loc[i, "Value"] for i in df.index.tolist()}

### Get Import Modules ###
imp_modules = [sys.modules[mod] for mod in sys.modules.keys() 
               if str(mod).split(".")[0] == "Test_Scripts"
               and str(mod) != "Test_Scripts"]

attr_dct = {}
for mod in imp_modules:
    execute_class = mod.execute
    description_class = mod.Description
    attr_dct[mod.Description.display()] = {"Display Name" : mod.Description.display(), \
                                           "Description" : mod.Description.description(),
                                           "Variables" : d[mod.Description.display()]}

save_to_json(attr_dct)

#path = str(pathlib.Path(p.parents[0]))


