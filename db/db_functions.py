#!/opt/rh/rh-python36/root/usr/bin/python

import sqlite3
import os

def connect_db():

    dbdir = os.environ['HOME'] + '/db'
    anvandare = sqlite3.connect(dbdir + '/hackerator_anvandare.db')
    stamplingar = sqlite3.connect(dbdir + '/hackerator_stamplingar.db')

    return anvandare, stamplingar


def hamta_anvandare(rfid):
    anvandare, stamplingar = connect_db()
    a = anvandare.execute("select * from anvandare where rfid='" + rfid + "'").fetchone()
    if a:
        return {'rfid': a[0], 'kortnummer': a[1], 'fornamn': a[2], 'efternamn': a[3]}
    else:
        return None
    
    
def stampla(kortnummer):
    anvandare, stamplingar = connect_db()
    events = stamplingar.execute("select * from stamplingar where kortnummer='" + kortnummer + "'").fetchall()
    print(events)
