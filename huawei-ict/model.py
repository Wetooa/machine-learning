from keras.models import Sequential, load_model
from keras.layers import Dense
from sklearn.model_selection import train_test_split

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


# |%%--%%| <SrCq6lEpzh|vfTIuMV5vR>

csv_file_path = r"./data/Combined_data.csv"
df = pd.read_csv(csv_file_path)
data = np.array(df, dtype="float")

# |%%--%%| <vfTIuMV5vR|CPrKiOuolb>

X, y = data[:, :-1], data[:, -1]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.4, random_state=42
)

# |%%--%%| <CPrKiOuolb|uJ2uHidnyw>

model = Sequential()
model.add(Dense(32, input_dim=X_train.shape[1], activation="relu"))
model.add(Dense(1, activation="softmax"))
model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

# |%%--%%| <uJ2uHidnyw|ghWo7I0idn>

model.fit(X_train, y_train, epochs=10, batch_size=1, validation_data=(X_test, y_test))

# |%%--%%| <ghWo7I0idn|0wttUpypa4>

loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Loss: {loss}, Test Accuracy: {accuracy}")
