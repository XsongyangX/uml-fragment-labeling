#!/bin/bash

# downloads and unzips the images for static delivery of fragments

# images only tar at
# https://github.com/XsongyangX/uml-class-fragmentation/releases/download/v1.0/images.tar.bz2

wget https://github.com/XsongyangX/uml-class-fragmentation/releases/download/v1.0/images.tar.bz2
mkdir -p labeling/static/fragments
tar -xjf images.tar.bz2 --directory labeling/static/fragments
mv labeling/static/fragments/to_be_labeled/*.png labeling/static/fragments/
rmdir labeling/static/fragments/to_be_labeled