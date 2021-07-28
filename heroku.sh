#!/bin/bash

# To run after each push on Heroku

# 1. Download all fragments from github
bash download.sh

# 2. Migrate
python manage.py migrate

# 3. Delete extrenous data
python manage.py shell -c 'from django.contrib.contenttypes.models import ContentType;ContentType.objects.all().delete()'

# 4. Load data from json
python manage.py loaddata dump_fragments.json

# 5. Collect fragments from github
python manage.py collectstatic
