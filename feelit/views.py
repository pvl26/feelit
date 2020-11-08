from django.shortcuts import render
from .forms import ReceveImage
from django.http import HttpResponse


import json
import os
import base64
import sys
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from apps.accounts.models import Person

# MAX_SIZE = 10*1024*1024 #10MB
import cv2
import numpy as np
import os.path

from cv2 import WINDOW_NORMAL
from facifier.src.face_detection import find_faces

def faceial_emotion_recognition(path):
    emotions = ["afraid", "angry", "disgusted", "happy", "neutral", "sad", "surprised"]

    # Load model
    fisher_face_emotion = cv2.face.FisherFaceRecognizer_create()
    fisher_face_emotion.read('facifier/src/models/emotion_classifier_model.xml')

    fisher_face_gender = cv2.face.FisherFaceRecognizer_create()
    fisher_face_gender.read('facifier/src/models/gender_classifier_model.xml')

    model_emotion = fisher_face_emotion
    model_gender = fisher_face_gender

    print(path)

    image = cv2.imread(path, 1)
    for normalized_face, (x, y, w, h) in find_faces(image):
        emotion_prediction = model_emotion.predict(normalized_face)
        gender_prediction = model_gender.predict(normalized_face)
        if (gender_prediction[0] == 0):
            cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255), 2)
        else:
            cv2.rectangle(image, (x,y), (x+w, y+h), (255,0,0), 2)

    return emotion_prediction[0]

@csrf_exempt
def save_person(request):
    if (request.method == "POST" and request.META.get("CONTENT_TYPE")
        == "application/json"):
        data = json.loads(request.body)
        avatar = data.get("avatar")
        file = base64.b64decode(avatar["file"])

        person = Person(avatar=SimpleUploadedFile(
            "test.png",
            file,
            getattr(avatar, "content_type", "application/octet-stream")))
        
        person.save()
        path = "media/avatars/test.png"
        faceial_emotion = faceial_emotion_recognition(path)
        os.remove(path)
        person.delete()

        response = {"id": person.id,
            "avatar": person.avatar.url}
        
        print(faceial_emotion)
        
        return render(request, 'succes.html', {
            'facial_emotion': faceial_emotion
        })
        # return HttpResponse(json.dumps(response), mimetype="application/json")

    response = {"error": {
        "code": "invalid_request",
        "message": "Method Not Allowed."
        }}
    return HttpResponseBadRequest(json.dumps(response),
        mimetype="application/json")

def homepage(request):
    return render(request, 'homepage.html')


# from django.conf import settings
# from django.core.files.storage import FileSystemStorage

# def homepage(request):
#     context = {} 
#     if request.method == 'POST' and request.FILES['image']:
#         myfile = request.FILES['image']
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)
#         uploaded_file_url = fs.url(filename)
#         return render(request, 'succes.html', {
#             'uploaded_file_url': uploaded_file_url
#         })
#     else:
#         form = ReceveImage()
#     context['form'] = form 
#     return render(request, 'homepage.html', context)



def about(request):
    return render(request, 'about.html')

def posts(request):
    html = "<html><body><h1<Hello There</h></body></html>"
    return HttpResponse(html)
