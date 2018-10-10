# Django Template

### Setup database
```
$ sudo su - postgres
$ psql
# CREATE USER django_template WITH SUPERUSER ENCRYPTED PASSWORD 'django_template';
# CREATE DATABASE django_template WITH OWNER 'django_template';
# \q
```

### Apply django migrations
```
python manage.py migrate
```