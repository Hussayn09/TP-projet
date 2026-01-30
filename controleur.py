"""
Contrôleur pour l'application Carnet d'Adressess
Architecture MVC : Ce module représente la couche Contrôleur (Controller)
Responsabilité : Faire le lien entre la vue (interface) et le modèle (base de données)

Le contrôleur :
- Récupère les données de la vue (formulaire, sélection)
- Valide les données (email, champs obligatoires)
- Appelle le modèle pour effectuer les opérations
- Met à jour la vue avec les résultats
"""

import re
# ============================================================
# IMPORT DE LA CLASSE DU MODÈLE
# ============================================================
# On importe la CLASSE CarnetAdresses du module model1
# Contrairement à avant où on importait des fonctions, on importe maintenant la classe
# Cela permet d'utiliser directement les méthodes de la classe en POO
from model1 import CarnetAdresses


class Controller:
    """
    Contrôleur MVC pour gérer les interactions entre la vue et le modèle
    
    Cette classe :
    - Stocke une référence vers le modèle (instance de CarnetAdresses)
    - Stocke une référence vers la vue (interface Tkinter)
    - Contient les méthodes qui gèrent les actions de l'utilisateur
    - Valide les données avant de les envoyer au modèle
    """
    
    # ============================================================
    # MÉTHODE CONSTRUCTEUR : init
    # ============================================================
    def __init__(self, vue):
        """
        Constructeur du contrôleur
        
        Cette méthode est appelée automatiquement quand on crée une instance du contrôleur
        Exemple : controller = Controller(vue)
        
        Args:
            vue: Instance de la vue (classe View avec l'interface Tkinter)
                 Le contrôleur a besoin de la vue pour :
                 - Récupérer les données du formulaire
                 - Afficher les résultats dans le Treeview
                 - Afficher les messages d'erreur/succès
        
        Processus :
            1. Création d'une instance du modèle (CarnetAdresses)
            2. Stockage de la référence vers la vue
            3. Configuration de la vue pour qu'elle connaisse ce contrôleur
            4. Liaison des boutons de la vue aux méthodes du contrôleur
            5. Chargement et affichage de tous les contacts au démarrage
        """
        # Étape 1: Création d'une instance du modèle
        # CarnetAdresses() crée une nouvelle instance de la classe CarnetAdresses
        # Cette instance sera utilisée pour toutes les opérations de base de données
        # On la stocke dans self.modele pour pouvoir l'utiliser dans toutes les méthodes
        # 
        # Pourquoi créer l'instance ici ?
        # - Le contrôleur a besoin du modèle pour fonctionner
        # - On crée l'instance une seule fois au démarrage
        # - Toutes les méthodes du contrôleur utiliseront cette même instance
        self.modele = CarnetAdresses()
        
        # Étape 2: Stockage de la référence vers la vue
        # self.vue = vue permet au contrôleur d'accéder aux widgets et méthodes de la vue
        # Ces références sont essentielles pour la communication MVC :
        # - Contrôleur → Modèle : pour appeler les méthodes de base de données
        # - Contrôleur → Vue : pour mettre à jour l'interface utilisateur
        # 
        # La vue contient :
        # - Les champs du formulaire (Entry, Text)
        # - Le Treeview (liste des contacts)
        # - Les boutons d'action
        # - Les méthodes pour afficher les résultats
        self.vue = vue
        
        # Étape 3: Faire connaître le contrôleur à la vue
        # La vue a besoin du contrôleur pour certaines interactions
        # Par exemple, quand l'utilisateur double-clique sur un contact dans le Treeview,
        # la vue peut appeler directement une méthode du contrôleur
        # Cette méthode set_controller() doit exister dans la classe View
        # 
        # Pourquoi cette étape ?
        # - Permet à la vue de notifier le contrôleur d'événements (double-clic, sélection)
        # - Crée une communication bidirectionnelle : Vue ↔ Contrôleur
        self.vue.set_controller(self)
        
        # Étape 4: Liaison des boutons de la vue aux méthodes du contrôleur
        # Cette méthode va configurer chaque bouton pour qu'il appelle
        # la méthode correspondante du contrôleur quand il est cliqué
        # 
        # Exemple de configuration :
        # bouton_ajouter.config(command=self.ajouter_contact)
        # Quand l'utilisateur clique sur "Ajouter", ça appelle self.ajouter_contact()
        # 
        # Pourquoi cette étape ?
        # - Connecte l'interface utilisateur aux actions du contrôleur
        # - Chaque bouton déclenche une action spécifique
        self._lier_boutons()
        
        # Étape 5: Chargement et affichage de tous les contacts au démarrage
        # Au démarrage de l'application, on veut afficher tous les contacts existants
        # dans la base de données pour que l'utilisateur voie immédiatement son carnet
        # 
        # Cette méthode :
        # 1. Appelle le modèle pour récupérer tous les contacts
        # 2. Demande à la vue de les afficher dans le Treeview
        # 
        # Pourquoi cette étape ?
        # - L'utilisateur voit immédiatement son carnet d'adresses
        # - Pas besoin de cliquer sur "Afficher tous" au démarrage
        self.afficher_tous()
    
    # ============================================================
    # MÉTHODE PRIVÉE : _lier_boutons
    # ============================================================
    def _lier_boutons(self):
        """
        Lie tous les boutons de la vue aux méthodes correspondantes du contrôleur
        
        Cette méthode est privée (préfixe _) car elle n'est utilisée qu'en interne
        Elle configure chaque bouton pour qu'il appelle la bonne méthode quand il est cliqué
        
        Processus :
            Pour chaque bouton de la vue :
            1. Récupérer la référence du bouton depuis la vue
            2. Configurer le bouton pour qu'il appelle la méthode correspondante
            3. Exemple : bouton.config(command=self.methode)
        
        Boutons configurés :
            - bouton_ajouter → self.ajouter_contact
            - bouton_rechercher → self.rechercher_contact
            - bouton_modifier → self.modifier_contact
            - bouton_supprimer → self.supprimer_contact
            - bouton_afficher_tous → self.afficher_tous
            - bouton_quitter → self.quitter
        """
        # Configuration de chaque bouton
        # La vue doit avoir des attributs comme self.bouton_ajouter, self.bouton_rechercher, etc.
        # .config(command=...) configure l'action à exécuter quand le bouton est cliqué
        
        # Bouton "Ajouter" : appelle self.ajouter_contact() quand cliqué
        self.vue.btn_ajouter.config(command=self.ajouter_contact)
        
        # Bouton "Rechercher" : appelle self.rechercher_contact() quand cliqué
        self.vue.btn_rechercher.config(command=self.rechercher_contact)
        
        # Bouton "Modifier" : appelle self.modifier_contact() quand cliqué
        self.vue.btn_modifier.config(command=self.modifier_contact)
        
        # Bouton "Supprimer" : appelle self.supprimer_contact() quand cliqué
        self.vue.btn_supprimer.config(command=self.supprimer_contact)
        
        # Bouton "Afficher tous" : appelle self.afficher_tous() quand cliqué
        self.vue.btn_afficher_tous.config(command=self.afficher_tous)
        
        # Bouton "Quitter" : appelle self.quitter() quand cliqué
        self.vue.btn_quitter.config(command=self.quitter)
    
    def valider_email(self,email):
         # Si le champ email est vide, on considère que c'est valide
          # (car l'email n'est pas obligatoire)
        if email == "":
            return True

            
    # Expression régulière pour vérifier un email valide
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'


    # Vérifie si l'email correspond au modèle défini
        if re.match(pattern,email):

            return True

        else: 
            return False


    def ajouter_contact(self):

