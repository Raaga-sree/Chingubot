import json
import pickle
import re
import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
    ssl._create_default_https_context = _create_unverified_https_context
except:
    pass

stemmer=PorterStemmer()
words=[]
classes=[]
documents=[]
with open("intents.json") as f:
    data=json.load(f)
    print("Loaded intents: ")
    
inputs=[]
labels=[]


for intent in data['intents']:
    for pattern in intent['patterns']:
         inputs.append(pattern)
         labels.append(intent['tag'])
         
         
print("Sample input:",inputs[:3])
print("Sample labels:",labels[:3])
for intent in data['intents']:
      for pattern in intent['patterns']:
              word_list=nltk.word_tokenize(pattern)
              words.extend(word_list)
              documents.append((word_list,intent['tag']))
      if intent['tag'] not in classes:
            classes.append(intent['tag'])
words=[stemmer.stem(w.lower()) for w in words if w.isalnum()]
words=sorted(list(set(words
)))
classes=sorted(list(set(classes)))
print("words",words[:10])
print("classes",classes)
     
def clean_text(text):
    text=text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text
clean_inputs=[clean_text(sentence) for sentence in inputs]
print("cleaned inputs:",clean_inputs[:5])
training = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    pattern_words = [stemmer.stem(w.lower()) for w in doc[0] if w.isalnum()]
    
    for word in words:
        bag.append(1) if word in pattern_words else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

# Shuffle and convert to array
import random
random.shuffle(training)
training = np.array(training, dtype=object)

train_x = np.array(list(training[:, 0]))
train_y = np.array(list(training[:, 1]))

print("Training data created!")
print("Example input vector:", train_x[0])
print("Example output label:", train_y[0])
with open("words.pkl","wb") as f:
     pickle.dump(words,f)
with open("classes.pkl","wb") as f:
     pickle.dump(classes,f)
print("words.pkl and classes.pkl created successfully!")
with open("training_data.pkl","wb") as f:
     pickle.dump((train_x,train_y),f)
print("training_data.pkl created successfully")