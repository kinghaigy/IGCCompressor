This is made in Python so you'll need the python 3.x interpreter on your computer to be able to run it. Get python from here: https://www.python.org/downloads/

Once python has been installed, move the IGCCompressor.py file into the folder with the IGC file or the IGC file into the folder with the script. Either way, they need to be together. (They actually don't, but it's easier if they are).

Open a termainal/command prompt window in this folder. In windows, hold shift and right click inside the folder and click "Open command window here...". In OSX, you'll have to to open a terminal window and use 'cd' (change directory) commands to navigate to the folder. 

Squeeze your flight under 10000 feet:

python IGCCompressor --file my_flight_log.igc --height 10000 --units feet


Squeeze your flight under 2000 metres:

python IGCCompressor --file my_flight_log.igc --height 2000 --units metres


Make a 2D tracklog:

python IGCCompressor --file my_flight_log.igc --height 0 --units feet 


After compression, the new flight log will be named Compressed my_flight_log.igc