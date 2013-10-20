#!/usr/bin/python

import pygtk
pygtk.require('2.0')
import gtk

import sys
import json
from multiprocessing import Process, Queue
import signal
from SimpleCV import Camera


def draw_pixbuf(widget, event, path):
    pixbuf = gtk.gdk.pixbuf_new_from_file(path)
    widget.window.draw_pixbuf(widget.style.bg_gc[gtk.STATE_NORMAL], pixbuf, 0, 0, 0, 0)


class guiHolder:

    def __init__(self):
        self.gladefile = "./gui/login.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.gladefile)
        self.builder.connect_signals(self)
        self.builder.get_object("background").connect('expose-event', draw_pixbuf, './gui/images/loginBackground.png')

        self.mainWindow = self.builder.get_object("windowMain")
        self.mainWindow.set_size_request(1600, 900)
        self.mainWindow.set_title("EyeTracking - Login")

        self.mainWindow.show_all()

    def on_windowMain_delete_event(self, event):
        gtk.main_quit()
        sys.exit(0)

    def on_windowMain_destroy(self, event):
        sys.exit(0)

    def draw_newScreen(self, pathToBackground,  pathToGlade, windowTitle):
        for obj in self.mainWindow.get_children():
                self.mainWindow.remove(obj)

        self.gladefile = pathToGlade
        self.builder.add_objects_from_file(self.gladefile, ["background"])
        self.builder.connect_signals(self)
        self.builder.get_object("background").connect('expose-event', draw_pixbuf, pathToBackground)
        self.mainWindow.add(self.builder.get_object("background"))
        self.mainWindow.set_title(windowTitle)

    def on_newUser_BTN_clicked(self, event):
        # Draw the next screen
        self.draw_newScreen("./gui/images/loginBackground.png",
                            "./gui/userReg.glade",
                            "EyeTracking - New User Registration")

    def on_next_BTN_userReg_clicked(self, event):

        # Store the credentials in the main index and create a new file
        firstName = self.builder.get_object("firstName_entry").get_text()
        lastName = self.builder.get_object("lastName_entry").get_text()

        with open("users/userIndex.txt", "r+") as f:
            # Get last index from last user
            line = 0
            for line in f.readlines():
                pass
            lastIndex = int(line[:3])

            # Put new user in file
            f.write(str(lastIndex+1).zfill(3)+" - "+firstName+" "+lastName+"\n")

        # Create new user file
        with open("users/"+str(lastIndex+1)+" - "+firstName+" "+lastName, "a") as f:
            self.userInfo = {"id": lastIndex, "firstName": firstName, "lastName": lastName}
            f.write(json.dumps(self.userInfo))

        # Draw the next screen
        self.draw_newScreen("./gui/images/usageExample.png",
                            "./gui/usageExample.glade",
                            "EyeTracking - Usage Example")

    def on_next_BTN_usageExample_clicked(self, event):

        # Draw the next screen
        adjustment = gtk.Adjustment(value=0, lower=0, upper=255, step_incr=1, page_incr=10, page_size=0)
        self.draw_newScreen("./gui/images/regularBackground.png",
                            "./gui/binarization.glade",
                            "EyeTracking - Binarization")

        self.scale = gtk.HScale(adjustment)
        self.scale.connect("value-changed", self.updateBinarization)
        #self.scale.set_update_policy(gtk.UPDATE_DELAYED)
        self.builder.get_object("scaleHolder").add(self.scale)
        self.mainWindow.set_keep_below(True)
        self.displayImage = self.builder.get_object("pupil_Image")
        self.mainWindow.show_all()

        # Show Example dialog
        self.display_binExample()

        # Go cam
        # Prepare Queue for passing binarization value and images
        self.queue = Queue()

        self.camProcess = Process(target=self.startCAM)
        self.camProcess.start()

    def updateBinarization(self, event):
        try:
            self.queue.put(self.scale.get_value())
        except ValueError:
            return 0

    def startCAM(self):
        cam = Camera()
        #cam = VirtualCamera("pupilTest.mp4", "video", 300)

        binarizationValue = 0

        while True:
            if not self.queue.empty():
                binarizationValue = self.queue.get()
            img = cam.getImage().binarize(binarizationValue)
            img.show()

    def display_binExample(self):
        # Exhibit a example box
        userMsg = "Adjust the threshold value so that the pupil looks as similar as the presented image."
        dialog = gtk.MessageDialog(self.mainWindow,
                                   gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_WARNING,
                                   gtk.BUTTONS_OK,
                                   userMsg)
        # Set example image
        img = gtk.Image()
        img.set_from_file("./gui/images/pupilExample.png")
        img.show()
        dialog.set_image(img)
        dialog.run()
        dialog.destroy()

    def on_next_BTN_binarization_clicked(self, event):
        #Terminate cam process
        self.camProcess.terminate()
        self.camProcess.exitcode == -signal.SIGTERM

        #Get binarization preference and save
        val = self.scale.get_value()
        self.userInfo["binarization"] = val

        #Save info in users profile
        with open("users/"+str(self.userInfo["id"])+" - "+self.userInfo["firstName"]+" "+self.userInfo["lastName"], "w") as f:
            f.write(json.dumps(self.userInfo))

        #Create Next Window

letsgo = guiHolder()
gtk.main()
