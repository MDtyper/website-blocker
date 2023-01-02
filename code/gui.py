import tkinter as tk
from tkinter.messagebox import askokcancel
from tkinter import ttk
import webbrowser
import os
import datetime

from blocker import url_cleaner_validater


class RootFrame:
    """Creates the top frame and adds the frames in the notebook"""
    def __init__(self,root,website_blocker):
        self.root = root
        self.note_book = ttk.Notebook(self.root)
        self.note_book.pack()

        self.different_frame_names = ['Main',"Extra"]
        self.different_frames = []
        # Based on the first list, x amount of frames object is made and appended inside the different_frames list
        for frame_name in self.different_frame_names:
    
            self.frame = ttk.Frame(self.note_book, width=600, height=380)
            self.frame.pack(fill='both', expand=True)
            self.note_book.add(self.frame, text=frame_name)
            self.different_frames.append(self.frame)
        
        main = MainFrame(self.root, self.different_frames[0],website_blocker)
        ExtraFrame(self.root, self.different_frames[1],main,website_blocker)
        this is some change



class MainFrame():
    
    def __init__(self,root,frame,obj_website_blocker):        
        self.website_blocker = obj_website_blocker
        self.frame = frame
        self.root = root
        
        # Inside this frame I will add the Entry widget and 2 button widgets 
        self.FRAME_up = tk.Frame(self.frame)
        self.FRAME_up.pack(pady=30)

        self.website_entry_text = tk.StringVar()
        self.label_entry = ttk.Label(self.FRAME_up,text="Enter Website: ")
        self.entry = ttk.Entry(self.FRAME_up,width=50,textvariable=self.website_entry_text)
        self.button_block = ttk.Button(self.FRAME_up,text="Block",command=self.command_block)

        self.label_entry.pack(side="left")
        self.entry.pack(side='left', padx = (20,0))
        self.button_block.pack(side='left',padx=20)


        # Inside this frame the Treeviewer is added

        self.FRAME_middle = tk.Frame(self.frame)
        self.FRAME_middle.pack(pady=10)

        # The colums for the treeviewer
        self.columns = ["Blocked_website","Redirected_to","blocked_date"]

        # The tree viewer itself
        self.tree_viewer = ttk.Treeview(self.FRAME_middle,columns=self.columns, show='headings') 

        self.tree_viewer.heading('Blocked_website', text='Blocked website')
        self.tree_viewer.heading('Redirected_to', text='Redirected to')
        self.tree_viewer.heading('blocked_date', text='blocked date')


        self.tree_viewer.pack(padx=10)
        ###### FROM OBJECT CHECK ######
        for website, redirect, *date in self.website_blocker.blocked_websites:
            self.tree_viewer.insert("",'end',values=(website,redirect,date))

        # Inside this frame I will add the Entry widget and 2 button widgets 
        self.FRAME_down = tk.Frame(self.frame)
        self.FRAME_down.pack(fill='x')
        
        self.FRAME_down_left = tk.Frame(self.FRAME_down)
        self.FRAME_down_left.pack(side="left",anchor="w")
        
        self.label_redirection = ttk.Label(self.FRAME_down_left,text="redirected to: ") 
        self.label_redirection_show = ttk.Label(self.FRAME_down_left,text="0.0.0.0")
        
        self.label_redirection.grid(column=0,row=0,padx=(10,10))
        self.label_redirection_show.grid(column=1,row=0,padx=(0,0),columnspan=3)
        
        
        self.FRAME_down_right = tk.Frame(self.FRAME_down)
        self.FRAME_down_right.pack(pady=10,side="right",padx=(0,10),anchor="e")

        self.button_website_test = ttk.Button(self.FRAME_down_right,text="Test Website",command=self.open_website)
        self.button_unblock = ttk.Button(self.FRAME_down_right,text="Unblock",command=self.command_unblock)
        self.button_quit = ttk.Button(self.FRAME_down_right,text="quit", command = self.quit_apl)

        self.button_website_test.grid(column=0,row=0,padx=(0,10))
        self.button_unblock.grid(column=1,row=0,padx=(0,0),sticky="w")
        self.button_quit.grid(column=2,row=0,padx=(10,0),sticky="w")

        #initializes the bindings
        self.bindings_main()


    def command_block(self):
        """Adds the url, redirection and date to the treeviewer"""
        url = url_cleaner_validater(self.website_entry_text.get())
        website,redirect,*date = self.website_blocker.block_website(url)
        self.tree_viewer.insert("",'end',values=(website,redirect,date))
        self.website_entry_text.set("")

    def command_unblock(self):
        """Removes the selected row out of the treeviewer"""
        try:
                        
            selectedItem = self.tree_viewer.selection()[0]
            url = self.tree_viewer.item(selectedItem)['values'][0]
            url = url_cleaner_validater(url)
            current_idx = self.tree_viewer.index(selectedItem)

            self.website_blocker.unblock_website(url,current_idx)
            selection= self.tree_viewer.selection()[0]
            self.tree_viewer.delete(selection)
            
        
        except IndexError:
            print( 'Nothing selected' )


    
    def bindings_main(self):
        self.entry.bind('<Return>',lambda e: self.command_block())
        self.tree_viewer.bind('<Delete>',lambda e: self.command_unblock())
        self.root.bind('<Escape>',lambda e: self.quit_apl())
      

    def quit_apl(self):
        print(f'Program quit {datetime.datetime.now()}')
        quit()

    def reset_treeviewer(self):
        """Removes all itmes from the treeviewer"""
        self.tree_viewer.delete(*self.tree_viewer.get_children())
    
    def open_website(self) -> None:
        """Opens the selected row in a chrome browser"""

        # Sets the webbrowser to Chrome
        webbrowser.register('chrome',None, webbrowser.BackgroundBrowser("C:\Program Files\Google\Chrome\Application\chrome.exe"))
        try:
            selectedItem = self.tree_viewer.selection()[0]
            url = self.tree_viewer.item(selectedItem)['values'][0]
            webbrowser.get('chrome').open_new(url)
        except IndexError:
            print("Nothing is selected") 
        





