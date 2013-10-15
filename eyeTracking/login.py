#!/usr/bin/python

import pygtk
pygtk.require('2.0')
import gtk
import time

import sys
from SimpleCV import Image, Camera

class guiHolder:

    def __init__(self):
        self.gladefile = "./gui/login.glade"
        self.glade = gtk.Builder()
        self.glade.add_from_file(self.gladefile)
        self.glade.connect_signals(self)
        self.glade.get_object("background").connect('expose-event', draw_pixbuf)
        self.glade.get_object("windowMain").set_size_request(640,500)

        self.glade.get_object("windowMain").show_all()

    def on_windowMain_delete_event(self, widget, event):
        gtk.main_quit()
        sys.exit(0)

    def on_windowMain_destroy(self, widget):
        sys.exit(0)
    

def draw_pixbuf(widget, event):
    path = './gui/images/rect.png'
    pixbuf = gtk.gdk.pixbuf_new_from_file(path)
    widget.window.draw_pixbuf(widget.style.bg_gc[gtk.STATE_NORMAL], pixbuf, 0, 0, 0, 0)

letsgo = guiHolder()
gtk.main()
