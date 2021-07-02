from django.db import models

# Create your models here.
class Fragments(models.Model):
    kind = models.CharField(max_length=50)
    number = models.IntegerField(blank=True, null=True)
    model = models.ForeignKey('Models', models.DO_NOTHING, db_column='model', blank=True, null=True)       
    unique_id = models.AutoField(primary_key=True, blank=True, null=False, default=0)


class Models(models.Model):
    name = models.CharField(primary_key=True, blank=True, null=False, max_length=50)
    classes = models.IntegerField(blank=True, null=True)
    relations = models.IntegerField(blank=True, null=True)

class Label(models.Model):
    label = models.TextField()
    fragment = models.ForeignKey('Fragments', models.DO_NOTHING)