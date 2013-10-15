'''
Created on 03.07.2013

@author: flavio
'''
from SimpleCV import Image, Camera, DrawingLayer

def findRedDot(redDot):
    #Find the distance of the other colors on the image to the searched RED
    redDist = redDot.colorDistance(color=(255,0,0))

    #Binarize to create even more contrast
    #(Detect direct color is faster???)
    redDot = redDist.binarize(100).invert()

    #Find circles (should be only 1)
    circles = redDot.findCircle(thresh=30, distance=100)
    if (circles != None):
        return circles.coordinates()
    else:
        return None


if __name__ == '__main__':
    cam = Camera(0)
    img = Image()

    samples = 0
    coordinates = redCoords = (0,0)
    text = " "

    while True:
        img = cam.getImage()
        # Make image black and white
        tmp = findRedDot(img)
        if (tmp != None):
            coordinates= (coordinates[0]+tmp[0][0], coordinates[1]+tmp[0][1])
            samples+=1

        if samples == 10:
            samples = 0
            coordinates = (coordinates[0]/10, coordinates[1]/10)
            text = str(coordinates)
            redCoords = coordinates
            coordinates = (0,0)

        redcircle = DrawingLayer((img.width, img.height))
        redcircle.circle(redCoords, 5, filled=True, color=(0,255,0)) #add circle point 10,10, radius 10.
        img.addDrawingLayer(redcircle)
        img.applyLayers()
        img.drawText(text)
        img.show()