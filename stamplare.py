#!/opt/rh/rh-python36/root/usr/bin/python

import os
import db_functions as db


a=db.hamta_anvandare('123,345,456,566')
print(a)

db.stampla(a['kortnummer'])
