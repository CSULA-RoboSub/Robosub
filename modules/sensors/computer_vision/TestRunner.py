import DiceDetector as dd
dd = dd.DiceDetector(0)

while True:
    dd.detect()
    #dd.pp.show_preprocess_images()
    print dd.directions
