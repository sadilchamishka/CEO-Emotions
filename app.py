from flask import Flask, request, jsonify
import pdfplumber
from pdfDataProcessor import processFirstpage,speakerSpeech
from speechRecognition import speechToText, mockSpeechToText

app = Flask(__name__)

def compare(text, speeches, current_index, stable_index):
  max_count = 0
  max_index = current_index
  index = stable_index
  for speech in speeches[stable_index:]:
    count = 0
    if index==current_index:
        count+=3
    for i in range(len(text)-1):
      if text[i]+' '+text[i+1] in ' '.join(speech):
        count+=1
    if max_count<count:
      max_count = count
      max_index = index
    index+=1
  
  return max_index

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
    
    #data = speechToText('transcript.mp3')
    data = mockSpeechToText()

    prediction_array = []
    current_index = 0
    stable_index = 0
    repeat_count = 0

    for transciption in data:
        if transciption!="":
            y = compare(transciption.split(' '), speeches, current_index, stable_index)
            if y==current_index:
                repeat_count +=1
            else:
                repeat_count = 0

            if repeat_count==3:
                stable_index = current_index

            current_index = y
            prediction_array.append(current_index)
        else:
            prediction_array.append("*")
    print(prediction_array)
    return "success"

if __name__ == "__main__":
    app.run()