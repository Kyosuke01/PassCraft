import random
import string
import tkinter as tk
from tkinter import ttk, messagebox
import requests  # Pour vérifier la version en ligne
import webbrowser  # Pour ouvrir le lien de mise à jour

# Version actuelle de l'application
CURRENT_VERSION = "1.0.0"

# Fonction pour vérifier les mises à jour
def check_for_updates():
    try:
        # URL du fichier de version sur GitHub (modifie avec ton URL réelle)
        version_url = "https://raw.githubusercontent.com/Kyosuke01/PassCraft/main/version.txt"
        response = requests.get(version_url)
        latest_version = response.text.strip()

        if latest_version != CURRENT_VERSION:
            if messagebox.askyesno("Mise à jour disponible", f"Une nouvelle version ({latest_version}) est disponible. Voulez-vous la télécharger ?"):
                # Lien de téléchargement direct
                webbrowser.open("https://github.com/Kyosuke01/PassCraft/releases/latest")
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

    # Création de la liste des caractères à utiliser
    char_pool = ""
    if use_lowercase:
        char_pool += string.ascii_lowercase
    if use_uppercase:
        char_pool += string.ascii_uppercase
    if use_numbers:
        char_pool += string.digits
    if use_special:
        char_pool += string.punctuation

    # Génération du mot de passe
    password = ''.join(random.choice(char_pool) for _ in range(len_mdp))

    # Affichage du mot de passe
    create_password_row(password)

# Fonction pour créer une ligne avec un mot de passe et un bouton "Copier" et "Supprimer"
def create_password_row(password):
    frame = tk.Frame(frame_passwords, bg="#f0f0f0", pady=5)
    frame.pack(fill="x", padx=5, pady=2)

    text = tk.Text(frame, height=1, width=30, wrap="none", bg="lightgray", font=("Arial", 10), highlightthickness=0)
    text.insert("1.0", password)
    text.config(state="disabled")
    text.pack(side="left", padx=5)

    btn_copy = tk.Button(frame, text="Copier", command=lambda: copy_to_clipboard(password), bg="#4CAF50", fg="white", relief="flat", font=("Arial", 10))
    btn_copy.pack(side="left", padx=5)

    btn_delete = tk.Button(frame, text="Supprimer", command=lambda: delete_password(frame), bg="#f44336", fg="white", relief="flat", font=("Arial", 10))
    btn_delete.pack(side="left", padx=5)

    # Mise à jour de la zone de défilement
    canvas_passwords.update_idletasks()
    canvas_passwords.configure(scrollregion=canvas_passwords.bbox("all"))

# Fonction pour copier un mot de passe dans le presse-papier
def copy_to_clipboard(password):
    root.clipboard_clear()
    root.clipboard_append(password)
    root.update()
    messagebox.showinfo("Copié", "Mot de passe copié dans le presse-papier.")

# Fonction pour copier tous les mots de passe en une seule fois
def copy_all_passwords():
    passwords = []
    for widget in frame_passwords.winfo_children():
        text_widget = widget.winfo_children()[0]
        passwords.append(text_widget.get("1.0", "end-1c"))
    all_passwords = "\n".join(passwords)
    root.clipboard_clear()
    root.clipboard_append(all_passwords)
    root.update()
    messagebox.showinfo("Copié", "Tous les mots de passe ont été copiés dans le presse-papier.")

# Fonction pour supprimer un mot de passe
def delete_password(frame):
    frame.destroy()
    canvas_passwords.update_idletasks()
    canvas_passwords.configure(scrollregion=canvas_passwords.bbox("all"))

# Fonction pour supprimer tous les mots de passe générés
def delete_all_passwords():
    for widget in frame_passwords.winfo_children():
        widget.destroy()
    canvas_passwords.update_idletasks()
    canvas_passwords.configure(scrollregion=canvas_passwords.bbox("all"))

