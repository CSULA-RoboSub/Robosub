from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array,load_img
import glob
datagen = ImageDataGenerator(
            rotation_range=60,
            width_shift_range=0.05,
            height_shift_range=0.05,
            rescale=1./255,
            zoom_range=0.2,
            horizontal_flip=True,
            fill_mode='nearest'
        )

imgs = []

for img in glob.glob('pos_dice/*.jpg'):
    im = load_img(img)
    x = img_to_array(im)
    x = x.reshape((1,) + x.shape)
    imgs.append(x)

for x in imgs:
    i = 0
    for batch in datagen.flow(x, batch_size=1, save_to_dir='pos_dice',save_prefix='die', save_format='jpg'):
        i+=1
        if i > 20:
            break