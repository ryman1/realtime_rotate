from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re
import msvcrt
import time
import sys
import os

if __name__ == '__main__':
    # Create a watchdog observer that updates the file path of the image to be modified in real time.
    class MyFileSystemEventHandler(FileSystemEventHandler):
        def on_modified(self, event):
            # If the picture number is even, it's a front
            try:
                if int(re.search(r'(.)\.jpg$', event.src_path).group(1)) % 2 == 0:
                    global activejpgfront
                    print('Active file front changed to ' + event.src_path)
                    activejpgfront = event.src_path
                if not int(re.search(r'(.)\.jpg$', event.src_path).group(1)) % 2 == 0:
                    global activejpgback
                    print('Active file back changed to ' + event.src_path)
                    activejpgback = event.src_path
            except AttributeError:
                pass

    def kbfunc():
        x = msvcrt.kbhit()
        if x:
            # Getch acquires the character encoded in binary ASCII
            ret = ord(msvcrt.getch())
        else:
            ret = False
        return ret

    def rotate(degrees):
        # Pause the observer until all write operations are completed
        observer.unschedule(scheduledwatch)
        try:
            # Rotate front photo
            im1 = Image.open(activejpgfront)
            im2 = im1.rotate(degrees, expand=True)
            im1.close()
            im2.save(activejpgfront)
            # Rotate back photo
            im1 = Image.open(activejpgback)
            im2 = im1.rotate(degrees * -1, expand=True)
            im1.close()
            im2.save(activejpgback)
            im2.close()
        # For when no photo has been selected yet
        except AttributeError:
            pass
        # Unpause the observer
        observer.schedule(handler, operatingpath, recursive=True)

    try:
        operatingpath = sys.argv[1]
    except IndexError:
        operatingpath = os.getcwd()
    activejpgfront = None
    activejpgback = None
    observer = Observer()
    handler = MyFileSystemEventHandler()
    scheduledwatch = observer.schedule(handler, operatingpath, recursive=True)
    observer.start()
    try:
        print 'Listening for instructions...'
        # Loop to listen for keypresses
        while True:
            x = msvcrt.kbhit()
            if x:
                key = ord(msvcrt.getch())
            else:
                key = None
            if key:
                if key in (72, 75, 77, 80, 97, 100, 119, 115):
                    if key in (75, 97):
                        direction = 'left'
                        rotationdegrees = 90
                    elif key in (77, 100):
                        direction = 'right'
                        rotationdegrees = -90
                    elif key in (72, 80, 119, 115):
                        direction = '180 degrees'
                        rotationdegrees = 180
                    rotate(rotationdegrees)
                    try:
                        print('rotated ' + activejpgfront + ' ' + direction)
                    except TypeError:
                        print('no photo selected yet')
            time.sleep(.01)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
