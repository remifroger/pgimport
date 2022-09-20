#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import sys
from dotenv import load_dotenv
load_dotenv()

PGHOST = os.getenv('PGHOST')
PGPORT = os.getenv('PGPORT')
PGUSER = os.getenv('PGUSER')
PGPWD = os.getenv('PGPWD')
PGDB = os.getenv('PGDB')
PGBINPATH = os.getenv('PGBINPATH')
QGISBINPATH = os.getenv('QGISBINPATH')

if PGHOST == "" or PGPORT == "" or PGUSER == "" or PGPWD == "" or PGDB == "" or QGISBINPATH == "":
    print('Renseignez les variables d\'environnement du fichier .env')
    exit()

if not os.path.exists(QGISBINPATH):
    print('Le chemin vers les binaires QGIS n\'existe pas (exemple : C:\Program Files\QGIS X.XX\bin)')
    exit()

if not os.path.exists(PGBINPATH):
    print('Le chemin vers les binaires PostgreSQL n\'existe pas (exemple : C:\Program Files\PostgreSQL\14\bin)')
    exit()

inputDirectory = sys.argv[1]
pgSchema = sys.argv[2]

os.chdir(PGBINPATH)
print('Création du schéma {0}'.format(pgSchema))
SQLQUERYSCHEMA = ("CREATE SCHEMA IF NOT EXISTS " + pgSchema + ";")
try: 
    subprocess.check_call(['psql', '-U', PGUSER, '-h', PGHOST, '-p', PGPORT, '-d', PGDB, '-c', '{}'.format(SQLQUERYSCHEMA)])
    print('Schéma créé')
except subprocess.CalledProcessError as e:
    print(e.output)

os.chdir(QGISBINPATH)
for file in os.listdir(inputDirectory):
    pathfile = os.path.join(inputDirectory, file)
    if (file.endswith(".csv") or file.endswith(".shp")) and os.path.isfile(pathfile):
        try:
            print('Import de {0}'.format(pathfile))
            subprocess.check_call(['ogr2ogr', '-f', 'PostgreSQL', "PG:host={0} port={1} dbname={2} user={3} password={4}".format(PGHOST, PGPORT, PGDB, PGUSER, PGPWD), "{0}".format(pathfile), '-lco', 'OVERWRITE=yes', '-nln', '{0}.{1}'.format(pgSchema, file)])
            print('Importé')
        except subprocess.CalledProcessError as e:
            print(e.output)
print('Terminé')