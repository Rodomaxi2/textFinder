from tkinter import *
import tkinter.ttk as ttk
from main import searchLinks

link = 'https://docs.python.org/3.8/library/tkinter.html'

window = Tk()
window.title("Analizador de paginas")
window.geometry("400x400")

linkLabel = Label(window, text="Ingresa el link a evaluar:", font=10)
linkLabel.place(x=10, y=30)

textAreaLink = Entry(window, font=30, width=35)
textAreaLink.place(x=10, y=60)

buttonAnalizar = Button(window, text="Analizar", command=lambda: searchLinks(
    textAreaLink.get()))

buttonAnalizar.place(x=335, y=57)

tableDraw = ttk.Treeview(window, columns=3)
tableDraw.place(x=10, y=160)
tableDraw['columns'] = ('numero', 'categoria', 'consejo')
tableDraw.column("#0", width=0,  stretch=True)
tableDraw.column("numero", anchor=CENTER, width=40, stretch=True)
tableDraw.column("categoria", anchor=CENTER, width=100)
tableDraw.column("consejo", anchor=CENTER, width=240)

tableDraw.heading("#0", text="", anchor=CENTER)
tableDraw.heading("numero", text="Num", anchor=CENTER)
tableDraw.heading("categoria", text="Categoria", anchor=CENTER)
tableDraw.heading("consejo", text="Consejo", anchor=CENTER)

tableDraw.insert(parent='', index='end', iid=0, text='',
                 values=('0', 'Alta', ""))
tableDraw.insert(parent='', index='end', iid=1, text='',
                 values=('0', 'Media', ""))
tableDraw.insert(parent='', index='end', iid=2, text='',
                 values=('0', 'Baja', ""))


window.mainloop()
