### Django-Autogenerator

"""
Model Choices
Written by Leo Neto
Updated on April 14, 2018
"""

from __future__ import unicode_literals
from django.db import models
from datetime import date


STATUS_CHOICES = (
    ('d', 'Draft'),
    ('p', 'Published'),
)

MESSAGE_STATUS = (
    ('u', 'Unread'),
    ('r', 'Read'),
    ('c', 'Replied'),
    ('t', 'Trashed'),
    ('s', 'Spam'),
)

MESSAGE_CHOICES = (
        ('a', 'Production'),
        ('i', 'Illustration'),
        ('v', 'Video'),
        ('p', 'Photography'),
        ('w', 'Website'),
        ('d', 'Domain'),
        ('l', 'Logos'),
    )

IDIOMAS = (
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('it', 'Italian'),
    ('pt', 'Portuguese'),
    ('ro', 'Romanian'),
)

TOPIC_CHOICES  = (
       ('N', 'News'),
       ('T', 'Technology'),
       ('A', 'Audio'),
       ('V', 'Video'),
       ('S', 'Science'),
       ('P', 'Programming'),
       ('G', 'General'),
       ('C', 'Culture'),
       ('R', 'Religion'),
       ('W', 'Web'),
    )
