#!/usr/bin/env python3

import sqlite3
import os
import time

def connect_db():

    dbdir = os.environ['HOME'] + '/db'
    anvandare = sqlite3.connect(dbdir + '/hackerator_anvandare.db')
    stamplingar = sqlite3.connect(dbdir + '/hackerator_stamplingar.db')

    return anvandare, stamplingar


def hamta_anvandare(rfid = None, kortnummer = None):
    anvandare, stamplingar = connect_db()

    if rfid is not None:
        a = anvandare.execute("select * from anvandare where rfid='" + rfid + "'").fetchone()
    else:
        a = anvandare.execute("select * from anvandare where kortnummer=" + kortnummer).fetchone()
    if a:
        return {'rfid': a[0], 'kortnummer': a[1], 'fornamn': a[2], 'efternamn': a[3]}
    else:
        return None



def stampla(kortnummer):
    # Stamplar in. typ: 1=in, 0=ut
    anvandare, stamplingar = connect_db()
    last_event = stamplingar.execute("select * from stamplingar where kortnummer=" + str(kortnummer) + " order by tid desc limit 1").fetchone()
    #print(last_event)


    new_ts = int(time.time())

    if not last_event:
        # Dagens forsta instampling
        new_status = 1
    else:
        last_status = last_event[2]
        #Stampling finns for den har dagen. Kollar status
        if last_status == 0:
            new_status = 1
        else:
            new_status = 0

    stamplingar.execute("insert into stamplingar values(" + str(kortnummer) + "," + str(new_ts) + "," + str(new_status) + ");")
    stamplingar.commit()

    return new_status, new_ts


def stamplingar(kortnummer):
    anvandare, stamplingar = connect_db()

    alla_stamplingar = list()
    data = stamplingar.execute("select * from stamplingar order by tid").fetchall()
    for row in data:
        alla_stamplingar.append({'kortnummer': row[0], 'tid': row[1], 'status': row[2]})
    return alla_stamplingar
