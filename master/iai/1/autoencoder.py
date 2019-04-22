#!/usr/bin/env python3
import math
import os
import numpy as np

from keras import (
    callbacks,
    layers,
    models,
    optimizers,
)
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from PIL import Image


def split(a, n, m):
    chunks = []
    for i in range(0, a.shape[0], n):
        for j in range(0, a.shape[1], m):
            chunks.append(a[i:i + n, j:j + m])
    return np.array(chunks)


def stack(chunks, rows, cols):
    return np.concatenate([
        np.concatenate(chunks[i * cols: (i + 1) * cols], axis=1)
        for i in range(rows)
    ], axis=0)


def open_image(filename, n, m):
    img = Image.open(filename)

    a = np.array(img)
    rows = math.ceil(a.shape[0] / n)
    cols = math.ceil(a.shape[1] / m)

    b = np.zeros((rows * n, cols * m, 3), a.dtype)
    b[:a.shape[0], :a.shape[1]] = a

    chunks = split(b, n, m)
    chunks = chunks.reshape((chunks.shape[0], n * m * 3))
    chunks = chunks / 255 - 0.5
    return chunks, a.shape[0], a.shape[1]


def save_image(filename, chunks, n, m, h, w):
    rows = math.ceil(h / n)
    cols = math.ceil(w / m)

    chunks = (chunks + 0.5) * 255
    chunks = chunks.reshape((chunks.shape[0], n, m, 3))

    b = stack(chunks, rows, cols)
    b = b[:h, :w]
    Image.fromarray(b.astype(np.uint8)).save(filename)


def create_model(n, k, lr):

    input_layer = layers.Input((n,))
    hidden_layer = layers.Dense(k, activation='linear')(input_layer)
    output_layer = layers.Dense(n, activation='linear')(hidden_layer)
    autoencoder = models.Model(inputs=[input_layer], outputs=[output_layer])

    optimizer = optimizers.Adagrad(lr=lr)
    autoencoder.compile(optimizer=optimizer, loss='mean_squared_error')
    autoencoder.summary()

    print()

    input_layer = layers.Input((n,), name='encoder-input-layer')
    output_layer = autoencoder.layers[1](input_layer)
    encoder = models.Model(inputs=[input_layer], outputs=[output_layer])
    encoder.compile(optimizer=optimizer, loss='mean_squared_error')

    input_layer = layers.Input((k,), name='decoder-input-layer')
    output_layer = autoencoder.layers[-1](input_layer)
    decoder = models.Model(inputs=[input_layer], outputs=[output_layer])
    decoder.compile(optimizer=optimizer, loss='mean_squared_error')

    return autoencoder, encoder, decoder


def create_deep_model(n, k, lr):
    optimizer = optimizers.Adagrad(lr=lr)

    input_layer = layers.Input((n,), name='input-layer')
    hidden_layer_1 = layers.Dense(k * 2, name='hidden-layer-1', activation='linear')(input_layer)
    hidden_layer_2 = layers.Dense(k, name='hidden-layer-2', activation='linear')(hidden_layer_1)
    hidden_layer_3 = layers.Dense(k * 2, name='hidden-layer-3', activation='linear')(hidden_layer_2)
    output_layer = layers.Dense(n, name='output-layer', activation='linear')(hidden_layer_3)
    autoencoder = models.Model(inputs=[input_layer], outputs=[output_layer])
    autoencoder.compile(optimizer=optimizer, loss='mean_squared_error')
    autoencoder.summary()
    print()

    return autoencoder


def fit_model(autoencoder, data, e=1e-5):

    class MyEarlyStopping(callbacks.Callback):

        def on_epoch_end(self, epoch, logs=None):
            current = logs.get('val_loss')
            if abs(current) < e:
                self.model.stop_training = True

    train, test = train_test_split(data, test_size=0.2, train_size=0.8)

    rv = autoencoder.fit(
        train, train,
        epochs=200,
        validation_split=0.2,
        callbacks=[MyEarlyStopping(), callbacks.EarlyStopping(patience=6)]
    )

    mse = mean_squared_error(test, autoencoder.predict(test))
    print('Test MSE: {:.8}'.format(mse))
    return rv


def process_image(filename, z, e, lr=0.01):
    N, M = 10, 10
    n = N * M * 3
    k = n // z

    autoencoder, encoder, decoder = create_model(n, k, lr)

    data, h, w = open_image(f'./in/{filename}', N, M)
    r = fit_model(autoencoder, data, e=e)

    # w = autoencoder.layers[1].get_weights()
    # print(w[0].shape)
    # print(w[1].shape)

    # encoded = encoder.predict(data)
    # # save_image(f'./mid/{filename}', encoded, N // z, M, h // z, w)
    #
    decoded = autoencoder.predict(data)
    save_image(f'./out/{filename}', decoded, N, M, h, w)

    mse = mean_squared_error(data, autoencoder.predict(data))
    print('Total MSE: {:.8}'.format(mse))

    return r.history


def process_image_deeply(filename, z, e, lr=0.01):
    N, M = 10, 10
    n = N * M * 3
    k = n // z

    autoencoder = create_deep_model(n, k, lr)

    data, h, w = open_image(f'./in/{filename}', N, M)
    r = fit_model(autoencoder, data, e=e)

    mse = mean_squared_error(data, autoencoder.predict(data))
    print('Total MSE: {:.8}'.format(mse))

    return r.history


def process_images(directory):
    N, M = 10, 10

    z = 10
    e = 1e-3
    n = N * M * 3
    k = n // z

    images = {}
    for base_path, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.jpg'):
                path = os.path.join(base_path, filename)
                images[path] = open_image(path, N, M)

    count = math.floor(len(images) * 0.8)
    print(count, list(images)[:count], list(images)[count:])
    data = np.concatenate([i[0] for i in list(images.values())[:count]])

    autoencoder, encoder, decoder = create_model(n, k, e)
    fit_model(autoencoder, data, e=e)

    for path, (data, h, w) in images.items():
        encoded = encoder.predict(data)
        save_image(path.replace('in', 'mid'), encoded, N // z, M, h // z, w)

        decoded = decoder.predict(encoded)
        save_image(path.replace('in', 'out'), decoded, N, M, h, w)

        mse = mean_squared_error(data, decoded)
        print('{} MSE: {:.8}'.format(path, mse))


if __name__ == '__main__':
    process_image('a.jpg', 4, 1e-4)
