#!/usr/bin/python

from SimpleCV import Camera, Image, Color, VirtualCamera

cam = VirtualCamera("pupilTest.mp4", "video", 200)

while True:
    img = cam.getImage()
    img = img.colorDistance(color=(255,0,0)).binarize(100)

    print img
   
    blobs = img.findBlobs()
    
    if blobs != None:
        blobs[-1].draw(color=(0, 0, 0))
        img.drawCircle((blobs[-1].x,blobs[-1].y),6, thickness=-1,color=Color.RED)
        img.drawCircle((blobs[-1].centroid()),5, thickness=-1,color=Color.BLUE)
        img.show()
    else:
        img.show()
