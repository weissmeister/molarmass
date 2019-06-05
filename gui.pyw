import tkinter as tk
import pyperclip
from tkinter import messagebox as msgbox
from common import calcmolmass


class Main(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title("Molecular Mass Calculator")
        self.checkboxchecked = tk.IntVar()

        lbl = tk.Label(self, text="Molecular Formula:")
        lbl.grid(row=0, column=0, padx=4, pady=4)

        box = tk.Entry(self, text="test")
        box.grid(row=0, column=1, padx=4, pady=4, columnspan=4, sticky = 'ew')
        self.box = box
        self.box.bind("<Return>", self.calcmass)

        btn = tk.Button(self, text="Calculate", command=self.calcmass)
        btn.grid(row=1, column=0, padx=4, pady=4, sticky='ew')

        lbl2 = tk.Label(self, text="Molar Mass:")
        lbl2.grid(row=1, column=1, padx=4, sticky='w')

        box2 = tk.Text(self, height=1, width=15, state='disabled')
        box2.grid(row=1, column=2, padx=0)
        self.box2 = box2

        btn2 = tk.Button(self, text="Copy", command=self.copy)
        btn2.grid(row=1, column=3, padx=4)

        chkbox = tk.Checkbutton(self, text="Auto-copy", variable=self.checkboxchecked)
        chkbox.grid(row=1, column=4, padx=0)

        self.grid()
        self.master.resizable(0, 0)

    def output(self, outputtxt):
        self.box2.configure(state='normal')
        self.box2.delete(1.0, tk.END)
        self.box2.insert(tk.END, outputtxt)
        self.box2.configure(state='disabled')

    def error(self, errortxt):
        msgbox.showwarning("Error!", errortxt)
        self.output("ERROR")

    def copy(self):
        molarmass = self.box2.get(1.0, tk.END)[:-1]  # Strip off newline that seems to exist for no reason
        if len(molarmass) > 0 and molarmass != "ERROR":
            pyperclip.copy(molarmass)

    def calcmass(self, dirtyfix=True):  # Dirty fix required to have correct amount of args on return keypress
        # Set up calling the function
        inputstr = self.box.get()
        if len(inputstr) == 0:
            return  # Do nothing

        # Call the function
        success, molmass, errormsg = calcmolmass(inputstr)
        if success:
            self.output(str(molmass))

            # Code to handle the auto-copy checkbox
            checked = self.checkboxchecked.get()
            if checked == 1:
                self.copy()
        else:
            self.error(errormsg)



mainprogram = Main()
mainprogram.mainloop()
