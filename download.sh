#!/bin/bash

# downloads and unzips the images for static delivery of fragments

# images only tar at
# https://github.com/XsongyangX/uml-class-fragmentation/releases/download/v1.0/images.tar.bz2

wget https://github.com/XsongyangX/uml-class-fragmentation/releases/download/v1.0/images.tar.bz2
mkdir -p labeling/static/fragments
mv images.tar.bz2 labeling/static/fragments/
tar -xjf labeling/static/fragments/images.tar.bz2