# 1️ Récupérer les données saisies dans le formulaire via la vue
        donnees = self.vue.get_inputs()
#nettoyer les données pour éviter les espaces parasites
        nom = donnees["nom"].strip()
        prenom = donnees["prenom"].strip()
        telephone = donnees["telephone"].strip()
        email = donnees["email"].strip()
        adresse = donnees["adresse"].strip()

 #  Vérifier les champs obligatoires
        if not nom or not prenom:
            self.vue.message_erreur("Erreur", "Le nom et le prénom sont obligatoires")
            return
 # Vérifier la validité de l'email
        if not self.valider_email(email):
            self.vue.message_erreur("Erreur", "L'email n'est pas valide")
            return

#   Appeler le modèle pour ajouter le contact dans la base
        self.modele.ajouter_contact(nom, prenom, telephone, email, adresse)

 #  Message de confirmation
        self.vue.message_info("Succès", "Contact ajouté avec succès")

#  Nettoyer le formulaire
        self.vue.vider_champs()

#  Rafraîchir la liste des contacts
        self.afficher_tous()

        
    def rechercher_contact(self):
#  Récupérer les données saisies dans le formulaire
        donnees = self.vue.get_inputs()
#  Nettoyer les données pour éviter les espaces parasites
        valeur = (donnees["nom"].strip() or donnees["telephone"].strip() or donnees["email"].strip())
