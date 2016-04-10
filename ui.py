import tkinter as tk
import tkinter.filedialog as filedialog
from data_scrub import Record, read_records

class Scrub(tk.Frame):
    def __init__(self):
        super().__init__()
        self.option_add("*Listbox.Font", "courier")
        self.pack(expand=True, fill='both')
        self._edit_bar()
        self._listboxes()
        self._button_bar()

    def _edit_bar(self):
        fr_editbar = tk.Frame(master=self)
        fr_editbar.pack(side=tk.TOP, pady=10, expand=False, fill='y')

        label = tk.Label(fr_editbar, text='Edit Selected: ')
        label.pack(side=tk.LEFT, padx=10)
    
        cols = [r for r in Record.fields if r[0][0] != '<']
        for name,width in cols:
            fr = tk.Frame(fr_editbar)
            fr.pack(side=tk.LEFT, expand=False, padx=5)
            label = tk.Label(fr, text=name.replace('_',' ').capitalize())
            label.pack(side=tk.TOP, expand=False)
            tb = tk.Entry(fr, width=width)
            tb.pack(side=tk.TOP, expand=False)
            setattr(self, 'tb_' + name, tb)

        save = tk.Button(fr_editbar, text='Commit')
        save.pack(side=tk.RIGHT)


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

    def _listboxes(self):
        fr_data = tk.Frame(master=self)
        fr_data.pack(side=tk.TOP, expand=True, fill='both')

        # Good Data
        fr_scrubbed = tk.Frame(master=fr_data)
        fr_scrubbed.pack(side=tk.LEFT, expand=True, fill='both')

        label = tk.Label(fr_scrubbed, text = 'Scrubbed Records')
        label.pack(side=tk.TOP, expand=False, fill='both')

        self.lb_main = tk.Listbox(fr_scrubbed)
        self.lb_main.pack(side=tk.LEFT, expand=True, fill='both')

        # create and hook up scrollbar
        sb_main = tk.Scrollbar(fr_scrubbed)
        sb_main.pack(side=tk.RIGHT, fill='y')

        self.lb_main.config(yscrollcommand=sb_main.set)
        sb_main.config(command=self.lb_main.yview)

        # bind listbox click
        self.lb_main.bind("<<ListboxSelect>>", self.select_main_record)

        # Buttons Between for moving data
        fr_move_buttons = tk.Frame(master=fr_data)
        fr_move_buttons.pack(side=tk.LEFT, expand=False, fill='both')

        fr_mv_inv = tk.Frame(fr_move_buttons)
        fr_mv_inv.pack(side=tk.TOP, expand=True, fill='both')

        b_move_invalid = tk.Button(fr_mv_inv, text="<")
        b_move_invalid.bind("<Button-1>", self.move_selected_suspect)
        b_move_invalid.pack(side=tk.LEFT, expand=False)

        fr_mv_inv = tk.Frame(fr_move_buttons)
        fr_mv_inv.pack(side=tk.TOP, expand=True, fill='both')

        b_move_duplicate = tk.Button(fr_mv_inv, text="<")
        b_move_duplicate.bind("<Button-1>", self.move_selected_duplicate)
        b_move_duplicate.pack(side=tk.LEFT, expand=False)

        # Removed Data
        fr_removed = tk.Frame(master=fr_data)
        fr_removed.pack(side=tk.LEFT, expand=True, fill='both')

        ## Suspect Data
        label = tk.Label(fr_removed, text = 'Invalid Records')
        label.pack(side=tk.TOP, expand=False, fill='both')

        fr_suspect = tk.Frame(fr_removed)
        fr_suspect.pack(side=tk.TOP, expand=True, fill='both')

        self.lb_suspect = tk.Listbox(fr_suspect)
        self.lb_suspect.pack(side=tk.LEFT, expand=True, fill='both')

        # create and hook up scrollbar (this is why fr_suspect exists)
        sb_suspect = tk.Scrollbar(fr_suspect)
        sb_suspect.pack(side=tk.RIGHT, fill='y')

        self.lb_suspect.config(yscrollcommand=sb_suspect.set)
        sb_suspect.config(command=self.lb_suspect.yview)

        # bind listbox click
        self.lb_suspect.bind("<<ListboxSelect>>", self.select_suspect_record)

        ## Duplicate Data
        label = tk.Label(fr_removed, text = 'Duplicate Records')
        label.pack(side=tk.TOP, expand=False, fill='both')

        fr_duplicate = tk.Frame(fr_removed)
        fr_duplicate.pack(side=tk.TOP, expand=True, fill='both')

        self.lb_duplicate = tk.Listbox(fr_duplicate)
        self.lb_duplicate.pack(side=tk.LEFT, expand=True, fill='both')

        # create and hook up scrollbar (this is why fr_duplicate exists)
        sb_duplicate = tk.Scrollbar(fr_duplicate)
        sb_duplicate.pack(side=tk.RIGHT, fill='y')

        self.lb_duplicate.config(yscrollcommand=sb_duplicate.set)
        sb_duplicate.config(command=self.lb_duplicate.yview)

        # bind listbox click
        self.lb_duplicate.bind("<<ListboxSelect>>", self.select_duplicate_record)


    def refresh(self):
        listboxes_and_records = [
                (self.lb_main, self.good),
                (self.lb_suspect, self.bad),
                (self.lb_duplicate, self.dupes)]
        for lb,records in listboxes_and_records:
            lb.delete(0, tk.END)
            for r in records:
                lb.insert(tk.END, r.short_repr())

    def open_cb(self, event):
        filename = filedialog.askopenfilename(initialdir='.', 
                filetypes=(('Text File', '*.txt'), ('All Files', '*.*')),
                title='Choose File to Open')
        self.good, self.bad, self.dupes = read_records(filename)
        print(str(len(self.good)), str(len(self.bad)), str(len(self.dupes)))
        self.refresh()

    def save_cb(self, event):
        print("Save")

    def quit_cb(self, event):
        self.quit()

    def move_selected_duplicate(self, event):
        pass
    def move_selected_suspect(self, event):
        pass
    def fill_edit_boxes(self, listbox, records):
        record = records[listbox.curselection()[0]] 

        cols = [r[0] for r in Record.fields if r[0][0] != '<']
        for name in cols:
            tb = getattr(self, 'tb_' + name)
            data = getattr(record, name)
            tb.delete(0, tk.END)
            tb.insert(0, data)

    def select_main_record(self, event):
        self.fill_edit_boxes(self.lb_main, self.good)

    def select_suspect_record(self, event):
        self.fill_edit_boxes(self.lb_suspect, self.bad)

    def select_duplicate_record(self, event):
        self.fill_edit_boxes(self.lb_duplicate, self.dupes)

top = Scrub()
top.mainloop()
