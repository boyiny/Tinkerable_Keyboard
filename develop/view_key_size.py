import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

class View_key_size:
    def __init__(self, controller, viewKeypad) -> None:
        self.controller = controller
        self.viewKeypad = viewKeypad
        self.keySizeDictDisplay = {
            'q': [80, 80],
            'w': [80, 80],
            'e': [80, 80],
            'r': [80, 80],
            't': [80, 80],
            'y': [80, 80],
            'u': [80, 80],
            'i': [80, 80],
            'o': [80, 80],
            'p': [80, 80],
            '<-': [80, 80],
            'a': [80, 80],
            's': [80, 80],
            'd': [80, 80],
            'f': [80, 80],
            'g': [80, 80],
            'h': [80, 80],
            'j': [80, 80],
            'k': [80, 80],
            'l': [80, 80],
            'Speak': [120, 80],
            'z': [80, 80],
            'x': [80, 80],
            'c': [80, 80],
            'v': [80, 80],
            'b': [80, 80],
            'n': [80, 80],
            'm': [80, 80],
            ',': [80, 80],
            '.': [80, 80],
            'Clear All': [130, 80],
            'Space': [300, 80]
        }
        self.keySizeDict = self.keySizeDictDisplay

    
    def _close(self):
        self.keySizeDict = self.keySizeDictDisplay
        self.root.destroy()

    def _save_key_size_settings(self):
        self.keySizeDictDisplay = self.keySizeDict
        # print(self.keySizeDictDisplay)
        self.viewKeypad.load_key_size(self.keySizeDictDisplay)
        self.root.destroy()
    

    def _update_key_x_y(self, caption):
        def _sv_x_callback(var, index, mode):
            if self.keySize1_x_Entry_sv.get() != '':
                self.keySizeDict[caption][0] = int(self.keySize1_x_Entry_sv.get())
                
        def _sv_y_callback(var, index, mode):
            if self.keySize1_y_Entry_sv.get() != '':
                self.keySizeDict[caption][1] = int(self.keySize1_y_Entry_sv.get())
       
        self.keySize1_x_Entry_sv = tk.StringVar(self.baseFrame, self.keySizeDict[caption][0])
        self.keySize1_y_Entry_sv = tk.StringVar(self.baseFrame, self.keySizeDict[caption][1])

        self.keySize1_x_Entry_sv.trace_add('write', _sv_x_callback) 
        self.keySize1_y_Entry_sv.trace_add('write', _sv_y_callback)

        updatedKeySize_x = tk.Entry(self.baseFrame, width=21, textvariable=self.keySize1_x_Entry_sv)
        updatedKeySize_x.grid(sticky="E", column=1, row=1)
        updatedKeySize_y = tk.Entry(self.baseFrame, width=21, textvariable=self.keySize1_y_Entry_sv)
        updatedKeySize_y.grid(sticky="E", column=2, row=1)
        

    def run(self):
        self.root = tk.Tk()
        self.root.title("Key Sizes")

        bigFont = tkFont.Font(family='Arial', size=20)
        self.root.option_add("*Font", bigFont)

        self.baseFrame = ttk.Frame(self.root)
        self.baseFrame.pack(padx=5, pady=5)

        ttk.Label(self.baseFrame, text="Caption").grid(sticky="W", column=0, row=0)
        ttk.Label(self.baseFrame, text="Edit Width").grid(sticky="W", column=1, row=0)
        ttk.Label(self.baseFrame, text="Edit Height").grid(sticky="W", column=2, row=0)

        # row 1
        self.keySize1_x_Entry = tk.Entry(self.baseFrame, width=21, textvariable='')
        self.keySize1_x_Entry.grid(sticky="E", column=1, row=1)
        self.keySize1_y_Entry = tk.Entry(self.baseFrame, width=21, textvariable='')
        self.keySize1_y_Entry.grid(sticky="E", column=2, row=1)

        keySize1Combobox = ttk.Combobox(self.baseFrame, width=21, values=list(self.keySizeDict.keys()), state="readonly") 
        keySize1Combobox.grid(sticky="E", column=0, row=1)

        keySize1Combobox.bind('<<ComboboxSelected>>', lambda event: self._update_key_x_y(caption=keySize1Combobox.get()))

        cancelBtn = ttk.Button(self.baseFrame, text="Confirm", command=self._save_key_size_settings).grid(sticky="W", ipadx=10, ipady=10, column=2, row=6)
        confirmBtn = ttk.Button(self.baseFrame, text="Cancel", command=self._close).grid(sticky="E", ipadx=10, ipady=10, column=2, row=6)

        self.root.mainloop()

    def get_key_size_dict(self):
        return self.keySizeDictDisplay