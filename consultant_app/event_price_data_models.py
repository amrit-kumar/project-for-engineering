from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField
import collections

from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import AbstractUser
import uuid
from django.contrib.auth.models import PermissionsMixin
from django import forms
from django.utils import timezone

from versatileimagefield.fields import VersatileImageField,PPOIField
from simple_history.models import HistoricalRecords
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey




class Bookmyshow(models.Model):
    event_name= models.CharField(max_length=500, blank=True, null=True)
    city_name= models.CharField(max_length=500, blank=True, null=True)
    date_time=models.CharField(max_length=500, blank=True, null=True)
    price_data=JSONField(blank=True, null=True, default=collections.OrderedDict())
    venue=models.CharField(max_length=500, blank=True, null=True)
    event_url=models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.event_name

class Eventshigh(models.Model):
    event_name= models.CharField(max_length=500, blank=True, null=True)
    city_name= models.CharField(max_length=500, blank=True, null=True)
    date_time=models.CharField(max_length=500, blank=True, null=True)
    price_data=JSONField(blank=True, null=True, default=collections.OrderedDict())
    venue=models.CharField(max_length=500, blank=True, null=True)
    event_url=models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.event_name


class Goeventz(models.Model):
    event_name= models.CharField(max_length=500, blank=True, null=True)
    city_name= models.CharField(max_length=500, blank=True, null=True)
    date_time=models.CharField(max_length=500, blank=True, null=True)
    price_data=JSONField(blank=True, null=True, default=collections.OrderedDict())
    venue=models.CharField(max_length=500, blank=True, null=True)
    event_url=models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.event_name


class Insider(models.Model):
    event_name= models.CharField(max_length=500, blank=True, null=True)
    city_name= models.CharField(max_length=500, blank=True, null=True)
    date_time=models.CharField(max_length=500, blank=True, null=True)
    price_data=JSONField(blank=True, null=True, default=collections.OrderedDict())
    venue=models.CharField(max_length=500, blank=True, null=True)
    event_url=models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.event_name


class Meraevents(models.Model):
    event_name= models.CharField(max_length=500, blank=True, null=True)
    city_name= models.CharField(max_length=500, blank=True, null=True)
    date_time=models.CharField(max_length=500, blank=True, null=True)
    price_data=JSONField(blank=True, null=True, default=collections.OrderedDict())
    venue=models.CharField(max_length=500, blank=True, null=True)
    event_url=models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.event_name


