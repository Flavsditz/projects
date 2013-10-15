

import pygtk

pygtk.require('2.0')
import gtk
import sys

import threading
import time

from SimpleCV import VirtualCamera, DrawingLayer, Color, Camera

binarizationValue = 30


class gui:
    def __init__(self):
        self.gladefile = "binControl.glade"
        self.glade = gtk.Builder()
        self.glade.add_from_file(self.gladefile)
        self.glade.connect_signals(self)
        self.glade.get_object("windowMain").show_all()

        self.scale = self.glade.get_object("binValue")
        #self.scale.connect("value-changed", self.on_binValue_value_changed)

    def on_MainWindow_delete_event(self, widget, event):
        gtk.main_quit()


    def on_binValue_value_changed(self, widget):
        print "At change value"
        try:
            global binarizationValue
            binarizationValue = self.glade.get_object("binValue").get_value()
            print binarizationValue
        except ValueError:
            return 0


    def on_windowMain_destroy(self, widget):
        sys.exit(0)


def startGUI():
    gui()
    gtk.main()



def startCAM():
    global binarizationValue
    cam = Camera()
    #cam = VirtualCamera("pupilTest.mp4", "video", 300)

    while True:
        img = cam.getImage().binarize(binarizationValue)
        blobs = img.findBlobs()

        if blobs is None:
            img.show()
        else:
            blobs[-1].draw(color=(0, 0, 0))
            img.drawCircle((blobs[-1].x,blobs[-1].y),6, thickness=-1,color=Color.RED)
            img.drawCircle((blobs[-1].centroid()),5, thickness=-1,color=Color.GREEN)

            sTmp = "Center of Mass: "+str(blobs[-1].x)+", "+str(blobs[-1].y)
            img.drawText(sTmp, x=10, y=30, color=Color.RED, fontsize=20)
            sTmp = blobs[-1].centroid()
            sTmp = "  Bounding Box: "+str(int(sTmp[0]))+", "+ str(int(sTmp[1]))
            img.drawText(sTmp, x=10, y=10, color=Color.GREEN, fontsize=20)

            img.show()

            #time.sleep(10)

def main():

    print "First Thread"

    guiThread = threading.Thread(target=startGUI)
    guiThread.start()

    startCAM()
    print "Got Here!"
    '''
    startGUI()
    '''





if __name__ == "__main__":
    main()


