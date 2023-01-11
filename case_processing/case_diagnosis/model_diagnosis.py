import tensorflow as tf
from architecture import BaseModel
from tensorflow.keras import layers

train_ds = tf.keras.utils.image_dataset_from_directory(
    "Imgs",
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(300, 300),
    batch_size=32,
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    "Imgs",
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(300, 300),
    batch_size=32,
)

class_names = train_ds.class_names

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

normalization_layer = layers.Rescaling(1.0 / 255)

normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
image_batch, labels_batch = next(iter(normalized_ds))
first_image = image_batch[0]

num_classes = len(class_names)

input_shape = (300, 300, 3)
net = BaseModel(input_shape)

net.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])

checkpoint_save_path = "./Model.ckpt"


cp_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_save_path, save_weights_only=True, save_best_only=True
)

history = net.fit(train_ds, epochs=30, batch_size=32, callbacks=[cp_callback])
