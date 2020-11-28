from flask import Flask, request, jsonify
import pdfplumber
from pdfDataProcessor import processFirstpage,speakerSpeech
import speech_recognition as sr
from pydub import AudioSegment

r = sr.Recognizer()

app = Flask(__name__)

@app.route("/", methods = ['POST'])
def home():
    conversation = request.files['audio']
    conversation.save('transcript.mp3')

    pdfTranscription = request.files['file']
    pdfTranscription.save('transcript.pdf')
    
    with pdfplumber.open(r'transcript.pdf') as pdf:
        all_text_data = []
        page_no = 0
        for page in pdf.pages:
            if page_no>0:
                all_text_data.extend(page.extract_text().split('\n')[1:-5])
            page_no+=1

    #found one occurance so removing   
    if "QUESTIONS AND ANSWERS" in all_text_data:
        all_text_data.remove("QUESTIONS AND ANSWERS")

    CORPORATE_PARTICIPANTS, CONFERENCE_CALL_PARTICIPANTS, start = processFirstpage(all_text_data)
    participants = CORPORATE_PARTICIPANTS+CONFERENCE_CALL_PARTICIPANTS+['Operator ']
    speakers,speeches = speakerSpeech(all_text_data[start:], participants)
    

    newAudio = AudioSegment.from_mp3('transcript.mp3')
    x = newAudio.duration_seconds*1000
    k = 0

    google_free_text_data = []

    while k+5000<x:
        segment = newAudio[k:k+5000]
        segment.export('seg.mp3', format="mp3")
        sound = AudioSegment.from_mp3('seg.mp3')
        sound.export('seg.wav', format="wav")

        with sr.AudioFile('seg.wav') as source:
            try:
                audio = r.record(source)
                #free
                text = r.recognize_google(audio)  
                google_free_text_data.append(text)
                print(text)
            except:
                google_free_text_data.append("")
                print("error")
        k+=5000



    return "success"

if __name__ == "__main__":
    app.run()