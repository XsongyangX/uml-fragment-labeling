#!/bin/bash

# downloads and unzips the images for static delivery of fragments

# images only tar at
# https://github.com/XsongyangX/uml-class-fragmentation/releases/download/v1.0/images.tar.bz2

wget https://github.com/XsongyangX/uml-class-fragmentation/releases/download/v1.0/images.tar.bz2
mv images.tar.bz2 static/fragments/
tar -xjf static/fragments/images.tar.bz2