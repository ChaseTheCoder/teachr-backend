from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# takes a request and returns a response
# more of a 'request handler'

def say_hello(request):
  return render(request, 'hello.html', { 'name': 'chase'})