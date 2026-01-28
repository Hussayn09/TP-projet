import tkinter as tk
from tkinter import ttk, messagebox


class ContactView:
    def __init__(self, root):  
        self.root = root
        self.root.title("Carnet d'Adresses")
        self.root.geometry("900x600")

        # ============================================
        # Titre principal
        # ============================================
        titre_frame = tk.Frame(self.root, bg="#2563eb", height=80)
        titre_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        titre_frame.pack_propagate(False)
          
        titre_label = tk.Label(
            titre_frame,
            text="Carnet d'adresses",
            font=("Arial", 24, "bold"),
            bg="#2563eb",
            fg="white"
        )
        titre_label.pack(pady=20)

        # ================= FRAME FORMULAIRE =================
        frame_form = tk.LabelFrame(root, text="Informations du contact", padx=10, pady=10)
        frame_form.pack(fill="x", padx=10, pady=5)

        # Nom
        tk.Label(frame_form, text="Nom *").grid(row=0, column=0, sticky="w")
        self.entry_nom = tk.Entry(frame_form)
        self.entry_nom.grid(row=0, column=1, padx=5, pady=2)

        # Prénom
        tk.Label(frame_form, text="Prénom *").grid(row=0, column=2, sticky="w")
        self.entry_prenom = tk.Entry(frame_form)
        self.entry_prenom.grid(row=0, column=3, padx=5, pady=2)

        # Téléphone
        tk.Label(frame_form, text="Téléphone").grid(row=1, column=0, sticky="w")
        self.entry_telephone = tk.Entry(frame_form)
        self.entry_telephone.grid(row=1, column=1, padx=5, pady=2)

        # Email
        tk.Label(frame_form, text="Email").grid(row=1, column=2, sticky="w")
        self.entry_email = tk.Entry(frame_form)
        self.entry_email.grid(row=1, column=3, padx=5, pady=2)

        # Label erreur email
        self.label_email_error = tk.Label(
            frame_form,
            text="",
            fg="red",
            font=("Arial", 8)
        )
        self.label_email_error.grid(row=1, column=4, sticky="w", padx=2)

        # Validation temps réel
        self.entry_email.bind("<KeyRelease>", self._valider_email_temps_reel)

        # Adresse
        tk.Label(frame_form, text="Adresse").grid(row=2, column=0, sticky="nw")
        self.text_adresse = tk.Text(frame_form, height=1, width=40)
        self.text_adresse.grid(row=2, column=1, columnspan=3, padx=5, pady=2)

        # ================= FRAME BOUTONS =================
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(fill="x", pady=5)

        self.btn_ajouter = tk.Button(
            frame_buttons,
            text="Ajouter",
            bg="#3b82f6",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            cursor="hand2"
        )
        self.btn_rechercher = tk.Button(
            frame_buttons,
            text="Rechercher",
            bg="#10b981",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            cursor="hand2"
        )
        self.btn_modifier = tk.Button(
            frame_buttons,
            text="Modifier",
            bg="#f59e0b",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            cursor="hand2"
        )
        self.btn_supprimer = tk.Button(
            frame_buttons,
            text="Supprimer",
            bg="#ef4444",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            cursor="hand2"
        )
        self.btn_afficher_tous = tk.Button(
            frame_buttons,
            text="Afficher tous",
            bg="#6366f1",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            cursor="hand2"
        )
        self.btn_quitter = tk.Button(
            frame_buttons,
            text="Quitter",
            bg="#64748b",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            cursor="hand2"
        )

        self.btn_ajouter.pack(side="left", padx=5)
        self.btn_rechercher.pack(side="left", padx=5)
        self.btn_modifier.pack(side="left", padx=5)
        self.btn_supprimer.pack(side="left", padx=5)
        self.btn_afficher_tous.pack(side="left", padx=5)
        self.btn_quitter.pack(side="right", padx=5)

        # ================= FRAME TABLE =================
        frame_table = tk.Frame(root)
        frame_table.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("id", "nom", "prenom", "telephone", "email", "adresse")

        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())

        self.tree.column("id", width=0, stretch=False)
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind(
            '<Double-1>',
            lambda e: self.controller.charger_contact_selection()
            if hasattr(self, 'controller') else None
        )

    # ================= VALIDATION EMAIL =================
    def _valider_email_temps_reel(self, event):
        email = self.entry_email.get().strip()

        if not email:
            self.label_email_error.config(text="", fg="red")
            self.entry_email.config(bg="white")
            return

        if "@" not in email:
            self.label_email_error.config(text="⚠️ @ manquant")
            self.entry_email.config(bg="#ffe6e6")
            return

        partie_locale, reste = email.split("@", 1)
        if not partie_locale:
            self.label_email_error.config(text="⚠️ Partie avant @ vide")
            self.entry_email.config(bg="#ffe6e6")
            return

        if "." not in reste:
            self.label_email_error.config(text="⚠️ Extension manquante")
            self.entry_email.config(bg="#ffe6e6")
            return

        if len(reste.split('.')[-1]) < 2:
            self.label_email_error.config(text="⚠️ Extension trop courte")
            self.entry_email.config(bg="#ffe6e6")
            return
        caracteres_interdits = [' ', ',', ';', ':', '!', '?']
        for char in caracteres_interdits:
            if char in email:
                self.label_email_error.config(
                    text=f"⚠️ Caractère '{char}' non autorisé"
                )
                self.entry_email.config(bg="#ffe6e6")
                return
# ✅ Email valide (au niveau syntaxique)
        self.label_email_error.config(text="✓ Format valide", fg="green")
        self.entry_email.config(bg="#e6ffe6")  # Fond vert clair
    # ================= MÉTHODES =================
    def get_inputs(self):
        return {
            "nom": self.entry_nom.get(),
            "prenom": self.entry_prenom.get(),
            "telephone": self.entry_telephone.get(),
            "email": self.entry_email.get(),
            "adresse": self.text_adresse.get("1.0", "end").strip()
        }

    def set_inputs(self, contact):
        self.vider_champs()
        self.entry_nom.insert(0, contact[1])
        self.entry_prenom.insert(0, contact[2])
        self.entry_telephone.insert(0, contact[3] or "")
        self.entry_email.insert(0, contact[4] or "")
        self.text_adresse.insert("1.0", contact[5] or "")

    def vider_champs(self):
        self.entry_nom.delete(0, "end")
        self.entry_prenom.delete(0, "end")
        self.entry_telephone.delete(0, "end")
        self.entry_email.delete(0, "end")
        self.text_adresse.delete("1.0", "end")

    def afficher_liste(self, liste_contacts):
        self.tree.delete(*self.tree.get_children())
        for contact in liste_contacts:
            self.tree.insert("", "end", values=contact)

    def get_selection(self):
        selected = self.tree.focus()
        if not selected:
            return None
        return self.tree.item(selected)["values"][0]

    def set_controller(self, controller):
        self.controller = controller

    def message_info(self, titre, message):
        messagebox.showinfo(titre, message)

    def message_erreur(self, titre, message):
        messagebox.showerror(titre, message)

    def message_confirmation(self, titre, message):
        return messagebox.askyesno(titre, message)