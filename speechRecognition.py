import speech_recognition as sr
from pydub import AudioSegment
from UtterenceModel import predictUtterence
import pickle
import numpy as np

MOCK_FILE_PATH = 'google_cloud_text.txt'

r = sr.Recognizer()

def speechToText(audiofile):
    newAudio = AudioSegment.from_mp3(audiofile)
    x = newAudio.duration_seconds*1000
    k = 0

    google_free_text_data = []
    emotion_array = []
    while k+5000<x:
        segment = newAudio[k:k+5000]
        segment.export('seg.mp3', format="mp3")
        sound = AudioSegment.from_mp3('seg.mp3')
        sound.export('seg.wav', format="wav")
        prediction = predictUtterence('seg.wav')
        emotion_array.append(np.argmax(prediction[0]))

        #with sr.AudioFile('seg.wav') as source:
        #    try:
        #        audio = r.record(source)
                #free
        #        text = r.recognize_google(audio)  
        #        google_free_text_data.append(text)
        #       print(text)
        #    except:
        #        google_free_text_data.append("")
        #        print("error")
        k+=5000
    
    return google_free_text_data, emotion_array

def mockSpeechToText():
    file = open(MOCK_FILE_PATH,'rb')
    return pickle.load(file)