import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
import random
import pickle

# Load preprocessed data (from step 3)
import json

with open("intents.json") as f:
    data = json.load(f)

# You must have these variables from Step 3 in the same file or loaded
# If you're running this separately, you can pickle & load training and output arrays
with open("words.pkl", "rb") as f:
    words = pickle.load(f)

with open("classes.pkl", "rb") as f:
    classes = pickle.load(f)

with open("training_data.pkl", "rb") as f:
    training, output = pickle.load(f)

training = np.array(training)
output = np.array(output)

# Build the model
model = Sequential()
model.add(Dense(128, input_shape=(len(training[0]),), activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(len(output[0]), activation="softmax"))

# Compile model
sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])

# Train the model
hist = model.fit(training, output, epochs=200, batch_size=5, verbose=1)

# Save model and metadata
model.save("chatbot_model.keras")
print("Model trained and saved in .keras format")