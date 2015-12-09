# drawbook
multi touch draw book with libavg and Python

Initial authors: Alexander Stenzel, Daniel Waxweiler, Hieu Nguyen, Lukas Löhle

## Prerequisites
You have to install:
 1. [Python 2.7.x](http://www.python.org)
 2. [libavg](https://www.libavg.de/)
 3. [Python Imaging Library](http://www.pythonware.com/products/pil/)

## Configuration
1. Download the code.
2. Open the file "DrawBook.py". A normal text editor is sufficient.
3. Search the main() function nearly at the bottom of the file.
4. Look at this line: DrawBook(folder='./', enableMultitouch=False, camDriver='firewire', camDevice='', camUnit=-1, camFormat="RGB", camFramerate=15, camFw800=False, camCapturewidth=640, camCaptureheight=480)
  * folder: You can change this argument to store the folder containing the drawings somewhere special.
  * enableMultitouch: Set this to True if you run it on a multitouch device.
  * cam`*`: Have a look at the [libavg reference](http://www.libavg.de/reference/current/areanodes.html#libavg.avg.CameraNode) and the [libavg ProgrammersGuide](http://www.libavg.de/wiki/ProgrammersGuide/CameraNode).

## Run
Start this program by running the "DrawBook.py" from your console or IDE, like any other Python program.


## Manual
After you started the program, you can see a Overview of all fields.
All undrawed field are showing the text "**touch here to draw**".
Once you touched on a drawed picture, you will get a bigger view of the touched one. One click on this picture again, the program will show you the overview again.
In case, you touching a free field, a drawing area will appear, with some tools on the left side.
For example, if you want to change the color, or the size of the pencil, easily touch on the pencil icon and choose your desired options!
Moreover, you can erase some or all parts of the picture with the rubber icon.
Furthermore, you can just let the webcam take a picture of you, if you want! After you are fine with your work, just touch the save button.
If not, then touch the cancel button and nothing will be saved.
Besides, if the field area misfits you, just scroll and choose another free field and get your individual and aspired position in the DrawBook!
Have fun :)

## Bedienungsanleitung (German manual)
Auf der Startseite kann man eine Teilübersicht aller gemalten Bilder und leeren Bilder betrachten.
Durch Berühren eines gemalten Bildes, wird eine Großaufname des Bildes gezeigt. Durch nochmaligen Berührens verkleinert sich das Bild wieder.
Noch freie Flächen werden mit einem "**touch here to draw**" gekennzeichnet.
Durch Berühren des Feldes, öffnet sich eine Zeichenfläche, wobei links Zeichen- und Webcamtools zur Verfügung stehen. Man kann Farbe und Größe des Stiftes auswählen, ggf. Fehler mit dem Radiergummi ausbessern und Speichern bzw. Abbrechen.
Wenn das Bild gespeichert wurde, kann es nicht mehr geändert werden, also gut überlegen ;).
Nachdem Sie Ihr Bild gespeichert haben, erscheint es in der Übersicht in dem Feld, welches Sie davor berüht hatten. Wenn Sie in einem ganz anderen Bereich zeichnen wollen, können Sie auch in der Bilderübersicht scrollen und somit ein anderes feld auswählen und dort Ihre Zeichenkünste, oder Ihre Meinung zum Ausdruck bringen. ;)