# Fonction pour faire défiler avec la molette de la souris
def on_mouse_wheel(event):
    visible_height = canvas_passwords.winfo_height()
    total_height = frame_passwords.winfo_height()

    if total_height > visible_height:
        if event.delta > 0:
            canvas_passwords.yview_scroll(-1, "units")
        elif event.delta < 0:
            canvas_passwords.yview_scroll(1, "units")

# Création de la fenêtre principale
root = tk.Tk()
root.title("PassCraft")
root.geometry("800x300")
root.resizable(False, False)
root.config(bg="#e0f7fa")

# Vérification des mises à jour au lancement
check_for_updates()

# Widgets pour les paramètres de génération
frame_controls = tk.Frame(root, pady=10, bg="#b2ebf2")
frame_controls.pack(side="left", padx=10, anchor="n")

tk.Label(frame_controls, text="Longueur du mot de passe :", bg="#b2ebf2", font=("Arial", 10)).grid(row=0, column=0, padx=10, pady=5)
entry_len_mdp = tk.Entry(frame_controls, font=("Arial", 10))
entry_len_mdp.insert(0, "20")
entry_len_mdp.grid(row=0, column=1, padx=10, pady=5)

var_lowercase = tk.BooleanVar(value=True)
tk.Checkbutton(frame_controls, text="Lettres minuscules", variable=var_lowercase, bg="#b2ebf2", font=("Arial", 10)).grid(row=1, column=0, columnspan=2)

var_uppercase = tk.BooleanVar(value=True)
tk.Checkbutton(frame_controls, text="Lettres majuscules", variable=var_uppercase, bg="#b2ebf2", font=("Arial", 10)).grid(row=2, column=0, columnspan=2)

var_numbers = tk.BooleanVar(value=True)
tk.Checkbutton(frame_controls, text="Nombres", variable=var_numbers, bg="#b2ebf2", font=("Arial", 10)).grid(row=3, column=0, columnspan=2)

var_special = tk.BooleanVar(value=True)
tk.Checkbutton(frame_controls, text="Caractères spéciaux", variable=var_special, bg="#b2ebf2", font=("Arial", 10)).grid(row=4, column=0, columnspan=2)

tk.Button(frame_controls, text="Générer", command=generate_password, bg="#4CAF50", fg="white", relief="flat", font=("Arial", 10)).grid(row=5, column=0, columnspan=2, pady=10)
tk.Button(frame_controls, text="Copier tous les mots de passe", command=copy_all_passwords, bg="#2196F3", fg="white", relief="flat", font=("Arial", 10)).grid(row=6, column=0, columnspan=2, pady=5)
tk.Button(frame_controls, text="Supprimer tous les mots de passe", command=delete_all_passwords, bg="#f44336", fg="white", relief="flat", font=("Arial", 10)).grid(row=7, column=0, columnspan=2, pady=5)

# Zone de défilement pour afficher les mots de passe
frame_scroll = tk.Frame(root)
frame_scroll.pack(side="right", fill="both", expand=True)

canvas_passwords = tk.Canvas(frame_scroll, bg="#ffffff")
scrollbar_passwords = ttk.Scrollbar(frame_scroll, orient="vertical", command=canvas_passwords.yview)
frame_passwords = tk.Frame(canvas_passwords, bg="#ffffff")

frame_passwords.bind(
    "<Configure>",
    lambda e: canvas_passwords.configure(scrollregion=canvas_passwords.bbox("all"))
)

canvas_passwords.create_window((0, 0), window=frame_passwords, anchor="nw")
canvas_passwords.configure(yscrollcommand=scrollbar_passwords.set)

canvas_passwords.pack(side="left", fill="both", expand=True)
scrollbar_passwords.pack(side="right", fill="y")

# Lier la molette de la souris pour le défilement
canvas_passwords.bind_all("<MouseWheel>", on_mouse_wheel)

# Centrer la fenêtre sur l'écran
center_window(root)

# Boucle principale de l'interface graphique
root.mainloop()
