<!-- TODO(1879352a-24dd-4639-8a78-5f677ec1590f): rename spendings -> expenses. Spending doesn't have plural form -->

# Spendings Sqlite Migration

I've been tracking all of my spendings since 07.06.2016 in a couple of
org-mode files with a table. The "database" has 750+ records. I wanna
migrate all of that to sqlite.

## Usage ##

    Usage: migrate.py <csv-file-spendings> <csv-file-places> <sqlite-output-file>
