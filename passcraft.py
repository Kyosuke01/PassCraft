import random
import string
import tkinter as tk
from tkinter import ttk, messagebox
import requests  # Pour vérifier la version en ligne
import webbrowser  # Pour ouvrir le lien de mise à jour
import os

# Version actuelle de l'application
CURRENT_VERSION = "1.1.1"

# Fonction pour vérifier les mises à jour
def check_for_updates():
    try:
        version_url = "https://raw.githubusercontent.com/Kyosuke01/PassCraft/main/version.txt"
        response = requests.get(version_url)
        latest_version = response.text.strip()

        if latest_version != CURRENT_VERSION:
            if messagebox.askyesno("⬆️ PassCraft - Mise à jour disponible", f"Une nouvelle version de PassCraft est disponible.\nVersion : {latest_version}\nVoulez-vous la télécharger ?"):
                webbrowser.open("https://github.com/Kyosuke01/PassCraft/releases/latest")
    except requests.RequestException as e:
        messagebox.showerror("Erreur", f"Problème de connexion pour vérifier les mises à jour : {e}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible de vérifier les mises à jour : {e}")

# Fonction pour centrer la fenêtre sur l'écran
def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# Fonction pour générer un mot de passe
def generate_password():
    try:
        len_mdp = int(entry_len_mdp.get())
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer une longueur valide.")
        return

    if len_mdp <= 0:
        messagebox.showerror("Erreur", "La longueur doit être supérieure à zéro.")
        return

    use_lowercase = var_lowercase.get()
    use_uppercase = var_uppercase.get()
    use_numbers = var_numbers.get()
    use_special = var_special.get()

    if not (use_lowercase or use_uppercase or use_numbers or use_special):
        messagebox.showerror("Erreur", "Sélectionnez au moins un type de caractère.")
        return

    # Création des pools de caractères par catégorie
    char_pools = {
        "lowercase": string.ascii_lowercase if use_lowercase else "",
        "uppercase": string.ascii_uppercase if use_uppercase else "",
        "numbers": string.digits if use_numbers else "",
        "special": string.punctuation if use_special else "",
    }

    # Sélection d'au moins un caractère de chaque type demandé
    selected_chars = [
        random.choice(pool) for pool in char_pools.values() if pool
    ]

    # Remplir le reste des caractères
    remaining_length = len_mdp - len(selected_chars)
    all_chars = "".join(char_pools.values())
    if remaining_length > 0:
        selected_chars.extend(random.choices(all_chars, k=remaining_length))

    # Mélanger pour éviter que les caractères soient dans un ordre prévisible
    random.shuffle(selected_chars)

    # Conversion de la liste en chaîne
    password = "".join(selected_chars)

    # Affichage du mot de passe
    create_password_row(password)

# Fonction pour créer une ligne avec un mot de passe et des boutons "Copier" et "Supprimer"
def create_password_row(password):
    frame = tk.Frame(frame_passwords, bg="white", pady=5)
    frame.pack(fill="x", padx=5, pady=2)

    text = tk.Entry(frame, width=30, font=("Arial", 10), highlightthickness=0)
    text.insert(0, password)
    text.config(state="readonly")
    text.pack(side="left", padx=5)

    tk.Button(frame, text="Copier", command=lambda: copy_to_clipboard(password), bg="#81c9fa", fg="black", relief="flat", font=("Arial", 10)).pack(side="left", padx=5)
    tk.Button(frame, text="Supprimer", command=lambda: delete_password(frame), bg="#ff5252", fg="black", relief="flat", font=("Arial", 10)).pack(side="left", padx=5)

    # Mise à jour de la zone de défilement
    canvas_passwords.update_idletasks()
    canvas_passwords.configure(scrollregion=canvas_passwords.bbox("all"))
    update_scrollbar_visibility()

    # Défiler automatiquement vers le bas
    canvas_passwords.yview_moveto(1.0)

# Variable globale pour stocker l'identifiant de l'événement `after`
message_timer_id = None

def show_message(text):
    global message_timer_id

    # Annuler le délai précédent s'il existe
    if message_timer_id is not None:
        root.after_cancel(message_timer_id)

    # Mettre à jour le texte du message
    message_label.config(text=text)

    # Programmer un nouveau délai
    message_timer_id = root.after(3000, lambda: message_label.config(text=""))

# Fonction pour copier un mot de passe dans le presse-papier
def copy_to_clipboard(password):
    root.clipboard_clear()
    root.clipboard_append(password)
    show_message("Mot de passe copié dans le presse-papier.")

# Fonction pour copier tous les mots de passe en une seule fois
def copy_all_passwords():
    passwords = [widget.winfo_children()[0].get() for widget in frame_passwords.winfo_children()]
    all_passwords = "\n".join(passwords)
    root.clipboard_clear()
    root.clipboard_append(all_passwords)
    show_message("Tous les mots de passe ont été copiés dans le presse-papier.")

