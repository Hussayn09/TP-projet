"""
Point d'entrée de l'application Carnet d'Adresses
Architecture MVC

Rôle de main.py :
- Créer la fenêtre principale Tkinter
- Initialiser la vue
- Initialiser le contrôleur
- Lancer la boucle principale de l'application
"""


# IMPORTS


import tkinter as tk

# Import de la vue
from view import ContactView

# Import du contrôleur
from controleur import Controller



# FONCTION PRINCIPALE


def main():
    """
    Fonction principale de l'application
    
    Cette fonction :
    1. Crée la fenêtre principale Tkinter
    2. Crée la vue (interface graphique)
    3. Crée le contrôleur (liaison vue ↔ modèle)
    4. Lance la boucle principale Tkinter
    """

    # 1️⃣ Création de la fenêtre principale
    root = tk.Tk()

    # 2️⃣ Création de la vue
    # On passe la fenêtre root à la vue
    vue = ContactView(root)

    # 3️⃣ Création du contrôleur
    # On passe la vue au contrôleur
    # Le contrôleur crée lui-même le modèle
    controller = Controller(vue)

    # 4️⃣ Lancement de la boucle principale Tkinter
    root.mainloop()



# POINT D'ENTRÉE DU PROGRAMME


if __name__ == "__main__":
    main()