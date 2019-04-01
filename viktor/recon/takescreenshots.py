import pyscreenshot as ImageGrab
from time import gmtime, strftime, sleep
if __name__ == '__main__':
    # part of the screen
    for k in range(100000):
       im = ImageGrab.grab(bbox=(0, 0, 1920, 1200))  # X1,Y1,X2,Y2
       im.save(strftime("screenshots/screenshot%Y-%m-%d %H:%M:%S.png", gmtime()))
       sleep(600)

#    im.show()
