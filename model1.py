"""
Module Model - Gestion de la base de données des contacts
Architecture MVC : Ce module représente la couche Modèle (Model)
Responsabilité : Gérer toutes les opérations de base de données SQLite

Programmation Orientée Objet (POO) :
- Encapsulation : Les données et méthodes sont regroupées dans une classe
- Réutilisabilité : Une instance peut être créée et réutilisée
- Maintenabilité : Code organisé et structuré
"""

import sqlite3
import os


class CarnetAdresses:
    """
    Classe principale pour gérer le carnet d'adresses dans une base de données SQLite
    
    Cette classe encapsule toutes les opérations CRUD (Create, Read, Update, Delete)
    sur la table contacts de la base de données.
    
    Attributs de classe :
        DB_PATH (str) : Chemin vers le fichier de base de données SQLite
        C'est un attribut de classe (partagé par toutes les instances)
        car toutes les instances utilisent la même base de données
    
    Méthodes principales :
        - initialiser_base() : Crée la table si elle n'existe pas
        - ajouter_contact() : Insère un nouveau contact
        - rechercher_contact() : Recherche des contacts par critère
        - modifier_contact() : Met à jour un contact existant
        - supprimer_contact() : Supprime un contact
        - afficher_tous() : Récupère tous les contacts
        - obtenir_contact_par_id() : Récupère un contact par son ID
    """
    
    # ============================================================
    # ATTRIBUT DE CLASSE : Chemin de la base de données
    # ============================================================
    # Cette variable est définie au niveau de la classe (pas de self)
    # Toutes les instances de CarnetAdresses partagent cette même valeur
    # Avantage : Si on change le chemin, toutes les instances utilisent le nouveau chemin
    # Syntaxe : DB_PATH est accessible via CarnetAdresses.DB_PATH ou self.DB_PATH
    DB_PATH = "carnet_adresses.db"
    
    # ============================================================
    # MÉTHODE CONSTRUCTEUR : init
    # ============================================================
    def init(self, db_path=None):
        """
        Constructeur de la classe CarnetAdresses
        
        Cette méthode est appelée automatiquement quand on crée une nouvelle instance
        Exemple : carnet = CarnetAdresses()
        
        Args:
            db_path (str, optional): Chemin personnalisé vers la base de données
                                   Si None, utilise DB_PATH par défaut
        
        Processus :
            1. Si un chemin personnalisé est fourni, on l'utilise
            2. Sinon, on utilise le chemin par défaut de la classe
            3. On initialise automatiquement la base de données
        
        Pourquoi cette méthode ?
        - Permet de personnaliser le chemin de la base de données si nécessaire
        - Assure que la base est toujours initialisée à la création de l'instance
        - Point d'entrée pour toute configuration future
        """
        # Étape 1: Vérification si un chemin personnalisé est fourni
        # Si db_path n'est pas None et n'est pas vide, on l'utilise
        # Cela permet de créer des instances avec des bases de données différentes
        # Exemple : carnet_test = CarnetAdresses("test.db")
        if db_path:
            # Si un chemin personnalisé est fourni, on met à jour l'attribut de classe
            # self.DB_PATH crée un attribut d'instance qui masque l'attribut de classe
            # pour cette instance spécifique
            self.DB_PATH = db_path
        else:
            # Si aucun chemin n'est fourni, on utilise l'attribut de classe par défaut
            # CarnetAdresses.DB_PATH fait référence à l'attribut de classe
            self.DB_PATH = CarnetAdresses.DB_PATH
        
        # Étape 2: Initialisation automatique de la base de données
        # Dès qu'une instance est créée, on s'assure que la table existe
        # Cela évite d'avoir à appeler initialiser_base() manuellement
        # C'est une bonne pratique : l'objet est prêtà l'emploi dès sa création
        self.initialiser_base()
    
    # ============================================================
    # MÉTHODE : initialiser_base
    # ============================================================
    def initialiser_base(self):
        """
        Initialise la base de données et crée la table contacts si elle n'existe pas
        
        Cette méthode est appelée :
        - Automatiquement dans init lors de la création de l'instance
        - Manuellement si besoin de réinitialiser la structure
        
        Processus détaillé :
        1. Connexion à la base de données SQLite
        2. Création d'un curseur pour exécuter des commandes SQL
        3. Exécution de CREATE TABLE IF NOT EXISTS
        4. Validation des changements (commit)
        5. Fermeture de la connexion
        
        Structure de la table contacts :
        - id : Identifiant unique auto-incrémenté (clé primaire)
        - nom : Nom du contact (obligatoire, NOT NULL)
        - prenom : Prénom du contact (obligatoire, NOT NULL)
        - telephone : Numéro de téléphone (optionnel)
        - email : Adresse email (optionnel)
        - adresse : Adresse postale (optionnel)
        
        Raises:
            sqlite3.Error: En cas d'erreur de connexion ou d'exécution SQL
        """
        # Étape 1: Connexion à la base de données SQLite
        # sqlite3.connect() crée une connexion à la base de données
        # Si le fichier n'existe pas, SQLite le crée automatiquement
        # self.DB_PATH fait référence au chemin de la base (attribut d'instance ou de classe)
        # La connexion est stockée dans la variable locale conn
        conn = sqlite3.connect(self.DB_PATH)
        
        # Étape 2: Création d'un curseur
        # Un curseur est un objet qui permet d'exécuter des commandes SQL
        # C'est comme un "pointeur" qui parcourt les résultats des requêtes
        # Toutes les opérations SQL (SELECT, INSERT, UPDATE, DELETE) passent par le curseur
        cursor = conn.cursor()
        
        # Étape 3: Exécution de la commande CREATE TABLE
        # CREATE TABLE IF NOT EXISTS : Crée la table seulement si elle n'existe pas déjà
        # C'est une sécurité : si la table existe déjà, rien ne se passe (pas d'erreur)
        # 
        # Structure de la table :
        # - id INTEGER PRIMARY KEY AUTOINCREMENT :
        #   * INTEGER : Type entier
        #   * PRIMARY KEY : Clé primaire (identifiant unique)
        #   * AUTOINCREMENT : Auto-incrémentation automatique (1, 2, 3, ...)
        #
        # - nom TEXT NOT NULL :
        #   * TEXT : Type texte (chaîne de caractères)
        #   * NOT NULL : Champ obligatoire (ne peut pas être vide)
        #
        # - prenom TEXT NOT NULL : Même principe que nom
        #
        # - telephone TEXT : Champ optionnel (peut être NULL)
        # - email TEXT : Champ optionnel
        # - adresse TEXT : Champ optionnel
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                telephone TEXT,
                email TEXT,
                adresse TEXT
            )
        """)
        
        # Étape 4: Validation des changements (commit)
        # En SQLite, les modifications ne sont pas automatiquement sauvegardées
        # conn.commit() valide et sauvegarde définitivement les changements
        # Sans commit(), les changements seraient perdus à la fermeture de la connexion
        # C'est une transaction : soit tout est sauvegardé, soit rien
        conn.commit()
        
        # Étape 5: Fermeture de la connexion
        # Il est important de fermer la connexion pour libérer les ressources
        # SQLite peut avoir des problèmes si trop de connexions sont ouvertes simultanément
        # La fermeture libère aussi les verrous sur le fichier de base de données
        conn.close()
    
    # ============================================================
    # MÉTHODE : ajouter_contact
    # ============================================================
    def ajouter_contact(self, nom, prenom, telephone=None, email=None, adresse=None):
        """
        Ajoute un nouveau contact dans la base de données
        
        Cette méthode implémente l'opération CREATE du CRUD
        Elle insère une nouvelle ligne dans la table contacts
        
        Args:
            nom (str): Nom du contact (obligatoire)
            prenom (str): Prénom du contact (obligatoire)
            telephone (str, optional): Numéro de téléphone
            email (str, optional): Adresse email
            adresse (str, optional): Adresse postale
        
        Returns:
            int: L'identifiant unique du contact ajouté (généré automatiquement)
                 Cet ID est utile pour référencer le contact plus tard
        
        Raises:
            ValueError: Si nom ou prenom est vide/None
            sqlite3.Error: En cas d'erreur de base de données
        
        Processus :
            1. Validation des champs obligatoires
            2. Initialisation de la base (s'assurer que la table existe)
            3. Connexion à la base de données
            4. Nettoyage des données (suppression des espaces)
            5. Insertion dans la table
            6. Récupération de l'ID généré
            7. Validation et fermeture
        """
        # Étape 1: Validation du champ nom (obligatoire)
        # not nom vérifie si nom est None, False, ou une chaîne vide ""
        # not nom.strip() vérifie si nom ne contient que des espaces "   "
        # Si l'une de ces conditions est vraie, on lève une exception ValueError
        # C'est une validation métier : on refuse les données invalides avant d'aller en base
        if not nom or not nom.strip():
            # raise ValueError() interrompt l'exécution et retourne une erreur
            # Le contrôleur pourra capturer cette exception et afficher un message à l'utilisateur
            raise ValueError("Le nom est obligatoire")
        
        # Étape 2: Validation du champ prenom (obligatoire)
        # Même logique que pour nom
        if not prenom or not prenom.strip():
            raise ValueError("Le prénom est obligatoire")
        
        # Étape 3: Initialisation de la base de données
        # On s'assure que la table existe avant d'insérer des données
        # C'est une sécurité : même si init a déjà fait ça, on peut appeler
        # ajouter_contact() directement sans passer par init
        self.initialiser_base()
        
        # Étape 4: Connexion à la base de données
        # On ouvre une nouvelle connexion pour cette opération
        # Chaque opération ouvre/ferme sa propre connexion (pattern simple)
        conn = sqlite3.connect(self.DB_PATH)
        
        # Étape 5: Création du curseur
        cursor = conn.cursor()
        
        # Étape 6: Nettoyage des données (sanitization)
        # .strip() supprime les espaces en début et fin de chaîne
        # Exemple : "  Jean  " devient "Jean"
        # Pourquoi ? Les espaces parasites peuvent causer des problèmes d'affichage
        # et de recherche
        nom = nom.strip()
        prenom = prenom.strip()
        
        # Pour les champs optionnels, on vérifie s'ils existent avant de les nettoyer
        # telephone.strip() if telephone else None signifie :
        # - Si telephone existe et n'est pas None : on le nettoie avec strip()
        # - Sinon : on met None (valeur par défaut pour les champs optionnels)
        telephone = telephone.strip() if telephone else None
        email = email.strip() if email else None
        adresse = adresse.strip() if adresse else None
        
        # Étape 7: Construction de la requête SQL INSERT
        # INSERT INTO contacts : Insère une nouvelle ligne dans la table contacts
        # (nom, prenom, telephone, email, adresse) : Liste des colonnes à remplir
        # VALUES (?, ?, ?, ?, ?) : Les valeurs à insérer
        # Les ? sont des placeholders (paramètres) qui seront remplacés par les vraies valeurs
        # Pourquoi utiliser ? au lieu de concaténerles valeurs ?
        # → Protection contre les injections SQL (sécurité)
        # → Gestion automatique des caractères spéciaux (guillemets, etc.)
        requete = """
            INSERT INTO contacts (nom, prenom, telephone, email, adresse) 
            VALUES (?, ?, ?, ?, ?)
        """
        
        # Étape 8: Exécution de la requête avec les paramètres
        # cursor.execute() exécute la requête SQL
        # Le deuxième argument est un tuple contenant les valeurs à substituer aux ?
        # L'ordre des valeurs doit correspondre à l'ordre des ? dans la requête
        # (nom, prenom, telephone, email, adresse) correspond aux 5 ? de la requête
        cursor.execute(requete, (nom, prenom, telephone, email, adresse))
        
        # Étape 9: Récupération de l'ID généré automatiquement
        # cursor.lastrowid contient l'ID de la dernière ligne insérée
        # C'est l'ID auto-incrémenté généré par SQLite (1, 2, 3, ...)
        # Cet ID est utile pour référencer le contact plus tard (modification, suppression)
        contact_id = cursor.lastrowid
        
        # Étape 10: Validation des changements
        # Sans commit(), l'insertion ne serait pas sauvegardée
        conn.commit()
        
        # Étape 11: Fermeture de la connexion
        conn.close()
        
        # Étape 12: Retour de l'ID du contact créé
        # Le contrôleur peut utiliser cet ID pour afficher un message de confirmation
        return contact_id
    
    # ============================================================
    # MÉTHODE : rechercher_contact
    # ============================================================
    def rechercher_contact(self, critere):
        """
        Recherche des contacts dans la base de données selon un critère
        
        Cette méthode implémente l'opération READ (recherche) du CRUD
        Elle recherche dans les champs nom, telephone et email
        
        Args:
            critere (str): Critère de recherche (nom, téléphone ou email partiel)
        
        Returns:
            list: Liste de tuples contenant les contacts trouvés
                 Format : [(id, nom, prenom, telephone, email, adresse), ...]
                 Liste vide [] si aucun contact ne correspond
        
        Raises:
            ValueError: Si le critère de recherche est vide
            sqlite3.Error: En cas d'erreur de base de données
        
        Processus :
            1. Validation du critère de recherche
            2. Initialisation de la base
            3. Connexion à la base
            4. Construction du pattern de recherche (LIKE avec %)
            5. Exécution de la requête SELECT avec OR
            6. Récupération des résultats
            7. Retour de la liste
        """
        # Étape 1: Validation du critère de recherche
        # On refuse une recherche vide ou ne contenant que des espaces
        if not critere or not critere.strip():
            raise ValueError("Le critère de recherche est obligatoire")
        
        # Étape 2: Initialisation de la base
        self.initialiser_base()
        
        # Étape 3: Connexion à la base de données
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()
        
        # Étape 4: Nettoyage du critère de recherche
        critere = critere.strip()
        
        # Étape 5: Construction du pattern de recherche
        # Le pattern utilise le caractère % qui signifie "n'importe quelle séquence"
        # Exemple : critere = "Jean" → pattern = "%Jean%"
        # Cela permet de trouver "Jean", "Jean-Pierre", "Dupont Jean", etc.
        # C'est une recherche partielle (contient le critère)
        pattern = f"%{critere}%"
        
        # Étape 6: Construction de la requête SQL SELECT
        # SELECT id, nom, prenom, telephone, email, adresse :
        #   Récupère ces colonnes pour chaque contact trouvé
        #
        # FROM contacts : Table à interroger
        #
        # WHERE : Condition de filtrage
        #   LOWER(nom) LIKE LOWER(?) : Recherche dans le nom (insensible à la casse)
        #   OR LOWER(telephone) LIKE LOWER(?) : OU dans le téléphone
        #   OR LOWER(email) LIKE LOWER(?) : OU dans l'email
        #   Le OR permet de trouver le critère dans n'importe lequel de ces champs
        #
        # LOWER() : Convertit en minuscules pour une recherche insensible à la casse
        #   "JEAN" et "jean" donneront les mêmes résultats
        #
        # LIKE : Opérateur de correspondance partielle (utilise % comme wildcard)
        #
        # ORDER BY nom, prenom : Trie les résultats par nom puis prénom (ordre alphabétique)
        requete = """
            SELECT id, nom, prenom, telephone, email, adresse 
            FROM contacts
            WHERE LOWER(nom) LIKE LOWER(?) 
                 OR LOWER(telephone) LIKE LOWER(?)
                 OR LOWER(email) LIKE LOWER(?)
            ORDER BY nom, prenom
        """
        
        # Étape 7: Exécution de la requête
        # On passe le même pattern trois fois car il y a trois ? dans la requête
        # (pattern, pattern, pattern) correspond aux trois conditions OR
        cursor.execute(requete, (pattern, pattern, pattern))
        
        # Étape 8: Récupération de tous les résultats
        # fetchall() retourne une liste de tuples
        # Chaque tuple représente un contact : (id, nom, prenom, telephone, email, adresse)
        # Si aucun résultat : retourne une liste vide []
        resultats = cursor.fetchall()
        
        # Étape 9: Fermeture de la connexion
        conn.close()
        
        # Étape 10: Retour des résultats
        # La vue pourra utiliser cette liste pour afficher les contacts dans le Treeview
        return resultats
    
    # ============================================================
    # MÉTHODE : modifier_contact
    # ============================================================
    def modifier_contact(self, contact_id, nom, prenom, telephone=None, email=None, adresse=None):
        """
        Modifie un contact existant dans la base de données
        
        Cette méthode implémente l'opération UPDATE du CRUD
        Elle met à jour les informations d'un contact identifié par son ID
        
        Args:
            contact_id (int): Identifiant unique du contact à modifier (obligatoire)
            nom (str): Nouveau nom du contact (obligatoire)
            prenom (str): Nouveau prénom du contact (obligatoire)
            telephone (str, optional): Nouveau numéro de téléphone
            email (str, optional): Nouvelle adresse email
            adresse (str, optional): Nouvelle adresse postale
        
        Returns:
            bool: True si le contact a été modifié, False si l'ID n'existe pas
                 Permet au contrôleur de savoir si l'opération a réussi
        
        Raises:
            ValueError: Si contact_id est invalide ou si nom/prenom sont vides
            sqlite3.Error: En cas d'erreur de base de données
        
        Processus :
            1. Validation de l'ID du contact
            2. Validation des champs obligatoires
            3. Initialisation de la base
            4. Connexion à la base
            5. Nettoyage des données
            6. Exécution de UPDATE
            7. Vérification du nombre de lignes modifiées
            8. Validation et fermeture
        """
        # Étape 1: Validation de l'ID du contact
        # On vérifie que contact_id existe, n'est pas None, et est supérieur à 0
        # Un ID invalide ne peut pas correspondre à un contact existant
        if not contact_id or contact_id <= 0:
            raise ValueError("L'identifiant du contact est invalide")
        
        # Étape 2: Validation des champs obligatoires (nom et prénom)
        # Même logique que dans ajouter_contact()
        if not nom or not nom.strip():
            raise ValueError("Le nom est obligatoire")
        if not prenom or not prenom.strip():
            raise ValueError("Le prénom est obligatoire")
        
        # Étape 3: Initialisation de la base
        self.initialiser_base()
        
        # Étape 4: Connexion à la base de données
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()
        
        # Étape 5: Nettoyage des données
        # Même processus que dans ajouter_contact()
        nom = nom.strip()
        prenom = prenom.strip()
        telephone = telephone.strip() if telephone else None
        email = email.strip() if email else None
        adresse = adresse.strip() if adresse else None
        
        # Étape 6: Construction de la requête SQL UPDATE
        # UPDATE contacts : Met à jour la table contacts
        # SET nom = ?, prenom = ?, ... : Définit les nouvelles valeurs pour chaque colonne
        # WHERE id = ? : Condition pour identifier le contact à modifier
        #   Seul le contact avec cet ID sera modifié
        requete = """
            UPDATE contacts
            SET nom = ?, prenom = ?, telephone = ?, email = ?, adresse = ?
            WHERE id = ?
        """
        
        # Étape 7: Exécution de la requête UPDATE
        # On passe les nouvelles valeurs dans l'ordre : nom, prenom, telephone, email, adresse
        # Puis l'ID en dernier pour la clause WHERE
        # L'ordre doit correspondre à l'ordre des ? dans la requête
        cursor.execute(requete, (nom, prenom, telephone, email, adresse, contact_id))
        
        # Étape 8: Vérification du nombre de lignes modifiées
        # cursor.rowcount contient le nombre de lignes affectées par la dernière requête
        # Si rowcount > 0 : le contact a été trouvé et modifié
        # Si rowcount == 0 : aucun contact avec cet ID n'existe (rien n'a été modifié)
        lignes_modifiees = cursor.rowcount
        
        # Étape 9: Validation des changements
        conn.commit()
        
        # Étape 10: Fermeture de la connexion
        conn.close()
        
        # Étape 11: Retour du résultat
        # lignes_modifiees > 0 retourne True si au moins une ligne a été modifiée
        # Sinon retourne False (le contact n'existe pas)
        # Le contrôleur peut utiliser ce booléen pour afficher un message approprié
        return lignes_modifiees > 0
    
    # ============================================================
    # MÉTHODE : supprimer_contact
    # ============================================================
    def supprimer_contact(self, contact_id):
        """
        Supprime un contact de la base de données
        
        Cette méthode implémente l'opération DELETE du CRUD
        Elle supprime définitivement un contact identifié par son ID
        
        Args:
            contact_id (int): Identifiant unique du contact à supprimer (obligatoire)
        
        Returns:
            bool: True si le contact a été supprimé, False si l'ID n'existe pas
                 Permet au contrôleur de savoir si l'opération a réussi
        
        Raises:
            ValueError: Si contact_id est invalide
            sqlite3.Error: En cas d'erreur de base de données
        
        Processus :
            1. Validation de l'ID du contact
            2. Initialisation de la base
            3. Connexion à la base
            4. Exécution de DELETE
            5. Vérification du nombre de lignes supprimées
            6. Validation et fermeture
        
        Attention : Cette opération est irréversible !
        """
        # Étape 1: Validation de l'ID du contact
        # Même logique que dans modifier_contact()
        if not contact_id or contact_id <= 0:
            raise ValueError("L'identifiant du contact est invalide")
        
        # Étape 2: Initialisation de la base
        self.initialiser_base()
        
        # Étape 3: Connexion à la base de données
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()
        
        # Étape 4: Construction de la requête SQL DELETE
        # DELETE FROM contacts : Supprime des lignes de la table contacts
        # WHERE id = ? : Condition pour identifier le contact à supprimer
        #   Seul le contact avec cet ID sera supprimé
        #   Sans WHERE, TOUS les contacts seraient supprimés (danger !)
        requete = """
            DELETE FROM contacts WHERE id = ?"""
        
        # Étape 5: Exécution de la requête DELETE
        # On passe contact_id dans un tuple (contact_id,)
        # La virgule est OBLIGATOIRE pour créer un tuple avec un seul élément
        # Sans la virgule : (contact_id) serait interprété comme juste une valeur
        cursor.execute(requete, (contact_id,))
        
        # Étape 6: Vérification du nombre de lignes supprimées
        # cursor.rowcount contient le nombre de lignes supprimées
        # Si rowcount > 0 : le contact a été trouvé et supprimé
        # Si rowcount == 0 : aucun contact avec cet ID n'existe (rien n'a été supprimé)
        lignes_supprimees = cursor.rowcount
        
        # Étape 7: Validation des changements
        # Important : Sans commit(), la suppression ne serait pas effective
        conn.commit()
        
        # Étape 8: Fermeture de la connexion
        conn.close()
        
        # Étape 9: Retour du résultat
        # lignes_supprimees > 0 retourne True si au moins une ligne a été supprimée
        # Sinon retourne False (le contact n'existe pas)
        return lignes_supprimees > 0
    
    # ============================================================
    # MÉTHODE : afficher_tous
    # ============================================================
    def afficher_tous(self):
        """
        Récupère tous les contacts de la base de données trié alphabetiquement
        
        
        
        Returns:
            list: Liste de tuples contenant tous les contacts
                 Format : [(id, nom, prenom, telephone, email, adresse), ...]
                 Liste vide [] si aucun contact n'existe
        
        Raises:
            sqlite3.Error: En cas d'erreur de base de données
        
        Processus :
            1. Initialisation de la base
            2. Connexion à la base
            3. Exécution de SELECT sans condition WHERE
            4. Récupération de tous les résultats
            5. Retour de la liste
        
        Utilisation :
            - Au démarrage de l'application pour afficher le carnet complet
            - Après une opération pour rafraîchir l'affichage
        """
        # Étape 1: Initialisation de la base
        self.initialiser_base()
        
        # Étape 2: Connexion à la base de données
        conn = sqlite3.connect(self.DB_PATH)
        cursor = conn.cursor()
        
        # Étape 3: Construction de la requête SQL SELECT
        # SELECT id, nom, prenom, telephone, email, adresse :
        #   Récupère toutes ces colonnes pour chaque contact
        #
        # FROM contacts : Table à interroger
        #
        # Pas de WHERE : Pas de condition, donc tous les contacts sont récupérés
        #
        # ORDER BY nom, prenom : Trie les résultats par nom puis prénom
        #   Ordre alphabétique croissant (A à Z)
        #   Permet un affichage organisé et lisible
        requete = """
            SELECT id, nom, prenom, telephone, email, adresse
            FROM contacts
            ORDER BY nom, prenom
        """
        
        # Étape 4: Exécution de la requête
        # Pas de paramètres car il n'y a pas de ? dans la requête
        cursor.execute(requete)
        
        # Étape 5: Récupération de tous les résultats
        # fetchall() retourne une liste de tuples
        # Chaque tuple représente un contact : (id, nom, prenom, telephone, email, adresse)
        # Si aucun contact : retourne une liste vide []
        resultats = cursor.fetchall()
        
        # Étape 6: Fermeture de la connexion
        conn.close()
        
        # Étape 7: Retour de tous les contacts
        # La vue pourra utiliser cette liste pour remplir le Treeview
        return resultats
    
    # ============================================================
    # MÉTHODE : obtenir_contact_par_id
    # ============================================================
    def obtenir_contact_par_id(self, contact_id):
        """
        Récupère un contact spécifique de la base de données par son identifiant unique
        
        Cette méthode est utiliséepour :
        - Charger les informations d'un contact dans le formulaire pour modification
        - Vérifier l'existence d'un contact avant suppression
        - Afficher les détails d'un contact sélectionné
        
        Args:
            contact_id (int): L'identifiant unique du contact à récupérer (obligatoire)
        
        Returns:
            tuple or None: Tuple contenant les informations du contact trouvé
                          Format : (id, nom, prenom, telephone, email, adresse)
                          Retourne None si le contact n'existe pas
        
        Raises:
            ValueError: Si contact_id est invalide
            sqlite3.Error: En cas d'erreur de base de données
        
        Processus :
            1. Validation de l'ID
            2. Initialisation de la base
            3. Connexion à la base
            4. Exécution de SELECT avec WHERE id = ?
            5. Récupération d'un seul résultat (fetchone)
            6. Retour du contact ou None
        """
        # Étape 1: Vérification que l'ID est valide
        # On vérifie que contact_id existe, est positif et supérieur à 0
        # Un ID invalide ne peut pas correspondre à un contact existant
        if not contact_id or contact_id <= 0:
            raise ValueError("L'identifiant du contact est invalide")
        
        # Étape 2: Initialisation de la base de données
        # On s'assure que la table existe avant de faire une requête
        self.initialiser_base()
        
        # Étape 3: Connexion à la base de données SQLite
        conn = sqlite3.connect(self.DB_PATH)
        
        # Étape 4: Création d'un curseur pour exécuter les requêtes SQL
        cursor = conn.cursor()
        
        # Étape 5: Construction de la requête SQL SELECT
        # SELECT id, nom, prenom, telephone, email, adresse :
        #   Récupère toutes ces colonnes pour le contact trouvé
        #
        # FROM contacts : Table à interroger
        #
        # WHERE id = ? : Condition pour identifier le contact spécifique par son ID unique
        #   Seul le contact avec cet ID sera récupéré
        #
        # Le ? est un placeholder qui sera remplacé par contact_id
        # Utiliser ? au lieu de concaténer évite les injections SQL (sécurité)
        requete = """
            SELECT id, nom, prenom, telephone, email, adresse
            FROM contacts
            WHERE id = ?
        """
        
        # Étape 6: Exécution de la requête SELECT avec l'ID comme paramètre
        # On passe contact_id dans un tuple (contact_id,)
        # La virgule après contact_id est OBLIGATOIRE pour créer un tuple avec un seul élément
        # Sans la virgule : (contact_id) serait interprété comme juste une valeur, pas un tuple
        # Python exige un tuple pour les paramètres SQL, même s'il n'y a qu'un seul paramètre
        cursor.execute(requete, (contact_id,))
        
        # Étape 7: Récupération du résultat de la requête
        # fetchone() retourne un seul résultat (le premier trouvé) sous forme de tuple
        # Contrairement à fetchall() qui retourne une liste de tuples
        # Si aucun résultat n'est trouvé, fetchone() retourne None
        # Format du tuple : (id, nom, prenom, telephone, email, adresse)
        contact = cursor.fetchone()
        
        # Étape 8: Fermeture de la connexion à la base de données
        # Important pour libérer les ressources
        conn.close()
        
        # Étape 9: Retour du contact trouvé (ou None si non trouvé)
        # Si contact existe : retourne le tuple (id, nom, prenom, telephone, email, adresse)
        # Si contact est None : retourne None (le contact n'existe pas)
        # Le contrôleur peut vérifier si contact est None pour afficher un message d'erreur
        return contact