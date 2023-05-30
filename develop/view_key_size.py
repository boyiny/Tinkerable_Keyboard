import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

class View_key_size:
    def __init__(self, controller, viewKeypad) -> None:
        self.controller = controller
        self.viewKeypad = viewKeypad
        self.keySizeDict = {
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





    
    def _close(self):
        self.root.destroy()

    def _save_key_size_settings(self):
        print(self.keySizeDict)
        self.viewKeypad.load_key_size(self.keySizeDict)
        self.root.destroy()
    
    def _callback_x(self, var, index, mode): #  caption, x
        print("Trace variable", var)
        # self.keySizeDict[caption][0] = x
        # print(caption, 'x = ', x)

    # def _callback_y(self, caption, y):
    #     self.keySizeDict[caption][1] = y
    #     print(caption, 'y = ', y)

    

    def _update_key_x_y(self, caption):
        # print(self.keySizeDict[caption][0], self.keySizeDict[caption][1])
        def _sv_x_callback(var, index, mode):
            print ("x = ", self.keySize1_x_Entry_sv.get())
            if self.keySize1_x_Entry_sv.get() != '':
                self.keySizeDict[caption][0] = int(self.keySize1_x_Entry_sv.get())
            print(self.keySizeDict)
                
        def _sv_y_callback(var, index, mode):
            print ("y = ", self.keySize1_y_Entry_sv.get())
            if self.keySize1_y_Entry_sv.get() != '':
                self.keySizeDict[caption][0] = int(self.keySize1_y_Entry_sv.get())
            print(self.keySizeDict)

        self.keySize1_x_Entry_sv = tk.StringVar(self.baseFrame, self.keySizeDict[caption][0])
        self.keySize1_y_Entry_sv = tk.StringVar(self.baseFrame, self.keySizeDict[caption][1])

        self.keySize1_x_Entry_sv.trace_add('write', _sv_x_callback) # self._sv_x_callback(sv=self.keySize1_x_Entry_sv, caption=caption)
        self.keySize1_y_Entry_sv.trace_add('write', _sv_y_callback)

        # print(self.keySize1_x_Entry_sv.get())

        updatedKeySize_x = tk.Entry(self.baseFrame, width=21, textvariable=self.keySize1_x_Entry_sv)
        updatedKeySize_x.grid(sticky="E", column=1, row=1)
        updatedKeySize_y = tk.Entry(self.baseFrame, width=21, textvariable=self.keySize1_y_Entry_sv)
        updatedKeySize_y.grid(sticky="E", column=2, row=1)

        print(updatedKeySize_x.get())
        


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

        # self.edditedKeySizeWidgetList = []
        # for i in range(5):
        #     self.edditedKeySizeWidgetList.append(self._create_key_size_setting_combobox_entry(row=i+1))

        
        # row 1
        keySize1_Entry_sv_Dict = {}
        
        # self.keySize1_x_Entry_sv.trace_add('write', lambda: self.sv_callback(sv=self.keySize1_x_Entry_sv))
        # self.keySize1_x_Entry_sv()
        self.keySize1_x_Entry = tk.Entry(self.baseFrame, width=21, textvariable='')
        self.keySize1_x_Entry.grid(sticky="E", column=1, row=1)
        
        # self.keySize1_y_Entry_sv.trace_add('write', lambda: self.sv_callback(sv=self.keySize1_y_Entry_sv))
        self.keySize1_y_Entry = tk.Entry(self.baseFrame, width=21, textvariable='')
        self.keySize1_y_Entry.grid(sticky="E", column=2, row=1)

        keySize1Combobox = ttk.Combobox(self.baseFrame, width=21, values=list(self.keySizeDict.keys()), state="readonly") # , validate='focusout', validatecommand=(self.root.register(check_okay), '%P')
        keySize1Combobox.grid(sticky="E", column=0, row=1)

        # keySize1_Entry_sv_Dict['caption_combobox'] = keySize1Combobox
        # keySize1_Entry_sv_Dict['x_sv'] = keySize1_x_Entry_sv
        # keySize1_Entry_sv_Dict['y_sv'] = keySize1_y_Entry_sv 

        # keySize_Entry_sv_Dict_List.append(keySize1_Entry_sv_Dict)

        keySize1Combobox.bind('<<ComboboxSelected>>', lambda event: self._update_key_x_y(caption=keySize1Combobox.get()))

        # # row 2
        # keySize2_x_Entry = tk.Entry(self.baseFrame, width=21, textvariable='')
        # keySize2_x_Entry.grid(sticky="E", column=1, row=2)
        # keySize2_y_Entry = tk.Entry(self.baseFrame, width=21, textvariable='')
        # keySize2_y_Entry.grid(sticky="E", column=2, row=2)

        # keySize2Combobox = ttk.Combobox(self.baseFrame, width=21, values=list(self.keySizeDict.keys()), state="readonly") # , validate='focusout', validatecommand=(self.root.register(check_okay), '%P')
        # keySize2Combobox.grid(sticky="E", column=0, row=2)

        # keySize2Combobox.bind('<<ComboboxSelected>>', lambda event: self._update_key_x_y(keySize_caption=keySize2Combobox.get(), row=2))

        # # row 3
        # keySize3_x_Entry = tk.Entry(self.baseFrame, width=21, textvariable='')
        # keySize3_x_Entry.grid(sticky="E", column=1, row=3)
        # keySize3_y_Entry = tk.Entry(self.baseFrame, width=21, textvariable='')
        # keySize3_y_Entry.grid(sticky="E", column=2, row=3)

        # keySize3Combobox = ttk.Combobox(self.baseFrame, width=21, values=list(self.keySizeDict.keys()), state="readonly") # , validate='focusout', validatecommand=(self.root.register(check_okay), '%P')
        # keySize3Combobox.grid(sticky="E", column=0, row=3)

        # keySize3Combobox.bind('<<ComboboxSelected>>', lambda event: self._update_key_x_y(keySize_caption=keySize3Combobox.get(), row=3))

        # # row 4
        # keySize4_x_Entry = tk.Entry(self.baseFrame, width=21, textvariable='')
        # keySize4_x_Entry.grid(sticky="E", column=1, row=4)
        # keySize4_y_Entry = tk.Entry(self.baseFrame, width=21, textvariable='')
        # keySize4_y_Entry.grid(sticky="E", column=2, row=4)

        # keySize4Combobox = ttk.Combobox(self.baseFrame, width=21, values=list(self.keySizeDict.keys()), state="readonly") # , validate='focusout', validatecommand=(self.root.register(check_okay), '%P')
        # keySize4Combobox.grid(sticky="E", column=0, row=4)

        # keySize4Combobox.bind('<<ComboboxSelected>>', lambda event: self._update_key_x_y(keySize_caption=keySize4Combobox.get(), row=4))

        # # row 5
        # keySize5_x_Entry = tk.Entry(self.baseFrame, width=21, textvariable='')
        # keySize5_x_Entry.grid(sticky="E", column=1, row=5)
        # keySize5_y_Entry = tk.Entry(self.baseFrame, width=21, textvariable='')
        # keySize5_y_Entry.grid(sticky="E", column=2, row=5)

        # keySize5Combobox = ttk.Combobox(self.baseFrame, width=21, values=list(self.keySizeDict.keys()), state="readonly") # , validate='focusout', validatecommand=(self.root.register(check_okay), '%P')
        # keySize5Combobox.grid(sticky="E", column=0, row=5)

        # keySize5Combobox.bind('<<ComboboxSelected>>', lambda event: self._update_key_x_y(keySize_caption=keySize5Combobox.get(), row=5))


        cancelBtn = ttk.Button(self.baseFrame, text="Confirm", command=self._save_key_size_settings).grid(sticky="W", ipadx=10, ipady=10, column=2, row=6)
        confirmBtn = ttk.Button(self.baseFrame, text="Cancel", command=self._close).grid(sticky="E", ipadx=10, ipady=10, column=2, row=6)

        self.root.mainloop()

    def get_key_size_dict(self):
        pass