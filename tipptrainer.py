#!/usr/bin/env python3
# tk_tipptrainer.py

from tkinter import *
from tkinter import ttk
import tkinter as tk
import random
import gc

wordbook = open('Wortliste_deutsch.txt', 'r')

wordbook_local = []

for zeile in wordbook:
    wordbook_local.append(zeile.rstrip('\n'))  # readline bringt per Definition einen Zeilenumbruch mit

print(len(wordbook_local))
wordbook.close()

vertipper = []
wordlist_finish = {}


def wortwahl():
    rand_index = random.randint(0, len(wordbook_local))
    # print(rand_index)

    word = wordbook_local[rand_index]
    # print(word, len(word))

    vertipper.clear()

    return word


def table_vertipper(dict_vertipper):
    for i in table_pruef.get_children():
        table_pruef.delete(i)

    for item in dict_vertipper:
        print(item, dict_vertipper[item])
        table_pruef.insert('', 0, values=(item, dict_vertipper[item]))


def entry_mask(entry_bg_color):
    entry = tk.Entry(mainFrame, textvariable=eingabewort, width=20, background=entry_bg_color,
                     justify=CENTER, font=('Comic Sans MS', 16, 'bold'))
    entry.grid_forget()
    entry.grid(column=2, row=2, sticky='W, E')

    if len(eingabewort.get()) == 0:
        entry.focus()


def check(*args):
    for i in range(0, len(eingabewort.get())):
        if eingabewort.get()[i] == vorgabewort.get()[i]:
            pruefwert.set('richtig')
            entry_mask('green4')
        else:
            pruefwert.set('falsch')
            vertipper.append(1)
            eingabewort.set(eingabewort.get()[0:len(eingabewort.get())-1])
            entry_mask('red')

    if eingabewort.get() == vorgabewort.get():

        tippfehler = 0
        for item in vertipper:
            tippfehler += item
        # print(tippfehler)
        # print(vertipper)

        wordlist_finish.update({vorgabewort.get(): tippfehler})

        pruefwert.set('absolut richtig')

        eingabewort.set('')
        vorgabewort.set(wortwahl())
        print('\n')

        return table_vertipper(wordlist_finish)


mainWin = tk.Tk()
mainWin.title('Tipptrainer')

aufloesung_x = 800
aufloesung_y = 600

mainWin.geometry(f'{aufloesung_x}x{aufloesung_y}')
mainWin.columnconfigure(0, weight=1)
mainWin.rowconfigure(0, weight=1)

mainFrame = ttk.Frame(mainWin, borderwidth=1, relief='groove', padding=20)
mainFrame.grid(column=0, row=0, sticky='NSEW')

mainFrame.columnconfigure(1, weight=5)
mainFrame.columnconfigure(2, weight=5)
mainFrame.columnconfigure(3, weight=5)

mainFrame.rowconfigure(1, weight=5)
mainFrame.rowconfigure(2, weight=5)
mainFrame.rowconfigure(3, weight=5)
mainFrame.rowconfigure(4, weight=5)

eingabewort = StringVar()
vorgabewort = StringVar()
pruefwert = StringVar()

vorgabewort.set(wortwahl())

label_vorgabe = ttk.Label(mainFrame, textvariable=vorgabewort, width=20,
                          anchor='center', font=('Comic Sans MS', 16, 'bold'))
label_vorgabe.grid(column=2, row=1, sticky='W, E')

entry_mask('green4')

label_pruef = ttk.Label(mainFrame, textvariable=pruefwert, width=20)
label_pruef.grid(column=2, row=3, sticky='W, E')

style_pruef = ttk.Style()
style_pruef.configure("style_tabelle_pruef.Treeview.Heading", font=('Comic Sans MS', 10, 'bold'))

spalten_pruef = ('Wort', 'vertipper')

table_pruef = ttk.Treeview(mainFrame, columns=spalten_pruef, show='headings',
                           style='style_tabelle_pruef.Treeview')

table_pruef.grid(column=2, row=4, sticky='W, E')
table_pruef.heading(0, text='Wort', anchor=W)
table_pruef.column(0, anchor=W, width=380, stretch=NO)
table_pruef.heading(1, text='vertipper', anchor=W)
table_pruef.column(1, anchor=W, width=80, stretch=NO)

# padding
for child in mainFrame.winfo_children():
    child.grid_configure(padx=10, pady=10)

mainWin.bind('<Key>', check)
gc.collect()
mainWin.mainloop()
