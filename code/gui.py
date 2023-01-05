import tkinter as tk
from tkinter.messagebox import askokcancel
from tkinter import ttk
import webbrowser
import os
import pyperclip

from blocker import BlockedList


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
        extra1 = ExtraFrame(self.root, self.different_frames[1],main,website_blocker)



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
        self.button_quit = ttk.Button(self.FRAME_down_right,text="quit", command = quit)

        self.button_website_test.grid(column=0,row=0,padx=(0,10))
        self.button_unblock.grid(column=1,row=0,padx=(0,0),sticky="w")
        self.button_quit.grid(column=2,row=0,padx=(10,0),sticky="w")

        #initializes the bindings
        self.bindings_main()


    def command_block(self):
        """Adds the url, redirection and date to the treeviewer"""
        url = self.website_entry_text.get()
        website,redirect,*date = self.website_blocker.block_website(url)
        self.tree_viewer.insert("",'end',values=(website,redirect,date))
        self.website_entry_text.set("")

    def command_unblock(self):
        """Removes the selected row out of the treeviewer"""
        try:
                        
            selectedItem = self.tree_viewer.selection()[0]
            url = self.tree_viewer.item(selectedItem)['values'][0]
            current_idx = self.tree_viewer.index(selectedItem)

            self.website_blocker.unblock_website(url,current_idx)
            selection= self.tree_viewer.selection()[0]
            self.tree_viewer.delete(selection)
            
        
        except IndexError:
            print( 'Nothing selected' )


    
    def bindings_main(self):
        self.entry.bind('<Return>',lambda e: self.command_block())
        self.tree_viewer.bind('<Delete>',lambda e: self.command_unblock())
        self.tree_viewer.bind('<Control-c>',lambda e: self.copy_url())
        self.root.bind('<Escape>',lambda e: quit())
      
    def reset_treeviewer(self):
        """Removes all itmes from the treeviewer"""
        self.tree_viewer.delete(*self.tree_viewer.get_children())
    
    def open_website(self) -> None:
        """Opens the selected row in a chrome browser, if you are able to surf to the selected website."""

        # Sets the webbrowser to Chrome
        webbrowser.register('chrome',None, webbrowser.BackgroundBrowser("C:\Program Files\Google\Chrome\Application\chrome.exe"))
        try:
            selectedItem = self.tree_viewer.selection()[0]
            url = self.tree_viewer.item(selectedItem)['values'][0]
            webbrowser.get('chrome').open_new(url)
        except IndexError:
            pass
        
    def copy_url(self):
        selectedItem = self.tree_viewer.selection()

        url_each_selection = "\n".join([self.tree_viewer.item(i)['values'][0] for i in selectedItem]) #into string because pyperclip can't copy list
        pyperclip.copy(url_each_selection)
        
          





