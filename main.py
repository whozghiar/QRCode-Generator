import tkinter as tk
import re

import pyqrcode
import png
from tkinter import filedialog
from tkinter import messagebox

def generate_qrcode(url,window):
    # Générer le QRCode
        print("Génération du QRCode...")
        print("URL : " + url)
        qrcode = pyqrcode.create(url)
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
        qrcode.png(save_path, scale=10)
        messagebox.showinfo("Succès", "QRCode généré avec succès")

        # Affiche le QRCode dans un messagebox pour l'utilisateur
        qrcode.show()

def check_url(url):
    # Vérifiez si l'URL correspond à l'expression régulière d'une URL internet
    url_regex = r'(https?://)?(www\.)?([a-zA-Z0-9]+)\.([a-zA-Z0-9]+)([a-zA-Z0-9\-\._\?\,\'/\\\+&%\$#\=~])'
    match = re.match(url_regex, url)
    return bool(match)

# Fonction qui active le bouton "Générer" si l'URL est valide par la fonction check_url, elle prend en paramètre un bouton
def activate_button(url_entry,button):
    if check_url(url_entry.get()):
        button.config(state="normal", bg = "green")
    else:
        button.config(state="disabled", bg="red")

def main():

    global window
    window = tk.Tk()
    window.geometry("600x400")
    window.title("QRCodeGenerator")
    window.iconbitmap("src/qrcode.ico")
    window.eval('tk::PlaceWindow . center')
    window.resizable(False, False)

    url_label = tk.Label(window, text="URL : ", font=("Arial", 8, "bold"))
    url_label.place(relx=0.2, rely=0.4, anchor="nw")

    url_entry = tk.Entry(window, width=50)
    url_entry.place(relx=0.3, rely=0.4, anchor="nw")

    #Le bouton n'est accessible que si l'utilisateur a entré une URL
    generate_button = tk.Button(window, text="Générer", command=lambda: generate_qrcode(url_entry.get(),window),fg="white",bg="red",state="disabled")
    generate_button.place(relx=0.3, rely=0.5, anchor="nw")

    url_entry.bind("<KeyRelease>", lambda event: activate_button(url_entry, generate_button))
    window.mainloop()
main()