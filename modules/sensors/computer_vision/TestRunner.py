import DetectBuoy as db
bd = db.DetectBuoy()
print bd.coords

while True:
    bd.detect()
    '''
    Update this to be a custom ROS message.
    the information must be of the form
    (x,y)
    where x,y are in {-1,0,1}
     x
    -1 left
     0 steady
     1 right
     
     y
     -1 down
     0 steady
     1 up
    '''
    print bd.coords

