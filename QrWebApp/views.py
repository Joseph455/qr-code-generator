from django.http import response
from django.http.response import Http404, HttpResponseBadRequest, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from io import BytesIO
from io import FileIO
import qrcode
from qrcode.image.svg import SvgImage
from qrcode.image.pil import PilImage
from django.utils import timezone
from django.core.mail import EmailMessage, BadHeaderError
import json
from string import ascii_lowercase, ascii_uppercase
import os
import random

from QrWebApp.forms import RequestForm

# Create your views here.


def home(request):
    url = reverse(viewname="post")
    context = {"submition_url": url}
    return render(request, 'home.html', context)


def name_generator(date: str, file_type: str) -> str:
    choices = ascii_lowercase + ascii_uppercase + "0123456789"
    name = "".join([random.choice(choices) for i in range(10)])
    full_name = f'/media/{name}.{file_type}'
    return full_name
    
def file_generator(link: str, type: str) -> tuple:

    factories = {
        "svg": SvgImage,
        "png": PilImage,
        "jpeg": PilImage 
    }

    date = timezone.now().date()
    file_name = name_generator(date, type)

    stream = FileIO(file=file_name, mode="x")
    preview_stream = BytesIO()

    img_file = qrcode.make(
        data=link,
        image_factory=factories.get(type, 'svg'),
        box_size=20env("DEBUG")
    )
    
    if type != "svg":
        
        img_prev = qrcode.make(
            data=link,
            image_factory=factories.get('svg'),
            box_size=20
        )

    else:
        img_prev = img_file

    img_prev.save(preview_stream)
    img_file.save(stream)

    return file_name, preview_stream.getvalue().decode()

def deliver_file_as_email(file_name: str, file_type: str, email: str, link: str) -> bool:
    sub =  "QrCode Is Ready"
    
    msg = f"""
        The QrCode you requested for {link} has been generated and is attacthed to this mail.
    """

    mail = EmailMessage(
        subject= sub,
        body= msg,
        to=[email]
    )

    mail.attach_file(file_name, f"image/{file_type}")
    
    delivered = False
    
    try:
        delivered = True if ( mail.send(fail_silently=False) == 1) else False
    except BadHeaderError: 
        pass

    return delivered        

def delete_file(file_name) -> None:
    os.remove(file_name)

def post_url(request):
    if request.method == "POST" and request.is_ajax:
        form = RequestForm(request.POST)

        if form.is_valid():
            link = form.cleaned_data.get("url")
            email = form.cleaned_data.get("email")
            type = form.cleaned_data.get("type", "svg")
            file_name, file_preview = file_generator(link, type)

            delivered = deliver_file_as_email(file_name, type, email, link)            
            
            delete_file(file_name)
            
            msg = ""

            if delivered:
                msg = f"The QrCode for the link {link} has been generated and sent to your email {email}"
            else:
                msg = "Couldn't send the code  please try again."

            return JsonResponse(data={"message": msg, 'preview': file_preview})
        else:
            return HttpResponseBadRequest(content=json.dumps(form.errors))
    else:
        return HttpResponseNotAllowed


