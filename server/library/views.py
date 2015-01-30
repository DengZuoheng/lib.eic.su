#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django import template
from django.shortcuts import render_to_response
from library.models import Book

# Create your views here.
def collection(request):
    book_list=list(Book.objects.all())
    return render_to_response('collection.html', {'book_list': book_list})