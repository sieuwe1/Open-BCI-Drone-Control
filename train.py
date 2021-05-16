from models import EEGNet, LSTMNet

from sklearn.model_selection import KFold, cross_val_score
from matplotlib import pyplot as plt
import numpy as np
import keras
import time

def fit_and_save(model, epochs, train_X, train_y, validation_X, validation_y, batch_size):
    # fits the network epoch by epoch and saves only accurate models
    val_acc = []
    acc = []

    # saving the model one epoch at a time
    for epoch in range(epochs):
        print("EPOCH: ", epoch)
        history = model.fit(train_X, train_y, epochs=1, batch_size=batch_size,
                            validation_data=(validation_X, validation_y))

        val_loss = history.history["val_loss"][-1]
        score = history.history["val_accuracy"][-1]
        val_acc.append(score)
        acc.append(history.history["accuracy"][-1])

        MODEL_NAME = f"models/{round(score * 100, 2)}-{epoch}epoch-{int(time.time())}-loss-{round(val_loss, 2)}.model"

        if  round(score * 100, 4) >= 81 and round(history.history["accuracy"][-1] * 100, 4) >= 81:
            # saving & plotting only relevant models
            model.save(MODEL_NAME)
            print("saved: ", MODEL_NAME)

            plt.plot(np.arange(len(val_acc)), val_acc)
            plt.plot(np.arange(len(acc)), acc)
            plt.title('Model Accuracy')
            plt.ylabel('accuracy')
            plt.xlabel('epoch')
            plt.legend(['val', 'train'], loc='upper left')
            plt.show()

def main():
    # TODO Load data

    OUTPUTS = ["left", "right", "empty"]
    model = EEGNet(nb_classes=len(OUTPUTS))
    model.summary()
    model.compile(loss='categorical_crossentropy',
                  optimizer='nadam',
                  metrics=['accuracy'])

    keras.utils.plot_model(model, "pictures/net.png", show_shapes=True)

    batch_size = 16
    epochs = 1000

    # kfold_cross_val(model, train_X, train_y, epochs, num_folds=10, batch_size=batch_size)
    fit_and_save(model, epochs, train_X, train_y, validation_X, validation_y, batch_size)


if __name__ == "__main__":
    main()