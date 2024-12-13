from treys import Card


class Joueur:
    """
    Représente un joueur de poker.

    Attributs :
        nom (str) : Le nom du joueur.
        cartes_en_main (list) : Les cartes actuellement en possession du joueur.
        jetons (int) : Le nombre de jetons que possède le joueur.
        en_jeu (bool) : Indique si le joueur est encore actif dans la manche.

    Méthodes :
        __repr__():
            Retourne une représentation lisible de l'objet Joueur.

        miser(montant):
            Réduit les jetons du joueur du montant misé et retourne ce montant.
            Lève une exception si le montant est invalide ou dépasse les jetons disponibles.

        se_coucher():
            Met le joueur hors jeu pour la manche en cours.

        hors_jeu():
            Vérifie si le joueur n'a plus de jetons.
    """

    def __init__(self, nom, jetons):
        """
        Initialise un joueur avec un nom, un nombre de jetons, et un état actif.

        Paramètres :
            nom (str) : Le nom du joueur.
            jetons (int) : Le nombre initial de jetons du joueur.
        """
        self.nom = nom
        self.cartes_en_main = []
        self.jetons = jetons
        self.en_jeu = True

    def __repr__(self):
        """
        Retourne une représentation lisible de l'objet Joueur.

        Retours :
            str : Une chaîne de caractères décrivant le joueur.
        """
        cartes_joueur = " ".join([Card.int_to_pretty_str(carte) for carte in self.cartes_en_main])
        return f"{self.nom} ({self.jetons} Jetons), Cartes : {cartes_joueur}"

    def miser(self, montant):
        """
        Réduit les jetons du joueur du montant spécifié.

        Paramètres :
            montant (int) : Le montant à miser.

        Retours :
            int : Le montant misé.

        Exceptions :
            ValueError : Si le montant est invalide ou dépasse les jetons disponibles.
        """
        if self.jetons >= montant > 0:
            self.jetons -= montant
            return montant
        else:
            raise ValueError("Montant invalide pour les jetons disponibles.")

    def se_coucher(self):
        """
        Met le joueur hors jeu pour la manche en cours.
        """
        print(f"{self.nom} s'est couché.")
        self.en_jeu = False

    def hors_jeu(self):
        """
        Vérifie si le joueur n'a plus de jetons.

        Retours :
            bool : True si le joueur n'a plus de jetons, False sinon.
        """
        return self.jetons == 0
