

import pygtk

pygtk.require('2.0')
import gtk
import sys

from multiprocessing import Process, Queue
import time

from SimpleCV import VirtualCamera, DrawingLayer, Color, Camera




class gui:
    def __init__(self, queue):
        self.gladefile = "binControl.glade"
        self.glade = gtk.Builder()
        self.glade.add_from_file(self.gladefile)
        self.glade.connect_signals(self)
        self.glade.get_object("windowMain").show_all()
        self.q = queue

        self.scale = self.glade.get_object("binValue")

    def on_MainWindow_delete_event(self, widget, event):
        gtk.main_quit()

    def on_binValue_value_changed(self, widget):
        try:
            self.q.put(self.glade.get_object("binValue").get_value())

        except ValueError:
            return 0


    def on_windowMain_destroy(self, widget):
        sys.exit(0)


def startGUI(queue):
    gui(queue)
    gtk.main()



def startCAM(queue):
    cam = Camera()
    #cam = VirtualCamera("pupilTest.mp4", "video", 300)
    binarizationValue = 30

    while True:
        if not queue.empty():
            binarizationValue = queue.get()
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

    #Prepare Queue for passing binarization
    q = Queue()

    guiProcess = Process(target=startGUI, args=(q,))
    guiProcess.start()

    camProcess = Process(target=startCAM, args=(q,))
    camProcess.start()





if __name__ == "__main__":
    main()


