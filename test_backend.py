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
    result = stamplare.stampla(data)
    if result['status'] is None:
        print(result['fel'])
    else:
        print("Resultat fran stampling:")
        if result['status'] == 0:
            print("Du blev utstamplad " + result['datum'])
        else:
            print("Du blev instamplad " + result['datum'])


elif action == 'stamplingar':
    stamplingar = stamplare.stamplingar(data)
    for row in stamplingar:
        if row['status'] == 0:
            status = "UT"
        else:
            status = "IN"

        print(row['datum'] + " (" + str(row['tid']) + "): " + status)

elif action == 'anvandare':
    if data == 'alla':
        anvandare = db.lista_anvandare()
        n = 1
        for a in anvandare:
            print("Anvandare #" + str(n))
            print("    Fornamn:           " + a['fornamn'])
            print("    Efternamn:         " + a['efternamn'])
            print("    FK-kortnummer:     " + str(a['kortnummer']))
            print("    RFID-kortnummer:   " + a['rfid'])
            n += 1
    else:
        user = db.hamta_anvandare(kortnummer = data)
        print(user)
        print("Fornamn:           " + user['fornamn'])
        print("Efternamn:         " + user['efternamn'])
        print("FK-kortnummer:     " + str(user['kortnummer']))
        print("RFID-kortnummer:   " + user['rfid'])

elif action == 'skapa':
    if len(sys.argv) < 6:
        usage()

    kortnummer = sys.argv[3]
    fornamn = sys.argv[4]
    efternamn = sys.argv[5]
    print("Fornamn:           " + fornamn)
    print("Efternamn:         " + efternamn)
    print("FK-kortnummer:     " + str(kortnummer))
    print("RFID-kortnummer:   " + data)
    result = db.skapa_anvandare(rfid = data, kortnummer = kortnummer, fornamn = fornamn, efternamn = efternamn)
    print("R:")
    print(result)


else:
    usage()

