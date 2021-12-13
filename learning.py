from tensorflow import keras, nn
import numpy as np

mnist = keras.datasets.mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = keras.models.Sequential([
  keras.layers.Flatten(input_shape=(28, 28)),
  keras.layers.Dense(128, activation='relu'),
  keras.layers.Dropout(0.2),
  keras.layers.Dense(10)
])

predictions = model(x_train[:1]).numpy()
# print(predictions)

loss_fn = keras.losses.SparseCategoricalCrossentropy(from_logits=True)
# print("Loss: ", loss_fn(y_train[:1], predictions).numpy())

model.compile(optimizer='adam', loss=loss_fn, metrics=['accuracy'])

# model.fit(x_train, y_train, epochs=1)

# model.evaluate(x_test,  y_test, verbose=2)

for weights in model.get_weights():
    print("#####  SHAPE  ##### ")
    print(np.shape(weights))
    print(weights)


