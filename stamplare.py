#!/opt/rh/rh-python36/root/usr/bin/python

import os
import time
from datetime import datetime

import db_functions as db

def stampla(rfid):
    a=db.hamta_anvandare(rfid = rfid)
    #print(a)

    if not a:
        return {'status': None, 'fel': "Fel: Kortet ar inte registrerat."}

    resultat = db.stampla(a['kortnummer'])
    return resultat


def stamplingar(kortnummer):
    a=db.hamta_anvandare(kortnummer = kortnummer)
    if not a:
        print("Anvandaren finns inte.")

    alla_stamplingar = db.stamplingar(antal=13)

    return alla_stamplingar

  
