#!/bin/sh

DBDIR=$HOME/hackerator/db


sqlite3 $DBDIR/hackerator_anvandare.db "create table anvandare(rfid text, kortnummer int, fornamn text, efternamn text);"
sqlite3 $DBDIR/hackerator_anvandare.db "insert into anvandare values ('101 102 103 104', '40043907', 'Fredrik', 'W');"

sqlite3 $DBDIR/hackerator_stamplingar.db "create table stamplingar(kortnummer int, tid int, typ int);"

