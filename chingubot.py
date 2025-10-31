import random
import math
import re
import json
import pickle
import numpy as np
import datetime
import pytz
from tensorflow.keras.models import load_model
import nltk 
from nltk.stem import PorterStemmer
def solve_math(query):
     try:
          if "square root" in query.lower():
               numbers=[int(s) for s in re.findall(r'\d+',query)]
               if numbers:
                    return f"The square root of {numbers[0]} is {math.sqrt(numbers[0]):.2f}"
          expression=re.sub(r'[^0-9+\-*/().]','',query)
          if expression:
               try:
                  result=eval(expression)
                  return f"The answer is {result}"
               except ZeroDivisionError:
                    return "Oops 😅 dividing by zero is impossible,even for me!"
     except Exception:
          pass 
     return "Sorry,I'm not a topper in Math 🤓,but I'll try to learn!"         
model=load_model("chatbot_model.keras")
words=pickle.load(open("words.pkl","rb"))
classes=pickle.load(open("classes.pkl","rb"))
with open("intents.json") as file:
     intents=json.load(file)
stemmer=PorterStemmer()
unknown_response=[
"Hmm..I'm not sure what you mean🤔,but I'm trying my best!!!",
"Oops,I'm still learning that one🥲",
"Ahh!! I missed that can you try to asking  me in a different way 🧐??"]
india_time=datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
current_hour=india_time.hour
if 5<=current_hour<12:
  greeting="Good Morning🌞"
elif 12<=current_hour<15:
    greeting="Good Afternoon☀️"
elif  15<=current_hour<18:
    greeting="Good Evening🌆"
else:
    greeting="Good Night🌙"
comment="" 
if 16<=current_hour<18:
    comment="Have you  had your evening tea☕️??" 
elif current_hour>=21 or current_hour<=4:
    comment="Why are you still up??,it's time to bed😴"
def clean_up_sentence(sentence):
     sentence_words=nltk.word_tokenize(sentence)
     sentence_words=[stemmer.stem(word.lower()) for word in sentence_words]
     return sentence_words
def bow(sentence,words):
     sentence_words=clean_up_sentence(sentence)
     bag=[0]*len(words)
     for s in sentence_words:
          for i, w in enumerate(words):
               if w==s:
                    bag[i]=1
     return np.array(bag)
def predict_class(sentence):                
    bow_vector=bow(sentence,words)
    res=model.predict(np.array([bow_vector]))[0]
    ERROR_THRESHOLD=0.2
    results=[[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1],reverse=True)
    return_list=[]
    for r in results:
         return_list.append({"intent": classes[r[0]],"probability":str(r[1])})
    return return_list
def get_response(intents_list,intents_json):
     if len(intents_list)==0:
          return random.choice(unknown_response)
     tag=intents_list[0]["intent"]
     list_of_intents=intents_json["intents"]
     for i in list_of_intents:
          if i["tag"]==tag:
               return random.choice(i["responses"])
     return random.choice(unknown_response)          
user_name=input("Chingubot:Before we start,what's your name?\nyou:").capitalize()  
print(f"Chingubot:Nice to meet you {user_name}😃")
print(f"{greeting} ,I'm Chingubot,Ask me something")
if comment:
     print(f"Chingubot:{comment}")
while True:
    user_input=input("You: ").lower()
    if user_input in ["bye","quit","exit"]:
                 print("Chingubot: Goodbye👋!, come back soon💖")
                 break
    if any(op in user_input for op in["+","-","*","/","square root"]):
        print("Chingubot:",solve_math(user_input))
        continue
    
    if any(greet in user_input for greet in ["hello","hi"]):
        print(f"Chingubot:{greeting},Human😃")
        if comment:
           print(f"Chingubot:{comment}")
        continue
    elif "your name" in user_input or "what is your name" in user_input:
         print("Chingubot:I'm Chingubot,your study buddy!")
         continue
    elif "how are you" in user_input:
          print("Chingubot:I'm functioning as expected and you!!")
          continue
    elif "what are you doing" in user_input:
         print("Chingubot:Just chilling in the terminal😎 and you??")
         continue
    elif "i'm tired" in user_input or "i am tired" in user_input:
        print("Chingubot:Aww,take a break chingu,\nyou have done enough today🩷")
        continue
    elif "i'm bored" in user_input or "i am bored " in user_input:
        print("Chingubot:wanna chill with some k-drama or wanna do something you love😁?")
    elif "thank you" in user_input:
        print("Chingubot:you're always welcome 😁  and anything for you chingu🫶")
        continue
    elif "you're cute" in user_input or "you are cute" in user_input:
        print("Chingubot:Aigoo!!☺️ stop it ,I'm blushing in binary ,anyways THANK YOU🥰 and you too💖")
        continue
    else:
      ints=predict_class(user_input)
      res=get_response(ints,intents)
      print(f"Chingubot: {res}")
    