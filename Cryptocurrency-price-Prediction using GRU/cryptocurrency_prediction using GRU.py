
"""CryptoCurrency_Prediction USING GRU.ipynb



from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.layers import Activation, Dense, Dropout, GRU
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error

data = pd.read_csv("/content/BTC.csv")
data = data.iloc[:,0:6]
y = data.loc[:,['Price']]
data = data.drop(['Price','Vol.'],axis='columns')
print(data.head(5))
print(y.head(5))

data = data.set_index('Date')
data.index = pd.to_datetime(data.index,unit='ns')
print(data.index)

aim = 'Price'

data.shape

X_train = data[300:]
X_test = data[:300]

y_train = y[300:]
y_test = y[:300]
print(y_test)


def line_plot(line1, line2, label1=None, label2=None, title='', lw=2):
    fig, ax = plt.subplots(1, figsize=(13, 7))
    ax.plot(line1, label=label1, linewidth=lw)
    ax.plot(line2, label=label2, linewidth=lw)
    ax.set_ylabel('BTC/USDT', fontsize=14)
    ax.set_title(title, fontsize=16)
    ax.legend(loc='best', fontsize=16);

line_plot(y_train[aim], y_test[aim], 'training', 'test', title='')

def normalise_zero_base(continuous):
    return continuous / continuous.iloc[0] - 1

def normalise_min_max(continuous):
    return (continuous - continuous.min()) / (data.max() - continuous.min())

X_train = normalise_zero_base(X_train)
X_test = normalise_zero_base(X_test)
y_train = normalise_zero_base(y_train)
y_test = normalise_zero_base(y_test)

import numpy as np
X_train = np.expand_dims(X_train, axis=1)
X_test = np.expand_dims(X_test,axis=1)

X_train.shape

from tensorflow import keras
# The GRU architecture
gruMODEL = Sequential()
# First GRU layer with Dropout regularisation
gruMODEL.add(GRU(
    units=1024,
    input_shape=(1,3),
    activation='PReLU',  
    recurrent_activation="sigmoid",
    use_bias=True,
    kernel_initializer="glorot_uniform",
    recurrent_initializer="orthogonal",
    bias_initializer="zeros",
    kernel_regularizer=None,
    recurrent_regularizer=None,
    bias_regularizer=None,
    activity_regularizer=None,
    kernel_constraint=None,
    recurrent_constraint=None,
    bias_constraint=None,
    dropout=0.0,
    recurrent_dropout=0.0,
    return_sequences=False,
    return_state=False,
    go_backwards=False,
    stateful=False,
    unroll=False,
    time_major=False,
    reset_after=True))
gruMODEL.add(Dropout(0.9))
# Second GRU layer
gruMODEL.add(GRU(
    units=2048,
    activation='PReLU',  
    recurrent_activation="sigmoid",
    use_bias=True,
    kernel_initializer="glorot_uniform",
    recurrent_initializer="orthogonal",
    bias_initializer="zeros",
    kernel_regularizer=None,
    recurrent_regularizer=None,
    bias_regularizer=None,
    activity_regularizer=None,
    kernel_constraint=None,
    recurrent_constraint=None,
    bias_constraint=None,
    dropout=0.0,
    recurrent_dropout=0.0,
    return_sequences=False,
    return_state=False,
    go_backwards=False,
    stateful=False,
    unroll=False,
    time_major=False,
    reset_after=True))
gruMODEL.add(Dropout(0.8))
# Third GRU layer
gruMODEL.add(GRU(
    units=4096,
    activation='PReLU',  
    recurrent_activation="sigmoid",
    use_bias=True,
    kernel_initializer="glorot_uniform",
    recurrent_initializer="orthogonal",
    bias_initializer="zeros",
    kernel_regularizer=None,
    recurrent_regularizer=None,
    bias_regularizer=None,
    activity_regularizer=None,
    kernel_constraint=None,
    recurrent_constraint=None,
    bias_constraint=None,
    dropout=0.0,
    recurrent_dropout=0.0,
    return_sequences=False,
    return_state=False,
    go_backwards=False,
    stateful=False,
    unroll=False,
    time_major=False,
    reset_after=True))
gruMODEL.add(Dropout(0.09))
# Fourth GRU layer
gruMODEL.add(GRU(
    units=512,
    activation='PReLU',  
    recurrent_activation="sigmoid",
    use_bias=True,
    kernel_initializer="glorot_uniform",
    recurrent_initializer="orthogonal",
    bias_initializer="zeros",
    kernel_regularizer=None,
    recurrent_regularizer=None,
    bias_regularizer=None,
    activity_regularizer=None,
    kernel_constraint=None,
    recurrent_constraint=None,
    bias_constraint=None,
    dropout=0.0,
    recurrent_dropout=0.0,
    return_sequences=False,
    return_state=False,
    go_backwards=False,
    stateful=False,
    unroll=False,
    time_major=False,
    reset_after=True))
gruMODEL.add(Dropout(0.09))
# The output layer
gruMODEL.add(Dense(units=1))
# Compiling the RNN
gruMODEL.compile(optimizer="sgd",loss='mean_squared_error')
gruMODEL.summary()

layers = [3,15,30,45,90,1]

layers_str = ["Input"] + ["GRU"] * (len(layers) - 2) + ["Output"]
layers_col = ["none"] + ["none"] * (len(layers) - 2) + ["none"]
layers_fill = ["black"] + ["gray"] * (len(layers) - 2) + ["black"]

penwidth = 15
font = "Hilda 10"

print("digraph G {")
print("\tfontname = \"{}\"".format(font))
print("\trankdir=LR")
print("\tsplines=line")
print("\tnodesep=.08;")
print("\tranksep=1;")
print("\tedge [color=black, arrowsize=.5];")
print("\tnode [fixedsize=true,label=\"\",style=filled," + \
    "color=none,fillcolor=gray,shape=circle]\n")

# Clusters
for i in range(0, len(layers)):
    print(("\tsubgraph cluster_{} {{".format(i)))
    print(("\t\tcolor={};".format(layers_col[i])))
    print(("\t\tnode [style=filled, color=white, penwidth={},"
          "fillcolor={} shape=circle];".format(
              penwidth,
              layers_fill[i])))

    print(("\t\t"), end=' ')

    for a in range(layers[i]):
        print("l{}{} ".format(i + 1, a), end=' ')

    print(";")
    print(("\t\tlabel = {};".format(layers_str[i])))

    print("\t}\n")
    # Nodes
for i in range(1, len(layers)):
    for a in range(layers[i - 1]):
        for b in range(layers[i]):
            print("\tl{}{} -> l{}{}".format(i, a, i + 1, b))

print("}")

with open('model.txt', 'w') as layers:

  layers = [3,5,10,15,20,1]

  layers_str = ["Input"] + ["GRU"] * (len(layers) - 2) + ["Output"]
  layers_col = ["none"] + ["none"] * (len(layers) - 2) + ["none"]
  layers_fill = ["black"] + ["gray"] * (len(layers) - 2) + ["black"]

  penwidth = 15
  font = "Hilda 10"

  print("digraph G {")
  print("\tfontname = \"{}\"".format(font))
  print("\trankdir=LR")
  print("\tsplines=line")
  print("\tnodesep=.08;")
  print("\tranksep=1;")
  print("\tedge [color=black, arrowsize=.5];")
  print("\tnode [fixedsize=true,label=\"\",style=filled," + \
    "color=none,fillcolor=gray,shape=circle]\n")

  # Clusters
  for i in range(0, len(layers)):
      print(("\tsubgraph cluster_{} {{".format(i)))
      print(("\t\tcolor={};".format(layers_col[i])))
      print(("\t\tnode [style=filled, color=white, penwidth={},"
          "fillcolor={} shape=circle];".format(
              penwidth,
              layers_fill[i])))

      print(("\t\t"), end=' ')

      for a in range(layers[i]):
          print("l{}{} ".format(i + 1, a), end=' ')

      print(";")
      print(("\t\tlabel = {};".format(layers_str[i])))

      print("\t}\n")
      # Nodes
  for i in range(1, len(layers)):
      for a in range(layers[i - 1]):
          for b in range(layers[i]):
              print("\tl{}{} -> l{}{}".format(i, a, i + 1, b))

  print("}")

!python python.py | dot -Tpdf > model_visulation.pdf

# Fitting to the training set
models = gruMODEL.fit(X_train,
                      y_train,
                      epochs=32,
                      batch_size=250,
                      validation_data=(X_test,y_test),
                      callbacks=[keras.callbacks.ModelCheckpoint("/content/model/model_{epoch}.h5")])

import matplotlib.pyplot as plt
plt.plot(models.history['loss'],'r',linewidth=2, label='Training loss')
plt.plot(models.history['val_loss'], 'g',linewidth=2, label='Validation loss')
plt.title('GRU Neural Networks - BTC Model')
plt.xlabel('Epochs numbers')
plt.ylabel('MSE numbers')
plt.show()

from tensorflow.keras.models import load_model
model = load_model('/content/model/model_32.h5')

preds = gruMODEL.predict(X_test).squeeze()
mean_absolute_error(preds, y_test)

from sklearn.metrics import mean_squared_error
SCORE_MSE=mean_squared_error(preds, y_test)
SCORE_MSE

from sklearn.metrics import r2_score
r2_score=r2_score(y_test, preds)
r2_score*100

y_test.ravel().shape

y_testt = scaling.inverse_transform(y_test)
print(type(y_testt))

preds = scaling.inverse_transform(gruMODEL.predict(X_test))

line_plot(y_testt, preds, 'test', 'prediction', title='')

"""27 March Prediction = **46351.24609375 BTC/USDT**

27 March 02.22AM (Istanbul Time) = **46564.0000 BTC/USDT**
"""

prediction = np.array([[44331,44818,44090]])
X_testt = scaling.inverse_transform(X_test[0])
prediction_new = np.array([[(X_test[0][0]/X_testt[0]*prediction[0])]])
predictions = gruMODEL.predict(prediction_new)[0][0]
predictions = np.array([[predictions]]) * prediction[0][0] / prediction_new[0][0][0]
f"27 March Prediction is {predictions[0][0]} BTC/USDT"

print("27 March Accuracy: ")
real = 46564
predict = predictions[0][0]
accuracy = 1- (real - predictions[0][0]) / real
print("Accuracy: {}".format(accuracy))
