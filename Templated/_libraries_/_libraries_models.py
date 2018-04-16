# This Python file uses the following encoding: utf-8

"""
Model Libraries
Written by Leo Neto
Updated on April 14, 2018
"""

from __future__ import unicode_literals
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse
from datetime import date
from _libraries_choices import *
from cloudinary.models import CloudinaryField
