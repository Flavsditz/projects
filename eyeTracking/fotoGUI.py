#!/usr/bin/python

import pygtk
pygtk.require('2.0')
import gtk
import time

import sys
from SimpleCV import Image, Camera

class VideoObject:

    def __init__(self, camNr):
        self.cam = Camera(camNr)
        self.img = Image()

    def getImg(self):
        self.img = self.cam.getImage()
        self.img.save("foto.jpg")
        return "foto.jpg"



class guiTester:

    def __init__(self):
        self.gladefile = "main.glade"
        self.glade = gtk.Builder()
        self.glade.add_from_file(self.gladefile)
        self.glade.connect_signals(self)
        self.glade.get_object("hbox1").connect('expose-event', draw_pixbuf)
        self.glade.get_object("windowMain").show_all()

    def on_MainWindow_delete_event(self, widget, event):
        gtk.main_quit()

    def on_addButton_clicked(self, widget):
        print "At newImage"
        try:
            thisTime = VideoObject(0)
        except ValueError:
            return 0
        self.glade.get_object("imageHolder").set_from_file(thisTime.getImg())
        self.glade.get_object("imageHolder").show()

    def on_streamBtn_toggled(self, widget):
        cam = VideoObject(0)
        frames = 3

        while frames > 0:
            self.on_addButton_clicked(widget)
            frames-=1

    def on_windowMain_destroy(self, widget):
        sys.exit(0)
    

def draw_pixbuf(widget, event):
    path = './gui/images/rect.png'
    pixbuf = gtk.gdk.pixbuf_new_from_file(path)
    widget.window.draw_pixbuf(widget.style.bg_gc[gtk.STATE_NORMAL], pixbuf, 0, 0, 0, 0)

letsgo = guiTester()
gtk.main()