class ExtraFrame():

    def __init__(self,root,frame,obj_main,obj_website_blocker) -> None:
        self.website_blocker = obj_website_blocker
        self.root = root
        self.frame = frame
        self.obj_main = obj_main
        

         # Inside this frame I will add the Entry widget and 2 button widgets 
        self.FRAME_LEFT = tk.Frame(self.frame)
        self.FRAME_LEFT.pack(pady=17,anchor="nw")

        self.label_dns = ttk.Label(self.FRAME_LEFT,text="Flush your dns:")
        self.label_reset = ttk.Label(self.FRAME_LEFT,text="Reset list:")
        self.label_change_redirection = ttk.Label(self.FRAME_LEFT,text="Change redirection:",foreground="grey")
        self.label_state_redirection = ttk.Label(self.FRAME_LEFT,text="base redirection")


        self.check_radio = tk.IntVar(value=1)
        self.button_block = ttk.Button(self.FRAME_LEFT,text='Flush',command=self.flusher)
        self.button_reset = ttk.Button(self.FRAME_LEFT,text='Reset',command=self.reset)
        self.checkbutton_state_redirection  = ttk.Checkbutton(self.FRAME_LEFT,variable=self.check_radio,command=self.state_rediraction)
        

        self.redirection_str = tk.StringVar(value="0.0.0.0")
        self.entry_redirection = ttk.Entry(self.FRAME_LEFT,textvariable=self.redirection_str,state="disabled")
        self.button_redirection = ttk.Button(self.FRAME_LEFT,text="OK",state="disabled",command=self.redirection_changer)


        self.label_dns.grid(column=0,row=0,padx=10,sticky="w") # label : "Flush your dns:"
        self.button_block.grid(column=1,row=0)
        self.label_reset.grid(column=0,row=1,padx=10,sticky="w") # label : "Reset everything:"
        self.button_reset.grid(column=1,row=1)
        
       
        self.label_state_redirection.grid(column=0,row=2,pady=(10,0),padx=10,sticky="w") # label : "base redirection"
        self.checkbutton_state_redirection.grid(column=1,row=2,pady=(10,0))
        
        self.label_change_redirection.grid(column=0,row=3,padx=10,sticky="w") # Label : "Change redirection:"
        self.entry_redirection.grid(column=1,row=3)
        self.button_redirection.grid(column=2,row=3)
        

    def flusher(self):
        
        os.system('cmd /c "ipconfig /flushdns"')

    def reset(self):
        """Resets all the files of blocked websites"""

        self.button_reset['state'] = tk.DISABLED
        user_response = askokcancel(title="Warning", message="You are about to reset the blocked sites")
                
        if user_response:
            self.website_blocker.resetter()
            self.obj_main.reset_treeviewer()
                      
        self.button_reset['state'] = tk.NORMAL
    
    def state_rediraction(self):
        """Unlocks the Entry field to choose a new redirection value"""

        result = self.check_radio.get()
        base_redirection = '0.0.0.0'

        if not result:
            self.entry_redirection["state"] = ["normal"]
            self.button_redirection["state"] = ["normal"]
            self.label_change_redirection.config(foreground="black")
            
        else:
            self.entry_redirection["state"] = ["disabled"]
            self.button_redirection["state"] = ["disabled"]
            self.label_change_redirection.config(foreground="grey")
            self.redirection_str.set(base_redirection)
            self.website_blocker.redirection = base_redirection
            self.obj_main.label_redirection_show.config(text=base_redirection)
    
    def redirection_changer(self):
        """Changes the redirection value inside the Blocker object"""

        result = self.redirection_str.get()

        if result != "":
            self.website_blocker.redirection = result 
            self.obj_main.label_redirection_show.config(text=result)
    
    
        


if __name__ == "__main__":
    print("This is the gui python file")
    
    
