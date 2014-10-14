from tkinter import Button, Label, Frame, StringVar, INSERT, END, SEL
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from tkinter.scrolledtext import ScrolledText
from random import randrange, choice
from re import sub, split


class SpinDelight(Frame):

    def __init__(self):
        Frame.__init__(self)
        self.master.geometry("1020x600+150+50")
        self.master.title("Spin Delight 1.0 - Copyright (c) Robin Thomas")
        self.master.resizable(0,0)
        self.grid()
        self.brwe = Button(self, text = "Browse", command = self.open_file, width = 10, relief = "groove")
        self.rtxt = Label(self, text="Input Text:")
        self.txt1 = ScrolledText(self, width = 50, height = 25)
        self.txt1.bind("<Control-Key-a>", self.select_all_txt1)
        self.txt1.bind("<Control-Key-A>", self.select_all_txt1)
        self.spin = Button(self, text = "Spin", command = self.spin_file, width = 10, relief = "groove")
        self.stxt = Label(self, text="Spun Text:")
        self.txt2 = ScrolledText(self, width = 50, height = 25)
        self.txt2.bind("<Control-Key-a>", self.select_all_txt2)
        self.txt2.bind("<Control-Key-A>", self.select_all_txt2)
        self.brwe.grid(row = 2, column = 2, pady = 15)
        self.rtxt.grid(row = 2, column = 0, padx = 25)
        self.txt1.grid(row = 3, column = 0, columnspan = 10, padx = 25)
        self.spin.grid(row = 3, column = 12)
        self.stxt.grid(row = 2, column = 13, padx = 25, pady = 5)
        self.txt2.grid(row = 3, column = 13, columnspan = 10, padx = 25)

    def select_all_txt1(self,event):
        self.txt1.tag_add(SEL, "1.0", END)
        self.txt1.mark_set(INSERT, "1.0")
        self.txt1.see(INSERT)
        return 'break'

    def select_all_txt2(self,event):
        self.txt2.tag_add(SEL, "1.0", END)
        self.txt2.mark_set(INSERT, "1.0")
        self.txt2.see(INSERT)
        return 'break'

    def open_file(self):
        fname = askopenfilename(filetypes=(("Text files", "*.txt"), ("All files", "*.*") ))
        if fname:
            try:
                self.txt1.delete(0.0, END)
                f = open(fname,'r')
                self.txt1.insert(INSERT,f.read())
            except:
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
    
    def spin_file(self):
        txt = self.txt1.get("1.0", END)
        self.txt2.delete(0.0, END)
        if len(txt):
            try:
                words = sub(r'([.,?])+', r' \1 ', sub(r'[^a-zA-Z0-9 .,?]+', ' ', txt)).split()
                w1 = words[0]
                z = [(words[j - 1], words[j]) for j in range(1, len(words))]
                values = self.generate_dict(z, w1)
                string = self.generate_sent(values)
                if len(string):
                    self.txt2.insert(INSERT, string)
                else:
                    showerror("Error", "Insufficient data to spin !!")
            except BaseException as e:
                showerror("Error", "Nothing to spin !!" + e)

                    
    def generate_dict(self, x, w1):
        values = {'.': [w1]}
        for (wa, wb) in x:
            if wa in values:
                values[wa].append(wb)
            else:
                values[wa] = [wb]
        return values


    def generate_sent(self, values):
        w1 = '.'
        w2 = choice(values[w1])
        string = w2
        values[w1].remove(w2)
        while values:
            w1 = w2
            if len(values[w1]):
                w2 = choice(values[w1])
            else:
                del values[w1]
                w1 = '.'
                break
            if w2 in ('.', ',', '?'):
                string += w2
            else:
                string += " " + w2
            values[w1].remove(w2)
        return string


if __name__ == "__main__": 
    SpinDelight().mainloop()
