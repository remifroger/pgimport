# pgimport

Importe dans une base un schéma d'une BDD PostgreSQL l'ensemble des fichiers CSV et SHP d'un dossier.

Nécessite l'installation de QGIS (ogr2ogr) et PostgreSQL (psql).

## Pré-requis

Remplir les variables d'environnement (.env).

## Usage

```
python main.py "path\to\dir" schema
```

Par exemple, la commande ci-dessous va importer l'ensemble des CSV et SHP du dossier tests (C:\Users\frog\OneDrive - Projet\data\tests) dans le schéma "schema_import".

```
python main.py "C:\Users\frog\OneDrive - Projet\data\tests" schema_import
```

Attention, bien veiller à mettre le chemin du dossier entre guillemets.