from django.shortcuts import render
# Create your views here.
# Importo Firebase Admin SDK 
import firebase_admin
 
# Hacemos uso de credenciales que nos permitirán usar Firebase Admin SDK 
from firebase_admin import credentials
 
# Importo el Servicio Firebase Realtime Database 
from firebase_admin import db

import os
import json
import requests

rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
FIREBASE_WEB_API_KEY = "AIzaSyAg2YwVXHQNJJXcdqh-emDCRr8nIFtD-XE"

cred = credentials.Certificate('./sysonenit901491409-firebase-adminsdk-lw6sw-2ed2ed0b1a.json')

firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://sysonenit901491409-default-rtdb.firebaseio.com/'
})


def IndexView(request):
        return render(request,"index.html")

def signIn(request):
        return render(request,"signin_copy.html")

def postsignIn(request):
        email=request.POST.get('email')

        pasw=request.POST.get('pass')
        infor_user=login_email_password(email,pasw)

        try:
                ref = db.reference('usuarios') 
                
                #print(infor_user)
                session_id=infor_user['idToken']
                request.session['uid']=str(session_id)

                datos = ref.get()[infor_user["localId"]]
                print(datos)
                return render(request,"Home.html",{"datosusuario":datos})
        except:
                message=infor_user["error"]["message"]
                print(message)
                return render(request,"signin_copy.html",{"message":message})

def Contacto(request):
        return render(request,"contacto.html")

def Aboutus(request):
        return render(request,"aboutus.html")

def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request,"signin_copy.html")

def login_email_password(emails,password):
        payload=json.dumps({
		"email":emails,
		"password":password,
		"returnSecureToken":True})
        r=requests.post(rest_api_url,
                        params={"key": FIREBASE_WEB_API_KEY},
                        data=payload)
        
        return r.json()