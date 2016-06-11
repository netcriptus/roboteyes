How to install NLTK:

Run python3 shell and run nltk.download() to download all models and stuff initially.


make sure to:

export GOOGLE_APPLICATION_CREDENTIALS=creds.json

first.


Sample curl to test locally:

curl -X POST http://0.0.0.0:5000/ -H 'Content-Type: multipart/form-data' -F 'question=What do I have in my pantry?' -F 'image=@testimages/pantry.jpg'