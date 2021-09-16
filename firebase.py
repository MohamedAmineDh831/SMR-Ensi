from pyrebase import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyAQzFDLyW2rDwbp5X5ES0QqC-UWz4DUbPc",
    "authDomain": "follow-86634.firebaseapp.com",
    "databaseURL": "https://follow-86634-default-rtdb.firebaseio.com/",

    "storageBucket": "follow-86634.appspot.com",

  }
firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()

database.child("nizar").set({"username":"nizar1","firstname": "nizar", "lastname":"selmi","email":"nizar@","password":"123456"})