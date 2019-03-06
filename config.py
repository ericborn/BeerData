# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 09:04:27 2019

@author: Eric Born
Config function that will read our database.ini file which contains the connection string information for the database
"""
from configparser import ConfigParser
  
def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
 
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
 
    return db