import customtkinter as ctk
import os
import PyGrab
import PyGive

from tkinter import filedialog, messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

def browse_directory():
    folder = ctk.filedialog.askdirectory()
    if folder: #Opens the Folder Picker for Windows (Note: test out on Linux and Mac eventually)
    
        path_entry.delete(0, ctk.END)
        #Clear entry field
        path_entry.insert(0, folder)
        #Insert chosen directory

def encrypt_files(): #Does what it says...
    folder = path_entry.get()
    if not os.path.isdir(folder):
        messagebox.showerror("Woops!", f"'{folder}' is not a directory.")
    else:
        PyGrab.main(folder)

def decrypt_files(): #Runs my FUN key recovery software (literally just replaces only the else statement)
    folder = path_entry.get()
    if not os.path.isdir(folder):
        messagebox.showerror("Woops!", f"'{folder}' is not a directory.")
    else:
        PyGive.main(folder)

app = ctk.CTk()
app.title("NCrypt Software")
app.geometry("550x350") #Adjust the size of window (in px)

ctk.CTkLabel(app, text = "NCrypt Software", font = ("Arial", 16)).pack(pady = 10, padx= 10)

row = ctk.CTkFrame(app)
row.pack(pady = 10, padx = 10, fill = "x")

path_entry = ctk.CTkEntry(row, placeholder_text = "Desired directory to secure", width = 300)
path_entry.pack(side = "left", fill = "x", expand = True, padx = (10, 50), pady = 10)

ctk.CTkButton(row, text = "Browse for files", command = browse_directory).pack(side = "right", padx = (10, 10), pady = 10)
ctk.CTkButton(app, text = "Encrypt Selected File(s)", command = encrypt_files).pack(fill = "x", padx = 20)
ctk.CTkButton(app, text = "Decrypt Selected File(s)", command = decrypt_files).pack(fill = "x", padx = (20, 20),pady= 10)

log = ctk.CTkTextbox(app, width = 400, height = 100, corner_radius = 12)
log.pack(fill = "both", expand = True, padx = 20, pady = 20)

app.mainloop()