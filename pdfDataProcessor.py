def processFirstpage(lines):
  CORPORATE_PARTICIPANTS = lines[lines.index('CORPORATE PARTICIPANTS')+1:lines.index('CONFERENCE CALL PARTICIPANTS')]
  CONFERENCE_CALL_PARTICIPANTS = lines[lines.index('CONFERENCE CALL PARTICIPANTS')+1:lines.index('PRESENTATION')]
  return CORPORATE_PARTICIPANTS, CONFERENCE_CALL_PARTICIPANTS, lines.index('PRESENTATION')

def speakerSpeech(lines, participants):
  a = []
  b = []
  speakers = []
  speeches = []
  line_no = 0

  for line in lines:
    if line in participants:             # The list of all the speakers and participants
      a.append(line)
      b.append(line_no)

    if len(a)==2:
      speakers.append(a[0])
      speeches.append(lines[b[0]+1:b[1]])
      a.pop(0)
      b.pop(0)
    
    line_no+=1
  
  endline = lines.index('DISCLAIMER')
  speakers.append(a[0])
  speeches.append(lines[b[0]+1:endline])
  return speakers,speeches