# importing only those functions
# which are needed
from tkinter import * 
from tkinter.ttk import *
  
# creating tkinter window
root = Tk()
  
# Adding widgets to the root window
Label(root, text = 'GeeksforGeeks', font =(
  'Verdana', 15)).pack(side = TOP, pady = 10)
  
# Creating a photoimage object to use image
photo = PhotoImage(file = r"img/next.png")
  
# Resizing image to fit on button
photoimage = photo.subsample(5, 5)
  
# here, image option is used to
# set image on button
# compound option is used to align
# image on LEFT side of button
Button(root, text = 'Click Me !', image = photoimage,
                    compound = LEFT).pack(side = TOP)
  
mainloop()