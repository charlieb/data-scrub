import tkinter as tk

class Scrub(tk.Frame):
    def __init__(self):
        super().__init__()
        self.pack(expand=True, fill='both')
        self._edit_bar()
        self._listboxes()
        self._button_bar()

    def _edit_bar(self):
        fr_editbar = tk.Frame(master=self)
        fr_editbar.pack(side=tk.TOP, expand=False)

        label = tk.Label(fr_editbar, text='Edit')
        label.pack(side=tk.RIGHT)


    def _button_bar(self):
        buttonbar = tk.Frame(master=self)
        buttonbar.pack(side=tk.BOTTOM)

        open = tk.Button(buttonbar, text="Open")
        open.bind("<Button-1>", self.open_cb)
        open.pack(side=tk.LEFT)
        
        save = tk.Button(buttonbar, text="Save")
        save.bind("<Button-1>", self.save_cb)
        save.pack(side=tk.LEFT)

        quit = tk.Button(buttonbar, text="Quit")
        quit.bind("<Button-1>", self.quit_cb)
        quit.pack(side=tk.RIGHT)

    def open_cb(self, event):
        print("Open")
    def save_cb(self, event):
        print("Save")
    def quit_cb(self, event):
        print("Quit")

    def _listboxes(self):
        self.fr_data = tk.Frame(master=self)
        self.fr_data.pack(side=tk.TOP, expand=True, fill='both')

        # Good Data
        self.fr_scrubbed = tk.Frame(master=self.fr_data)
        self.fr_scrubbed.pack(side=tk.LEFT, expand=True, fill='both')

        label = tk.Label(self.fr_scrubbed, text = 'Scrubbed Records')
        label.pack(side=tk.TOP, expand=False, fill='both')

        self.lb_main = tk.Listbox(self.fr_scrubbed)
        self.lb_main.pack(side=tk.LEFT, expand=True, fill='both')

        self.lb_main.insert(tk.END, "This is a test")
        self.lb_main.insert(tk.END, "This is a test")
        self.lb_main.insert(tk.END, "This is a test")
        self.lb_main.insert(tk.END, "This is a test")

        # Buttons Between for moving data
        self.fr_move_buttons = tk.Frame(master=self.fr_data)
        self.fr_move_buttons.pack(side=tk.LEFT, expand=False, fill='both')

        fr_mv_inv = tk.Frame(self.fr_move_buttons)
        fr_mv_inv.pack(side=tk.TOP, expand=True, fill='both')

        b_move_invalid = tk.Button(fr_mv_inv, text="<")
        #b_move_invalid.bind("<Button-1>", self.move_selected_invalid)
        b_move_invalid.pack(side=tk.LEFT, expand=False)

        fr_mv_inv = tk.Frame(self.fr_move_buttons)
        fr_mv_inv.pack(side=tk.TOP, expand=True, fill='both')

        b_move_duplicate = tk.Button(fr_mv_inv, text="<")
        #b_move_duplicate.bind("<Button-1>", self.move_selected_duplicate)
        b_move_duplicate.pack(side=tk.LEFT, expand=False)

        
        # Removed Data
        self.fr_removed = tk.Frame(master=self.fr_data)
        self.fr_removed.pack(side=tk.LEFT, expand=True, fill='both')

        label = tk.Label(self.fr_removed, text = 'Invalid Records')
        label.pack(side=tk.TOP, expand=False, fill='both')

        self.lb_suspect = tk.Listbox(self.fr_removed)
        self.lb_suspect.pack(side=tk.TOP, expand=True, fill='both')

        self.lb_suspect.insert(tk.END, "This is a suspect")
        self.lb_suspect.insert(tk.END, "This is a suspect")
        self.lb_suspect.insert(tk.END, "This is a suspect")
        self.lb_suspect.insert(tk.END, "This is a suspect")

        label = tk.Label(self.fr_removed, text = 'Duplicate Records')
        label.pack(side=tk.TOP, expand=False, fill='both')

        self.lb_duplicate = tk.Listbox(self.fr_removed)
        self.lb_duplicate.pack(side=tk.TOP, expand=True, fill='both')

        self.lb_duplicate.insert(tk.END, "This is a duplicate")
        self.lb_duplicate.insert(tk.END, "This is a duplicate")
        self.lb_duplicate.insert(tk.END, "This is a duplicate")
        self.lb_duplicate.insert(tk.END, "This is a duplicate")

top = Scrub()
top.mainloop()
