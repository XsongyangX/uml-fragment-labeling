# Django project of the labeling process of UML fragments
A UML fragment is a portion of a UML class diagram. The label is a English text description.

## Non-django files
* images.py: Copies relevant images from the raw fragment folder to the django static folder
* fragment.db: Original SQLite database of the file names of models and fragments
* static/fragments/images.tar.bz2: Tar archive of the 5k images. Must be extracted in the same folder to be deployed.
* download.sh: Downloads the archive of images from the internet and extracts it in the correct folder.