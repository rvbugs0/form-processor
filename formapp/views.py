from django.shortcuts import render
from django.http import HttpResponse

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .Hello import return_hello_message
# Create your views here.
from .form_processor import execute

import os
here = os.path.dirname(os.path.abspath(__file__))
oneup = ".."


def print_hello_message(request):
    msg = return_hello_message()
    response = "{'message':'"
    response += msg
    response+= "'}"
    return HttpResponse(response, content_type="application/json")



def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)

        uploaded_file_url = fs.url(filename)
        
        file_path = here +"/.."+uploaded_file_url
        

        uploaded_csv_url = execute(file_path_input= file_path)
        print(uploaded_csv_url)    
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url,
            'uploaded_csv_url': uploaded_csv_url
        })

    
    return render(request, 'simple_upload.html')


def home(request):
    return render(request, 'home.html')


def simple_uploadd(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        
        
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
