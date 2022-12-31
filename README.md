# "Website Silencer"

A python script to block certain websites using the hosts file. 

## First things first
To run the program, first change the file path of the website.txt file. The existence of the file is not necessary as it will be created if it doesn't exist.
If you running the code on something different than Windows, the hosts path should be changed accordingly. 

<img width="318" alt="Paths" src="https://user-images.githubusercontent.com/58997886/210122225-2e2ee097-3730-427f-9b55-117493fa6f7f.PNG">

Once the paths have been updated, simply run the main.py to start the program.

## How to use?
Using the Tkinter library a simple GUI is shown and allows for the simple adding and removal of website links. 

<img width="493" alt="Gui" src="https://user-images.githubusercontent.com/58997886/210121817-b7aa1440-7cc5-48b1-a6ba-39c208537f23.PNG">

To "block" a website, insert the website inside the entry and press the Block button or simply press Enter. The website will be added to the hosts file and will be shown within the GUI.

To "remove" a website, select the row within the GUI you want to remove and press the Unlock button or the "delete" key. 
