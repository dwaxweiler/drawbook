# Prerequisites #

You have to install:
  1. [Python 2.7.x](http://www.python.org)
  1. [libavg](https://www.libavg.de/)
  1. [Python Imaging Library](http://www.pythonware.com/products/pil/)


# Configuration #

  1. Download the code.
  1. Open the file "DrawBook.py". A normal text editor is sufficient.
  1. Search the main() function nearly at the bottom of the file.
  1. Look at this line: DrawBook(folder='./', enableMultitouch=False, camDriver='firewire', camDevice='', camUnit=-1, camFormat="RGB", camFramerate=15, camFw800=False, camCapturewidth=640, camCaptureheight=480)
    * folder: You can change this argument to store the folder containing the drawings somewhere special.
    * enableMultitouch: Set this to True if you run it on a multitouch device.
    * cam`*`: Have a look at the [libavg reference](http://www.libavg.de/reference/current/areanodes.html#libavg.avg.CameraNode) and the [libavg ProgrammersGuide](http://www.libavg.de/wiki/ProgrammersGuide/CameraNode).


# Run #

Start this program by running the "DrawBook.py" from your console or IDE, like any other Python program.