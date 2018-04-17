# This Python file uses the following encoding: utf-8
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
        ('a', 'Produção de Áudio'),
        ('i', 'Ilustração'),
        ('v', 'Produção e/ou Edição de Vídeo'),
        ('f', 'Fotografia'),
        ('w', 'Criação de Website'),
        ('d', 'Registrar Domínio'),
        ('l', 'Logotipo'),
    )

IDIOMAS = (
    ('en', 'English'),
    ('es', 'Español'),
    ('fr', 'Français'),
    ('it', 'Italiano'),
    ('pt', 'Português'),
    ('ro', 'Roumain'),
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
