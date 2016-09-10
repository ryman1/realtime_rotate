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
            if re.search(r'\.jpg$', event.src_path):
                global activejpg
                print('Active file changed to ' + event.src_path)
                activejpg = event.src_path

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
            im1 = Image.open(activejpg)
            im2 = im1.rotate(degrees, expand=True)
            im1.close()
            im2.save(activejpg)
            im2.close()
        except AttributeError:
            pass
        # Unpause the observer
        observer.schedule(handler, operatingpath, recursive=True)

    try:
        operatingpath = sys.argv[1]
    except IndexError:
        operatingpath = os.getcwd()
    activejpg = None
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
                        print('rotated ' + activejpg + ' ' + direction)
                    except TypeError:
                        print('no photo selected yet')
            time.sleep(.01)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
