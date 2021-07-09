# Django project of the labeling process of UML fragments
A UML fragment is a portion of a UML class diagram. The label is a English text description.

## Getting Started
This will run the website on your own computer.

### Installation
To run this locally, you need:
* [django](https://docs.djangoproject.com/en/3.2/topics/install/) : Version 3+
* Python 3+
* A Bash interpreter like Git Bash or Cygwin
* wget: a GNU command for downloading files

### Collect data
To collect the data into the repo, use `download.sh`. 
```bash
./download.sh
```
This will download a zip from another repo and unzip it in `labeling/static/fragments/`. About 9000 images totaling 200 MB will be available.

### Run a local server
At the root of the repo, run in the command line
```bash
python manage.py migrate
python manage.py runserver
```
A message like this will print. Access the website via the IP address [`http://127.0.0.1:8000/`](http://127.0.0.1:8000/).
```bash
$ python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
July 09, 2021 - 10:15:20
Django version 3.2.4, using settings 'umllabels.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
> You only need to `migrate` once. After that, you can just use `runserver`.

## Non-django files
* `images.py`: Copies relevant images from the raw fragment folder to the django static folder
* `fragment.db`: Original SQLite database of the file names of models and fragments
* `download.sh`: Downloads the archive of images from the internet and extracts it in the correct folder.