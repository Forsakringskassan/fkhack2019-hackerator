#!/usr/bin/env python3

import os
import sys
import time
from datetime import datetime

import db_functions as db
import stamplare as stamplare

def usage():
    print("Usage:")
    print(sys.argv[0] + " stampla <rfid>")
    print(sys.argv[0] + " status <kortnummer>")
    sys.exit(1)

if len(sys.argv) < 3:
    usage()

action = sys.argv[1]
data = sys.argv[2]

#print("A: " + action)
#print("D: " + data)

if action == 'stampla':
    status, ts = stamplare.stampla(data)
    if status is None:
        print(ts)
    else:
        print("Resultat fran stampling:")
        date = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        if status == 0:
            print("Du blev utstamplad " + date)
        else:
            print("Du blev instamplad " + date)


elif action == 'stamplingar':
    stamplingar = stamplare.stamplingar(data)
    for row in stamplingar:
        date=datetime.utcfromtimestamp(row['tid']).strftime('%Y-%m-%d %H:%M:%S')
        if row['status'] == 0:
            status = "UT"
        else:
            status = "IN"

        print(date + ": " + status)

elif action == 'anvandare':
    user = db.hamta_anvandare(kortnummer = data)
    print("Fornamn:           " + user['fornamn'])
    print("Efternamn:         " + user['efternamn'])
    print("FK-kortnummer:     " + str(user['kortnummer']))
    print("RFID-kortnummer:   " + user['rfid'])

else:
    usage()