class ExtraFrame():
    
    def __init__(self,root,frame,obj_main,obj_website_blocker) -> None:
        
        
        self.website_blocker = obj_website_blocker
        self.root = root
        self.frame = frame
        self.obj_main = obj_main
        self.list_obj = BlockedList()
        


         # Window split into 2 FRAMES:  self.FRAME_LEFT and self.FRAME_RIGHT
        self.FRAME_LEFT = tk.Frame(self.frame)
        self.FRAME_LEFT.pack(pady=10,anchor="nw",fill="y",side="left")

        self.FRAME_RIGHT = tk.Frame(self.frame)
        self.FRAME_RIGHT.pack(fill="y",side="right",anchor='ne',pady = 10)

        # Create a frame inside the self.FRAME_LEFT at the top self.FRAME_LEFT_up
        self.FRAME_LEFT_up = tk.Frame(self.FRAME_LEFT)
        self.FRAME_LEFT_up.pack(pady=10,anchor="nw")

        self.label_dns = ttk.Label(self.FRAME_LEFT_up,text="Flush your dns:")
        self.label_reset = ttk.Label(self.FRAME_LEFT_up,text="Reset list:")
        self.label_change_redirection = ttk.Label(self.FRAME_LEFT_up,text="Change redirection:",foreground="grey")
        self.label_state_redirection = ttk.Label(self.FRAME_LEFT_up,text="base redirection")


        self.check_redirection_state = tk.IntVar(value=1)
        self.button_block = ttk.Button(self.FRAME_LEFT_up,text='Flush',command=self.flusher)
        self.button_reset = ttk.Button(self.FRAME_LEFT_up,text='Reset',command=self.reset)
        self.checkbutton_state_redirection  = ttk.Checkbutton(self.FRAME_LEFT_up,variable=self.check_redirection_state,command=self.state_rediraction)
        

        self.redirection_str = tk.StringVar(value="0.0.0.0")
        self.entry_redirection = ttk.Entry(self.FRAME_LEFT_up,textvariable=self.redirection_str,state="disabled")
        self.button_redirection = ttk.Button(self.FRAME_LEFT_up,text="OK",state="disabled",command=self.redirection_changer)
        self.label_current_redirection = ttk.Label(self.FRAME_LEFT_up,text="Currect redirection: ")
        self.label_current_redirection_var = ttk.Label(self.FRAME_LEFT_up,text=self.website_blocker.redirection)

        self.canvas1 = tk.Canvas(self.FRAME_LEFT_up,width=400,height=3)

        self.label_state_redirection.grid(column=0,row=0,padx=10,sticky="w") # label : "base redirection"
        self.checkbutton_state_redirection.grid(column=1,row=0,)
        
        self.label_change_redirection.grid(column=0,row=1,padx=10,sticky="w") # Label : "Change redirection:"
        self.entry_redirection.grid(column=1,row=1)
        self.button_redirection.grid(column=2,row=1)

        self.label_current_redirection.grid(column=0,row=2,padx=10,pady=(0,5))
        self.label_current_redirection_var.grid(column=1,row=2,padx=10,pady=(0,5))
        
        self.canvas1.grid(column=0,row=3,columnspan=3,sticky="w")
        self.canvas1.create_line(10,2,400,2,fill="#D6D5D5")

        self.label_reset.grid(column=0,row=4,padx=10,pady=(5,0),sticky="w") # label : "Reset everything:"
        self.button_reset.grid(column=1,row=4,pady=(5,0))
        
        self.label_dns.grid(column=0,row=5,padx=10,sticky="w") # label : "Flush your dns:"
        self.button_block.grid(column=1,row=5)

        # Create a frame inside the self.FRAME_LEFT at the top self.FRAME_LEFT_BOTTOM       
        self.FRAME_BOTTOM = tk.Frame(self.FRAME_LEFT)
        self.FRAME_BOTTOM.pack(anchor="w",pady=(10,0))

        self.check_text = tk.IntVar(value=1)
        
        
        self.text_list_text = tk.StringVar()
        self.text_list = tk.Text(self.FRAME_BOTTOM,width=50,height=10,wrap="word")
       
        self.text_list.grid(column=0,row=1,columnspan=3,padx=(10,0))

        # Create a frame inside the self.FRAME_LEFT at the top self.FRAME_BOTTOM_BUTTONS
        self.FRAME_BOTTOM_BUTTONS = tk.Frame(self.FRAME_LEFT,width=640)
        self.FRAME_BOTTOM_BUTTONS.pack(side="left")

        self.button_blockall = ttk.Button(self.FRAME_BOTTOM_BUTTONS,text="Block list",command = self.add_blocked_list)
        self.button_default = ttk.Button(self.FRAME_BOTTOM_BUTTONS,text="add list",command=self.append_blocked_list)
        
        self.button_set_default = ttk.Button(self.FRAME_BOTTOM_BUTTONS,text="quit",command=quit)
        

        self.button_set_default.pack(side="left",padx = (10,145))
        self.button_blockall.pack(side="right",anchor="e")
        self.button_default.pack(side="right",padx = 15)


        
        #Create top frame for rigth side
        self.frame_right_up = tk.Frame(self.FRAME_RIGHT)
        self.frame_right_up.pack(fill="x")

        self.entry_save_var = tk.StringVar()
        self.entry_save = ttk.Entry(self.frame_right_up,textvariable=self.entry_save_var)
        self.button_save = ttk.Button(self.frame_right_up,text="New",command=self.save_name)

        self.entry_save.pack(side="left",pady=(10,0),padx=(10,0))
        self.button_save.pack(side="right",pady=(10,0),padx=(0,10))

        self.frame_right_down = tk.Frame(self.FRAME_RIGHT)
        self.frame_right_down.pack(pady=(14,0),padx=10)

        self.columns = ["saved_presets"]
        self.tree_viewer_presets = ttk.Treeview(self.frame_right_down,show='',columns=self.columns,height=15)
        self.tree_viewer_presets.pack()

        for name in self.list_obj.saved_preset_name_list:
            self.tree_viewer_presets.insert("",'end',values=(name.replace(" ","\ ")))
        
        self.popup = tk.Menu(self.root, tearoff=0)

        #Adding Menu Items
        self.popup.add_command(label="Delete",command=self.treeviewer_delete)

        self.state_tree = True
        self.bindings()

    def bindings(self):
        self.tree_viewer_presets.bind("<Button-3>", self.menu_popup)
        self.tree_viewer_presets.bind("<Motion>",self.hovering_tree_viewer)
        self.tree_viewer_presets.bind("<Button-1>",lambda e:self.when_click_tree())
        self.tree_viewer_presets.bind("<Leave>",lambda e:self.leaving_tree())
        self.tree_viewer_presets.bind('<Enter>',lambda e:self.on_entering())
        self.tree_viewer_presets.bind('<Delete>',lambda e:self.treeviewer_delete())
        
        self.entry_save.bind('<Return>',lambda e:  self.save_name())

        self.text_list.bind("<Enter>",lambda e: self.deselect())
    
    def when_click_tree(self):
        
        if self.state_tree:
            self.state_tree = False
            self.current_list = None
            self.insert_preset_list()
    
    def deselect(self):
        try:
            item_selected = self.tree_viewer_presets.selection()[0]
            self.tree_viewer_presets.selection_remove(item_selected)
        except:
            pass
            
        
    def on_entering(self):
        self.current_list = self.text_list.get('1.0','end')
    
    def leaving_tree(self):
        self.state_tree = True
        
        
    def menu_popup(self,event):
        """allows for a menu pop up when right clicking a presets inside the treeviewer"""
        iid = self.tree_viewer_presets.identify_row(event.y)

        if iid:
            self.tree_viewer_presets.selection_set(iid)
            self.popup.post(event.x_root, event.y_root)            

            
    def hovering_tree_viewer(self,event):
        """Shows the urls within the specific presets when hovering over it"""
        
        if self.state_tree:
            iid = self.tree_viewer_presets.identify_row(event.y)
            
            if iid:
                self.tree_viewer_presets.selection_set(iid)
                self.insert_preset_list()

    def flusher(self):
        """Flushes the dns"""
        
        os.system('cmd /c "ipconfig /flushdns"')

    def reset(self):
        """Resets all the files of blocked websites"""

        self.button_reset['state'] = tk.DISABLED
        user_response = askokcancel(title="Warning", message="You are about to reset ALL blocked sites")
                
        if user_response:
            self.website_blocker.resetter()
            self.obj_main.reset_treeviewer()
                      
        self.button_reset['state'] = tk.NORMAL
    
    def treeviewer_delete(self):
        """Deletes a value from the treeviewer"""
        item_selected = self.tree_viewer_presets.selection()[0]
        self.list_obj.delete(self.tree_viewer_presets.item(item_selected)['values'][0])
        self.tree_viewer_presets.delete(item_selected)
        

    def state_rediraction(self):
        """Unlocks the Entry field to choose a new redirection value"""

        result = self.check_redirection_state.get()
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
            self.label_current_redirection_var.config(text=base_redirection)
    
    def redirection_changer(self):
        """Changes the redirection value inside the Blocker object"""

        result = self.redirection_str.get()

        if result != "":
            self.website_blocker.redirection = result 
            self.obj_main.label_redirection_show.config(text=result)
            self.label_current_redirection_var.config(text=result)
         
    def insert_preset_list(self,lst=None):
        """Inserts the preset list of the saved presets"""
        self.text_list.delete("1.0","end")
        
        if lst:
            n_lst = [i+"\n" for i in lst.split('\n')]
        
        else:
            selectedItem = self.tree_viewer_presets.selection()[0]
            name = self.tree_viewer_presets.item(selectedItem)['values'][0]
            name.replace("\ "," ")
            
            self.list_obj.name_saver(name)

        list_to_insert = n_lst if lst != None else self.list_obj.get_presets_list()  

        #Then it adds the new list it receives
        default = list_to_insert
        if default:
            for x,i in enumerate(default):
                if i != "":
                    self.text_list.insert(f"{x+1}.0",i)


    def save_name(self):
        """grabes a name, passes it to the BlockedList obj and puts it into tree viewer"""
        given_list_websites = self.text_list.get('1.0','end').split("\n")
        name = self.entry_save_var.get()
        name_absence = self.list_obj.check_availability_name(name)

        if name_absence != None:
            if name_absence:
                ok_or_not = askokcancel(title="Warning", message="You are about to overwrite an existing preset")
                if ok_or_not:
                    self.list_obj.name_saver(name)
                    self.list_obj.delete(name)
                    self.list_obj.save_new_preset(given_list_websites)
            else:
                self.list_obj.name_saver(name)
                self.list_obj.save_new_preset(given_list_websites)
                self.tree_viewer_presets.insert("",'end',values=(name.replace(" ", "\ ")))
                self.entry_save_var.set("")          

            

    def add_blocked_list(self):
        """Adds the list to the tree viewer by removing everything currently in"""

        self.website_blocker.resetter()
        self.obj_main.reset_treeviewer()
        
        list_for_tree = self.website_blocker.block_list_website(self.text_list.get('1.0','end').split("\n"))
        

        for row_input in list_for_tree:
            website,redirect,*date = row_input
            self.obj_main.tree_viewer.insert("",'end',values=(website,redirect,date))
        
        self.text_list.delete("1.0","end") 

    def append_blocked_list(self):
        """Adds the list to the tree viewer"""

        list_for_tree = self.website_blocker.block_list_website(self.text_list.get('1.0','end').split("\n"))

        for row_input in list_for_tree:
            website,redirect,*date = row_input
            self.obj_main.tree_viewer.insert("",'end',values=(website,redirect,date))
        
        self.text_list.delete("1.0","end")



    
if __name__ == "__main__":
    print("This is the gui python file")
    