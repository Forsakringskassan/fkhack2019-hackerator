#!/opt/rh/rh-python36/root/usr/bin/python

import os
import time
from datetime import datetime

import db_functions as db

def stampla(rfid):
    a=db.hamta_anvandare(rfid = rfid)
    #print(a)

    if not a:
        return None, "Fel: Kortet ar inte registrerat."

    status, ts = db.stampla(a['kortnummer'])
    return status, ts

def stamplingar(kortnummer):
    a=db.hamta_anvandare(kortnummer = kortnummer)
    if not a:
        print("Anvandaren finns inte.")

    alla_stamplingar = db.stamplingar(kortnummer)

    return alla_stamplingar

  
