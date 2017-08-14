# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils import timezone

class path_deploy(models.Model):
    name_service = models.CharField(max_length=200)
    base_dir = models.CharField(max_length=200)
    ip_server = models.CharField(max_length=200,default="192.168.1.101")
# Create your models here.
