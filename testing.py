import requests

files = {'audio': open('/home/sadil/Downloads/OneDrive_2020-10-28/Audio samples/2020-Sep-25-FDS.N-139738717183-transcript.mp3','rb'),'file': open('/home/sadil/Downloads/OneDrive_2020-10-28/Audio samples/2020-Sep-25-FDS.N-139738717183-transcript.pdf','rb'),}
r = requests.post('http://localhost:5000/', files=files)
