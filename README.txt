Dole Tsan, 2019-12-12

Document about SNAP scripts

snappyProcess.py contains the SNAP functions

mosaic.py is used to mosaic a directory of files together depending on FQ and date

processMosaic.py applies preprocessing to the files within the directory and then calls mosaic.py to mosaic them together

These can be run in command line by using the following:
'PATH/python.exe SCRIPTLOCATION/mosaic.py PATH/directoryfolder'

They can also be run inline on pythons console. An assertion will fail but it is in place to notify the command line users.
