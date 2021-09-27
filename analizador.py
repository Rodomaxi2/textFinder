from tkinter import *
from main import searchLinks

link = 'https://docs.python.org/3.8/library/tkinter.html'

window = Tk()
window.title("Analizador de paginas")
window.geometry("400x400")

Label(window, text="Ingresa el link a evaluar:")

display = Entry(window)
display.grid(row=1, columnspan=6, sticky=W+E)

Button(window, text="Analizar", command=lambda: searchLinks(
    link)).grid(row=1, column=9)

window.mainloop()
