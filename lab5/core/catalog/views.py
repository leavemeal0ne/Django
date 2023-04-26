from django.shortcuts import render
from .sources import data
# Create your views here.

def index(request):
    """

    """
    return  render(request,'index.html')

def apartments(request):
    """

    """
    return  render(request,'goods.html',context={'data':data})

def additions(request):
    """

    """
    return  render(request,'additions.html')

def contacts(request):
    """

    """
    return  render(request,'contacts.html')
