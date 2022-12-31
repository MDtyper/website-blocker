import tkinter as tk
from gui import RootFrame
from blocker import Blocker

def main():
    website_blocker = Blocker()
    root = tk.Tk()
    root.title("Website Silencer")
    root.geometry("650x430")
    root.resizable(False, False)

    RootFrame(root,website_blocker)
    root.mainloop()



if __name__ == "__main__":
    main()