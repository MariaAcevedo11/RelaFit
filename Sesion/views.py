from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.urls import reverse


class HomePageView(TemplateView):
    
    template_name = "Sesion/home.html"

class SesionPageView(TemplateView):

    template_name = "Sesion/sesion.html"

    