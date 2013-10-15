from SimpleCV import Image, DrawingLayer, Color, Display


d = Display((1240, 820), title="London Map - Scotland Yard")
lMap = Image("C:\\Users\\flavio\\Documents\\Python\\Scotland Yard\\maps\\map.jpg")
circlesLayer = DrawingLayer((lMap.width, lMap.height))

circlesLayer.circle ((191,44), 20,color=Color.ORANGE, filled=True, alpha = 255)
lMap.addDrawingLayer(circlesLayer)
lMap.applyLayers()

lMap.save(d)