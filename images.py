# Transfers the png from disk by filtering according to the database fragment.db

import sqlite3
import os, shutil
import sys

import multiprocessing

if len(sys.argv) != 3:
    print("Usage: python images.py source-dir dest-dir")
    sys.exit(1)

source = sys.argv[1]
destination = sys.argv[2]

pool = multiprocessing.Pool()

con = sqlite3.connect("fragment.db")
cursor = con.cursor()

# copy fragments
def copy_fragments(row):
    kind, number, model = row

    filename = f"{model}_{kind}{number}.png"

    shutil.copyfile(os.path.join(source, filename), os.path.join(destination, filename))

row = cursor.execute('SELECT kind, number, model FROM fragments')
pool.map(copy_fragments, row)

# copy models
for model, class_count in cursor.execute('SELECT name, classes FROM models'):
    if int(class_count) == 0:
        continue
    filename = f"{model}.png"

    shutil.copyfile(os.path.join(source, filename), os.path.join(destination, filename))

con.close()