#  Vérifier si le critère de recherche est present
        if not valeur:
            self.vue.message_erreur("Erreur", "Le critère de recherche est obligatoire")
            return
#  Appeler le modèle pour effectuer la recherche

        resultats = self.modele.rechercher_contact(valeur)
#  Vérifier s'il y a des résultats
        if not resultats:
            self.vue.message_erreur("Erreur", "Aucun contact trouvé")
            return
#  Afficher les résultats dans le Treeview
        self.vue.afficher_liste(resultats)
        
    
    def charger_contact_selection(self):
#  Récupérer l'ID du contact sélectionné dans le Treeview
        contact_id = self.vue.get_selection()
#  Vérifier qu'un contact est bien sélectionné
        if not contact_id :
            self.vue.message_erreur("Erreur", "Aucun contact sélectionné")

            return
#  Récupérer le contact complet depuis le modèle        
        contact = self.modele.obtenir_contact_par_id(contact_id)
#  Remplir le formulaire avec les données du contact

        self.vue.set_inputs(contact)


    def modifier_contact(self):
#  Récupérer l'ID du contact sélectionné
        contact_id = self.vue.get_selection()
# Vérifier qu'un contact est bien sélectionné
        if not contact_id :
            self.vue.message_erreur("Erreur", "Aucun contact sélectionné")
            return


#  Récupérer les données saisies dans le formulaire
        donnees = self.vue.get_inputs()

 #nettoyage des donnees 
        nom = donnees["nom"].strip() 
        prenom = donnees["prenom"].strip()
        telephone = donnees["telephone"].strip()
        email = donnees["email"].strip()
        adresse = donnees["adresse"].strip()
#  Vérifier les champs obligatoires
        if not nom or not prenom:
            self.vue.message_erreur("Erreur","Nom et prénom sont obligatoir" )
            return
#  Vérifier la validité de l'email
        if not self.valider_email(email):
            self.vue.message_erreur("Erreur", "Email invalide")
            return

#  Appeler le modèle pour modifier le contact
        self.modele.modifier_contact(contact_id, nom, prenom, telephone, email, adresse)
#  Message de confirmation
        self.vue.message_info("Succès", "Contact modifié avec succès")

#  Nettoyage du formulaire
        self.vue.vider_champs()

#  Rafraîchir la liste des contacts
        self.afficher_tous()

    def supprimer_contact(self):
 # Récupérer l'ID du contact sélectionné
        contact_id = self.vue.get_selection()

#  Vérifier qu'un contact est bien sélectionné
        if not contact_id :
             self.vue.message_erreur("Erreur", "Sélectionnez un contact à supprimer")
             return  
#  Récupérer les informations du contact (pour confirmation)
        contact = self.modele.obtenir_contact_par_id(contact_id)  
#  Demander confirmation à l'utilisateur
        confirmation = self.vue.message_confirmation(
        "Confirmation",
        f"Voulez-vous vraiment supprimer ce contact ?\n\n"
        f"Nom : {contact[1]}\n"
        f"Prénom : {contact[2]}"
    )

# Si l'utilisateur annule, on arrête
        if not confirmation :
          return
#  Appeler le modèle pour supprimer le contact
        self.modele.supprimer_contact(contact_id)
#  Message de confirmation
        self.vue.message_info("Succès", "Contact supprimé avec succès")

        #  Nettoyage du formulaire
        self.vue.vider_champs()

        #  Rafraîchir la liste des contacts
        self.afficher_tous()



    def afficher_tous(self):
        #  Récupérer tous les contacts depuis le modèle
        contacts = self.modele.afficher_tous()

        #  Afficher la liste complète dans le Treeview via la vue
        self.vue.afficher_liste(contacts)

    def quitter(self):
        """Quitte l'application"""
        self.vue.root.quit()