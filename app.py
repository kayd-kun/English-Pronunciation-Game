import uuid
import os, subprocess
from os import path
from flask import Flask, request, render_template, flash, redirect
# Speech Recognition Library
import speech_recognition as sr
from flask import jsonify

import pyttsx3
engine = pyttsx3.init()
# engine.setProperty('rate', 150) 
engine.setProperty('volume',2.0)


app = Flask(__name__)
# # For CSRF token
app.config['SECRET_KEY'] = 'AADDGADFKJAKDFHNNADS;FA'
app.config['SESSION_TYPE'] = 'filesystem'

# from flask import Flask
app = Flask(__name__)

predefined_words = [
    'Understand',
    'People',
    'Hello',
    'Country',
    'English',
    'Computer',
    'Don\'t',
]

@app.route('/')
def hello_world():
    return render_template('index.html', predefined_words=predefined_words)

@app.route('/save-record', methods=['POST'])
def save_record():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    # file_name = str(uuid.uuid4()) + ".WebM"
    # full_file_name = os.path.join('uploaded_audio', file_name)
    full_file_name = os.path.join('uploaded_audio', 'user_audio.WebM')
    file.save(full_file_name)
    convert_webm_to_wav(full_file_name)
    return 'Success'

def convert_webm_to_wav(fileName):
    # ffmpeg -i /content/audio.WebM /content/audio.wav -y
    subprocess.run(["ffmpeg", "-i", f"{fileName}", "./uploaded_audio/check_audio.wav", "-y"])

@app.route('/check-audio', methods=['POST'])
def checkAudio():
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), "./uploaded_audio/check_audio.wav")
    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file
    
    result = ''
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        result = r.recognize_google(audio)
        print('=============================')
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        result = 'Could Not Understand'
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        result = 'Service not available from google'

    # return f'<p>{result}</p>'
    return jsonify(result=result)

@app.route('/speak-audio/<word>')
def speak_audio(word):
    engine.say(word)
    engine.runAndWait()
    engine.stop()
    return "OK"
