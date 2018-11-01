Install Postgres db:
```
brew install postgres
initdb /usr/local/var/postgres
pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start

psql postgres -c 'CREATE USER postgres WITH PASSWORD '123456';';
psql postgres -c 'CREATE DATABASE btredb WITH OWNER postgres;";'
```

- Go to the [Google Google Developers](https://console.developers.google.com/apis/library?project=_) Console and create a project.

- Create OAuth client ID for Web Application under Credentials menu.

- Enter the following URI's in Authorized redirect URIs
```
http://localhost:8000/auth/complete/google-oauth2/
http://127.0.0.1:8000/auth/complete/google-oauth2/
```

- Under the APIs and services tab, search for Google+ API and Gmail API and enable them.

!!!Add your SOCIAL_AUTH_GOOGLE_OAUTH2_KEY and SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET in settings.py!!!
```
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY =''  #Paste CLient Key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '' #Paste Secret Key
```

Migrate db:
```
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```
