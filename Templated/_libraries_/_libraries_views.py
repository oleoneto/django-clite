### Django-Autogenerator

"""
Views Libraries
Written by Leo Neto
Updated on April 14, 2018
"""

from __future__ import unicode_literals

# HTTP Handling and Routing...
from django.http import HttpRequest, Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# System Authentication
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

# Forms
from django import forms

# System Views...
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DeleteView, DetailView
from django.shortcuts import get_object_or_404

# REST API Imports...
from rest_framework import routers, serializers, viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
