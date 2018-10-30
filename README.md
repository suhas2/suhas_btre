Install Postgres db:
```
brew install postgres
initdb /usr/local/var/postgres
pg_ctl -D /postgres -l /postgres/server.log start

psql postgres -c 'CREATE USER sako WITH PASSWORD 'sako';';
psql postgres -c 'CREATE DATABASE sample_database WITH OWNER sako;";'
```

Migrate db:
```
pip3 install -r requirement.txt
python3 manage.py makemigration
python3 manage.py migrate
python3 manage.py runserver
```
