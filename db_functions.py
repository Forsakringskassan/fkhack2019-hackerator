#!/usr/bin/env python3


import sqlite3
import os
import time
from datetime import datetime

def connect_db():

    dbdir = os.environ['HOME'] + '/db/'
    anvandare_fil = dbdir + '/hackerator_anvandare.db'
    stamplingar_fil = dbdir + '/hackerator_stamplingar.db'

    if not os.path.exists(dbdir):
        os.makedirs(dbdir)

    if not os.path.isfile(anvandare_fil):
        # Skapa databasen anvandare
        anvandare = sqlite3.connect(anvandare_fil)
        anvandare.execute("create table anvandare(rfid text, kortnummer text, fornamn text, efternamn text);")
        anvandare.execute("insert into anvandare values ('1234', '40043907', 'Fredrik', 'W');")
        anvandare.commit()
    else:
        anvandare = sqlite3.connect(anvandare_fil)

    if not os.path.isfile(stamplingar_fil):
        # Skapa databasen stamplingar
        stamplingar = sqlite3.connect(dbdir + '/hackerator_stamplingar.db')
        stamplingar.execute("create table stamplingar(kortnummer text, tid real, typ int);")
    else:
        stamplingar = sqlite3.connect(dbdir + '/hackerator_stamplingar.db')

    return anvandare, stamplingar


def hamta_anvandare(rfid = None, kortnummer = None):
    anvandare, stamplingar = connect_db()


    if rfid is not None:
        a = anvandare.execute("select * from anvandare where rfid='" + rfid + "'").fetchone()
    else:
        a = anvandare.execute("select * from anvandare where kortnummer='" + str(kortnummer) + "'").fetchone()
    if a:
        return {'rfid': a[0], 'kortnummer': a[1], 'fornamn': a[2], 'efternamn': a[3]}
    else:
        return None


def lista_anvandare():
    anvandare, stamplingar = connect_db()
    a = anvandare.execute("select * from anvandare order by efternamn, fornamn").fetchall()
    anvandare = list()
    for row in a:
        print(row)
        anvandare.append({'rfid': row[0], 'kortnummer': row[1], 'fornamn': row[2], 'efternamn': row[3]})
    return anvandare


def skapa_anvandare(rfid, kortnummer, fornamn, efternamn):
    anvandare, stamplingar = connect_db()
    if anvandare.execute("select count(*) from anvandare where kortnummer='" + str(kortnummer) + "'").fetchone()[0] != 0:
        print("Anvandare med kortnummer " + kortnummer + " finns redan.")
        return False
    if anvandare.execute("select count(*) from anvandare where rfid='" + rfid + "'").fetchone()[0] != 0:
        print("Anvandare med RFID-kort " + rfid + " finns redan.")
        return False

    anvandare.execute("insert into anvandare values('" + rfid + "','" + str(kortnummer) + "','" + fornamn + "','" + efternamn + "')")
    anvandare.commit()
    return True


def stampla(kortnummer):
    # Stamplar in. typ: 1=in, 0=ut
    anvandare, stamplingar = connect_db()
    last_event = stamplingar.execute("select * from stamplingar where kortnummer='" + str(kortnummer) + "' order by tid desc limit 1").fetchone()
    #print(last_event)


    new_ts = time.time()
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

    stamplingar.execute("insert into stamplingar values('" + str(kortnummer) + "'," + str(new_ts) + "," + str(new_status) + ");")
    stamplingar.commit()
    new_date = datetime.utcfromtimestamp(new_ts).strftime('%Y-%m-%d %H:%M:%S')
    return {'status': new_status, 'tid': new_ts, 'datum': new_date}


def stamplingar(kortnummer = None, antal = 10):
    anvandare, stamplingar = connect_db()

    alla_stamplingar = list()
    if kortnummer is None:
        data = stamplingar.execute("select * from stamplingar order by tid desc limit " + str(antal)).fetchall()
    else:
        data = stamplingar.execute("select * from stamplingar where kortnummer='" + str(kortnummer) + "' order by tid desc limit" + antal).fetchall()
    for row in data:
        datum = datetime.utcfromtimestamp(row[1]).strftime('%Y-%m-%d %H:%M:%S')

        alla_stamplingar.append({'kortnummer': row[0], 'tid': row[1], 'status': row[2], 'datum': datum})
    return alla_stamplingar

