# Traffic

Read the official guideline [here](https://cs50.harvard.edu/ai/2020/projects/5/traffic/)

## Description
An AI that identifies which traffic sign appears in a photograph.

```
$ python traffic.py gtsrb
Epoch 1/10
500/500 [==============================] - 5s 9ms/step - loss: 3.7139 - accuracy: 0.1545
Epoch 2/10
500/500 [==============================] - 6s 11ms/step - loss: 2.0086 - accuracy: 0.4082
Epoch 3/10
500/500 [==============================] - 6s 12ms/step - loss: 1.3055 - accuracy: 0.5917
Epoch 4/10
500/500 [==============================] - 5s 11ms/step - loss: 0.9181 - accuracy: 0.7171
Epoch 5/10
500/500 [==============================] - 7s 13ms/step - loss: 0.6560 - accuracy: 0.7974
Epoch 6/10
500/500 [==============================] - 9s 18ms/step - loss: 0.5078 - accuracy: 0.8470
Epoch 7/10
500/500 [==============================] - 9s 18ms/step - loss: 0.4216 - accuracy: 0.8754
Epoch 8/10
500/500 [==============================] - 10s 20ms/step - loss: 0.3526 - accuracy: 0.8946
Epoch 9/10
500/500 [==============================] - 10s 21ms/step - loss: 0.3016 - accuracy: 0.9086
Epoch 10/10
500/500 [==============================] - 10s 20ms/step - loss: 0.2497 - accuracy: 0.9256
333/333 - 5s - loss: 0.1616 - accuracy: 0.9535
```

## Background
As research continues in the development of self-driving cars, one of the key challenges is computer vision, allowing these cars to develop an understanding of their environment from digital images. In particular, this involves the ability to recognize and distinguish road signs – stop signs, speed limit signs, yield signs, and more.

In this project, TensorFlow is used to build a neural network to classify road signs based on an image of those signs. To do so, you’ll need a labeled dataset: a collection of images that have already been categorized by the road sign represented in them.

Several such data sets exist, but for this project, we’ll use the [German Traffic Sign Recognition Benchmark](http://benchmark.ini.rub.de/?section=gtsrb&subsection=news) (GTSRB) dataset, which contains thousands of images of 43 different kinds of road signs.

---

# My Experimentation

The demonstration of my experimentation -> https://youtu.be/pdFbP-s96W8

## What I Tried

My observations for this network are formed from the experimentation which comprised of

- different numbers and sizes of convolutional and pooling layers
- different numbers of kernels
- Max-Pooling and Average-Pooling
- different dropout rates with various numbers of layers and units

## What I Noticed

### Convolutional and Pooling Layer

- The greater the pool_size, the less the accuracy.
- The greater the sizes of convolutional layer, the less the accuracy (generally), albeit with some exceptions.
- The number of kernels is found to be somewhat proportional to the accuracy as well.
- Adding double layers of convoluion and pooling is found to improve the accuracy of the network. However, further addition of those layers results in the otherwise.
- Max-Pooling turns out to fit slightly better than Average-Pooling with this particular dataset. Their difference becomes more conspicuous with double pooling layers of the same type.

### Dropout and Hidden Layers

- The gap between the maximum accuracy among those of each epoch while fitting model on training data and the accuracy when the network is evaluated is larger when the dropout rate is higher.
  - In this case, the accuracy in evaluation state in significantly higher than that in training state.
  - This proves that the network does sacrifice the accuracy in training state in order to be able to generalise well or reduce the loss in performing with actual testing data.
- Too high dropout rate can also result in poor performance while being evaluated. On the other hand, with too low or no dropout rate, the network, in actuality, doesn't perform as well as it does in training state.
- Choosing the most optimal middle ground might probably vary depending on the number of units in the previous hidden layer in sequential neural network.
- Addional hidden layer necessitates another dropout layer in order to circumvent overfitting for that added hidden layer in question.
