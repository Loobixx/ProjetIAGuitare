from fpdf import FPDF
from CreationDuTableau import *
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pygame

# Initialisation de pygame
pygame.mixer.init()

# Création de la fenêtre principale
root = tk.Tk()
root.title("Sélecteur de fichier audio")
root.geometry("400x250")
root.configure(bg="#e0dfd5")  # Couleur de fond en accord avec le logo

fichier_selectionne = ""
text_affichage = tk.StringVar()
text_affichage.set("")

label_message = tk.Label(root, textvariable=text_affichage, font=("Arial", 10), bg="#e0dfd5")
label_message.pack(pady=5)

def choisir_fichier():
    global fichier_selectionne
    fichier_selectionne = filedialog.askopenfilename(filetypes=[("Fichiers audio", "*.mp3;*.wav")])
    if fichier_selectionne:
        label_fichier.config(text=f"Fichier sélectionné : {fichier_selectionne}", bg="#e0dfd5")
        text_affichage.set("Fichier chargé")
        pygame.mixer.music.load(fichier_selectionne)

def valider_action():
    if fichier_selectionne:
        text_affichage.set("Chargement en cours...")
        label_message.config(fg="orange")
        label_message.update_idletasks()
        class TablaturePDF(FPDF):
            def header(self):
                if self.page_no() == 1:
                    self.set_font('Arial', 'B', 12)
                    self.cell(0, 10, 'Titre de la musique', 0, 1, 'C')

            def footer(self):
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

            def ajouter_pages(self):
                self.add_page()
                y = 40 - 2
                for i in range(6):
                    for j in range(6):
                        self.line(10, y + j * 5, 200, y + j * 5)
                    y += 40

            def main(self):
                self.ajouter_pages()
                self.set_font('Arial', 'I', 12)
                x = 11
                y = 29
                for i in range(len(tab)):
                    for j in range(len(tab[i])):
                        self.text(x, y + (5 * (tab[i][j][1] + 1)), str(tab[i][j][0]))
                    x += 8
                    if x > 199:
                        y += 40
                        x = 11
                    if y > 250:
                        self.ajouter_pages()
                        y = 29
                        x = 11

        pdf = TablaturePDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        # Charger l'audio

        audio_path = (fichier_selectionne)

        tab = creationTab(audio_path)

        pdf.main()

        # Sauvegarder le PDF
        pdf.output("Tablature/tablature.pdf")
        print("PDF Crée")
        text_affichage.set("PDF créé avec succès")
        label_message.config(fg="green")

def jouer_audio():
    if fichier_selectionne:
        pygame.mixer.music.play()
        text_affichage.set("Lecture en cours...")

def pause_audio():
    pygame.mixer.music.pause()
    text_affichage.set("Lecture en pause")

def reprendre_audio():
    pygame.mixer.music.unpause()
    text_affichage.set("Lecture reprise")


# Bouton pour choisir un fichier
btn_choisir = tk.Button(root, text="Choisir un fichier audio", command=choisir_fichier, bg="#e0dfd5")
btn_choisir.pack(pady=5)

# Label pour afficher le fichier sélectionné
label_fichier = tk.Label(root, text="Aucun fichier sélectionné", wraplength=300, bg="#e0dfd5")
label_fichier.pack()

# Bouton de validation
btn_valider = tk.Button(root, text="Valider", command=valider_action, bg="#e0dfd5")
btn_valider.pack(pady=5)

# Cadre pour les boutons de lecture
frame_controls = tk.Frame(root, bg="#e0dfd5")
frame_controls.pack(pady=5)

btn_jouer = tk.Button(frame_controls, text="▶ Jouer", command=jouer_audio, bg="#e0dfd5")
btn_jouer.pack(side=tk.LEFT, padx=5)

btn_pause = tk.Button(frame_controls, text="⏸ Pause", command=pause_audio, bg="#e0dfd5")
btn_pause.pack(side=tk.LEFT, padx=5)

btn_reprendre = tk.Button(frame_controls, text="⏯ Reprendre", command=reprendre_audio, bg="#e0dfd5")
btn_reprendre.pack(side=tk.LEFT, padx=5)

# Lancement de l'application
root.mainloop()