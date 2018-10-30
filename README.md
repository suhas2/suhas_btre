Install Postgres db:
```
brew install postgres
initdb /usr/local/var/postgres
pg_ctl -D /postgres -l /postgres/server.log start

psql postgres -c 'CREATE USER sako WITH PASSWORD 'sako';';
psql postgres -c 'CREATE DATABASE sample_database WITH OWNER sako;";'
```

!!!Add your SOCIAL_AUTH_GOOGLE_OAUTH2_KEY and SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET in settings.py!!!
```
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY =''  #Paste CLient Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '' #Paste Secret Key
```

Migrate db:
```
pip3 install -r requirement.txt
python3 manage.py makemigration
python3 manage.py migrate
python3 manage.py runserver
```
