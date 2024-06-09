from transformers import pipeline
import spacy
import re 

pipe1=pipeline("automatic-speech-recognition", model="openai/whisper-large-v3")
pipe2= pipeline("token-classification", model="dslim/bert-base-NER")


inp='#input'
transcript=pipe1(inp)
translower=transcript.lower()


nlp = spacy.load("en_core_web_lg")
pattern = r'\brupee(s)?\b'
replacement = 'dollar'
result = re.sub(pattern, replacement, translower, flags=re.IGNORECASE)
translower=result

a={}
if 'pledge' in translower :
   a['need']='pledge'
elif 'redeem' in translower or 'redemption' in translower or 'redemed' in translower:
   a['need']='redeem'
elif 'search' in translower:
   a['need']='search'


pattern = re.compile(r'[a-z]\d{5}|[A-Z]\d{5}')
billno = pattern.findall(translower)
a['billno']=billno


doc=nlp(translower)

for i in doc.ents:
  if i.label_=='MONEY':
     a['amount']=i.text
  if i.label_=='QUANTITY':
     a['weight']=i.text
  if i.label_=='DATE':
     a['date']=i.text

new=pipe2(transcript)
names = []
locations = []

for i in range(len(new)):
    if new[i]['entity'] in ['B-PER', 'I-PER']:
        if new[i]['word'].startswith('#') and i > 0 and new[i - 1]['entity'] in ['B-PER', 'I-PER']:
            names[-1] += new[i]['word'][1:] 
        else:
            names.append(new[i]['word']) 
    elif new[i]['entity'] in ['B-LOC', 'I-LOC']:
        if new[i]['word'].startswith('#') and i > 0 and new[i - 1]['entity'] in ['B-LOC', 'I-LOC']:
            locations[-1] += new[i]['word'][1:] 
        else:
            locations.append(new[i]['word']) 

names = [name.replace('#', '') for name in names]

locations = [loc.replace('#', '') for loc in locations]

print(a)
print(names)
print(locations)



