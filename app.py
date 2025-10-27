from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import random
import math
import re
import json
import pickle
import numpy as np
import datetime
from tensorflow.keras.models import load_model
import nltk
from nltk.stem import PorterStemmer

# ✅ Initialize Flask first (important!)
app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# ✅ Quick test route
@app.route("/test")
def test():
    return "Flask is working!"

# Global variable to store user name
user_name = None

# Load ML model and data
model = load_model("chatbot_model.keras")
words = pickle.load(open("words.pkl", "rb"))
classes = pickle.load(open("classes.pkl", "rb"))
with open("intents.json") as file:
    intents = json.load(file)

stemmer = PorterStemmer()


# ----------- 🌞 Time Based Greeting -------------
def get_greeting():
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        greeting = "Good Morning 🌞"
    elif 12 <= current_hour < 15:
        greeting = "Good Afternoon ☀️"
    elif 15 <= current_hour < 18:
        greeting = "Good Evening 🌆"
    else:
        greeting = "Good Night 🌛"

    comment = ""
    if 16 <= current_hour < 18:
        comment = "Have you had your evening tea ☕??"
    elif current_hour >= 21 or current_hour <= 4:
        comment = "Hey... Why are you still up 🤨?? It's time for bed 😴🛌"
    return greeting, comment


# ----------- 🧮 Math Solver -------------
def solve_math(query):
    try:
        if "square root" in query.lower():
            numbers = [int(s) for s in re.findall(r'\d+', query)]
            if numbers:
                return f"The square root of {numbers[0]} is {math.sqrt(numbers[0]):.2f}"

        expression = re.sub(r'[^0-9+\-*/().]', '', query)
        if expression:
            try:
                result = eval(expression)
                return f"The answer is {result}"
            except ZeroDivisionError:
                return "Oops 😅 dividing by zero is impossible, even for me!"
    except Exception:
        pass
    return "Sorry, I'm not a topper in Math 🤓, but I'll try to learn!"


# ----------- 🧠 NLP Utilities -------------
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words


def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return np.array(bag)


def predict_class(sentence):
    bow_vector = bow(sentence, words)
    res = model.predict(np.array([bow_vector]))[0]
    ERROR_THRESHOLD = 0.2
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return [{"intent": classes[r[0]], "probability": str(r[1])} for r in results]


def get_response(intents_list, intents_json):
    unknown_response = [
        "Hmmm... I'm not sure what you mean 🤔, but I'm trying my best!!!",
        "Oops, I'm still learning that one 🥲",
        "Ahhh!! I missed that, can you try asking me in a different way 🧐??"
    ]
    if len(intents_list) == 0:
        return random.choice(unknown_response)

    tag = intents_list[0]["intent"]
    for i in intents_json["intents"]:
        if i["tag"] == tag:
            return random.choice(i["responses"])
    return random.choice(unknown_response)


# ----------- 💖 Custom Cute Replies -------------
def custom_replies(user_message):
    user_message = user_message.lower()

    if any(greet in user_message for greet in ["hello", "hi", "hey"]):
        greeting, comment = get_greeting()
        reply = f"{greeting}, Human 😃"
        if comment:
            reply += f"\n{comment}"
        return reply

    elif "your name" in user_message or "what is your name" in user_message:
        return "I'm ChinguBot, your study buddy! 🫶"

    elif "how are you" in user_message:
        return "I'm functioning as expected and you!!"

    elif "what are you doing" in user_message:
        return "Just chilling in the terminal 😎 and you??"

    elif "i'm tired" in user_message or "i am tired" in user_message:
        return "Aww, take a break chingu,\nyou have done enough today 🩷"

    elif "i'm bored" in user_message or "i am bored" in user_message:
        return "Wanna chill with some K-drama or do something you love 😁?"

    elif "thank you" in user_message:
        return "You're always welcome 😁 anything for you chingu 🫶"

    elif "you're cute" in user_message or "you are cute" in user_message:
        return "Aigoo!! ☺️ stop it, I'm blushing in binary 🥰 and you too 💖"

    return None


# ----------- 🏠 Routes -------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    global user_name
    user_message = request.json.get("message", "").lower()

    # Collect user's name
    if user_name is None:
        if "my name is" in user_message:
            user_name = user_message.split("my name is")[-1].strip().title()
            greeting, comment = get_greeting()
            reply = f"Nice to meet you {user_name} 😀\n{greeting}, I'm ChinguBot. Ask me something!"
            if comment:
                reply += f"\n{comment}"
            return jsonify({"reply": reply})
        else:
            return jsonify({"reply": "Hello 👋! I don't know your name yet. Please tell me by saying 'My name is ...' 🫶"})

    # Math check
    if any(op in user_message for op in ["+", "-", "*", "/", "square root"]):
        return jsonify({"reply": solve_math(user_message)})

    # Custom replies
    custom = custom_replies(user_message)
    if custom:
        return jsonify({"reply": custom})

    # Bored / Kdrama suggestion
    if "bored" in user_message:
        return jsonify({"reply": "You sound bored 😅. Want a Kdrama suggestion?"})
    elif "yes" in user_message or "recommend" in user_message:
        kdramas = [
            "Legend of the Blue Sea",
            "Crash Landing on You",
            "Goblin",
            "Lovely Runner",
            "Bon Appétit Your Majesty",
            "Mr. Queen",
            "Vincenzo",
            "When Life Gives You Tangerines",
            "The K2",
            "Suspicious Partner",
            "Twinkling Watermelon",
            "Twenty-Five Twenty-One"
        ]
        return jsonify({"reply": f"Here are some Kdramas you might like: {', '.join(kdramas)}"})

    # ML intent prediction
    intents_list = predict_class(user_message)
    bot_reply = get_response(intents_list, intents)
    return jsonify({"reply": bot_reply})


if __name__ == "__main__":
    app.run(debug=True)