# Fonction pour supprimer un mot de passe
def delete_password(frame):
    frame.destroy()
    canvas_passwords.update_idletasks()
    canvas_passwords.configure(scrollregion=canvas_passwords.bbox("all"))
    update_scrollbar_visibility()

# Fonction pour supprimer tous les mots de passe générés
def delete_all_passwords():
    for widget in frame_passwords.winfo_children():
        widget.destroy()
    canvas_passwords.update_idletasks()
    canvas_passwords.configure(scrollregion=canvas_passwords.bbox("all"))
    update_scrollbar_visibility()

# Fonction pour faire défiler avec la molette de la souris
def on_mouse_wheel(event):
    if frame_passwords.winfo_height() > canvas_passwords.winfo_height():
        canvas_passwords.yview_scroll(-1 if event.delta > 0 else 1, "units")

# Fonction pour mettre à jour la visibilité de la barre de défilement
def update_scrollbar_visibility():
    if frame_passwords.winfo_height() > canvas_passwords.winfo_height():
        scrollbar_passwords.pack(side="right", fill="y")
    else:
        scrollbar_passwords.pack_forget()

# Création de la fenêtre principale
root = tk.Tk()
root.title("PassCraft")
root.geometry("800x300")
root.resizable(False, False)
root.config(bg="white")

try:
    root.iconbitmap(os.path.join(os.path.dirname(__file__), "cadenas.ico"))
except Exception as e:
    print(f"Erreur d'icône : {e}")  # Permet d'ignorer l'erreur si l'icône n'est pas trouvée

# Vérification des mises à jour au lancement
check_for_updates()

# Widgets pour les paramètres de génération
frame_controls = tk.Frame(root, pady=10, bg="white")
frame_controls.pack(side="left", padx=10, anchor="n")

tk.Label(frame_controls, text="Longueur du mot de passe :", bg="white", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5)
entry_len_mdp = tk.Entry(frame_controls, font=("Arial", 10), bg="lightgrey", fg="black", bd=0, relief="flat", insertbackground="black")
entry_len_mdp.insert(0, "20")
entry_len_mdp.grid(row=0, column=1, padx=10, pady=5)

# Checkbuttons pour les critères de génération de mot de passe
var_lowercase, var_uppercase, var_numbers, var_special = tk.BooleanVar(value=True), tk.BooleanVar(value=True), tk.BooleanVar(value=True), tk.BooleanVar(value=True)
for i, (text, var) in enumerate([("Lettres minuscules", var_lowercase), ("Lettres majuscules", var_uppercase), ("Nombres", var_numbers), ("Caractères spéciaux", var_special)]):
    tk.Checkbutton(frame_controls, text=text, variable=var, bg="white", fg="black", selectcolor="white", font=("Arial", 10)).grid(row=i+1, column=0, columnspan=2)

# Boutons d'action
tk.Button(frame_controls, text="Générer", command=generate_password, bg="#5ccb5f", fg="black", relief="flat", font=("Arial", 10)).grid(row=5, column=0, columnspan=2, pady=10)
tk.Button(frame_controls, text="Copier tous les mots de passe", command=copy_all_passwords, bg="#81c9fa", fg="black", relief="flat", font=("Arial", 10)).grid(row=6, column=0, columnspan=2, pady=5)
tk.Button(frame_controls, text="Supprimer tous les mots de passe", command=delete_all_passwords, bg="#ff5252", fg="black", relief="flat", font=("Arial", 10)).grid(row=7, column=0, columnspan=2, pady=5)

# Label pour afficher les messages
message_label = tk.Label(root, text="", bg="white", font=("Arial", 10), fg="#009929")
message_label.pack(side="bottom", pady=5)

# Zone de défilement pour afficher les mots de passe
frame_scroll = tk.Frame(root)
frame_scroll.pack(side="right", fill="both", expand=True)

canvas_passwords = tk.Canvas(frame_scroll, bg="white")
scrollbar_passwords = ttk.Scrollbar(frame_scroll, orient="vertical", command=canvas_passwords.yview)
frame_passwords = tk.Frame(canvas_passwords, bg="white")

canvas_passwords.create_window((0, 0), window=frame_passwords, anchor="nw")
canvas_passwords.configure(yscrollcommand=scrollbar_passwords.set)

canvas_passwords.pack(side="left", fill="both", expand=True)
scrollbar_passwords.pack(side="right", fill="y")

update_scrollbar_visibility()

# Lier la molette de la souris pour le défilement
canvas_passwords.bind_all("<MouseWheel>", on_mouse_wheel)

# Centrer la fenêtre
center_window(root)

# Un petit délai avant de forcer le focus
root.after(100, root.focus_force)  # 100 ms de délai

# Boucle principale
root.mainloop()
