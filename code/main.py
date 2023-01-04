import tkinter as tk
import os

from gui import RootFrame
from blocker import Blocker


def create_dir():
    path = r'.\save_files'
    if not os.path.exists(path):
        os.mkdir(path)


def main():
    create_dir()
    website_blocker = Blocker()
    root = tk.Tk()
    
    root.title("Website Silencer")
    root.geometry("650x430")
    
    root.resizable(False, False)
    RootFrame(root,website_blocker)
    root.mainloop()
    


if __name__ == "__main__":
    main()
    
    