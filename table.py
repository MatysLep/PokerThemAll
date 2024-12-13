from treys import Card, Deck
from joueur import Joueur


class Table:
    """
    Représente la table de jeu de poker Poker Them All.

    Attributs :
        cartes_communautaires (list) : Liste des cartes visibles sur la table.
        pot (int) : Montant total des jetons misés dans le pot.
        joueurs (list) : Liste des joueurs participant à la partie.
        paquet (Deck) : Instance de la classe Deck de la bibliothèque Treys, représentant le paquet de cartes.

    Méthodes :
        distribuer_cartes():
            Distribue deux cartes aléatoires à chaque joueur encore en jeu.
        
        nouveau_paquet():
            Réinitialise le paquet, les cartes communautaires et le pot pour une nouvelle manche.

        ajouter_joueur(joueur):
            Ajoute un joueur à la table si l'objet est une instance valide de la classe Joueur.
        
        phase_flop():
            Tire trois cartes du paquet et les ajoute aux cartes communautaires.

        phase_turn():
            Tire une carte du paquet et l'ajoute aux cartes communautaires (phase turn).

        phase_river():
            Tire une carte du paquet et l'ajoute aux cartes communautaires (phase river).

        afficher_pot():
            Affiche le montant total du pot.
    """

    def __init__(self):
        self.cartes_communautaires = []
        self.pot = 0
        self.joueurs = []
        self.paquet = Deck()

    def distribuer_cartes(self):
        """
        Distribue deux cartes aléatoires à chaque joueur encore en jeu.
        """
        for joueur in self.joueurs:
            joueur.cartes_en_main = [self.paquet.draw(1)[0], self.paquet.draw(1)[0]]

    def nouveau_paquet(self):
        """
        Réinitialise le paquet, les cartes communautaires et le pot pour une nouvelle manche.
        """
        self.paquet = Deck()
        self.cartes_communautaires = []
        self.pot = 0

    def ajouter_joueur(self, joueur):
        """
        Ajoute un joueur à la table.

        Paramètres :
            joueur (Joueur) : Instance de la classe Joueur à ajouter.

        Exceptions :
            TypeError : Si l'objet ajouté n'est pas une instance de la classe Joueur.
        """
        if isinstance(joueur, Joueur):
            self.joueurs.append(joueur)
        else:
            raise TypeError("L'objet ajouté doit être une instance de Joueur.")

    def phase_flop(self):
        """
        Tire trois cartes du paquet et les ajoute aux cartes communautaires.
        """
        self.cartes_communautaires.extend(self.paquet.draw(3))

    def phase_turn(self):
        """
        Tire une carte du paquet et l'ajoute aux cartes communautaires (phase turn).
        """
        self.cartes_communautaires.append(self.paquet.draw(1)[0])

    def phase_river(self):
        """
        Tire une carte du paquet et l'ajoute aux cartes communautaires (phase river).
        """
        self.cartes_communautaires.append(self.paquet.draw(1)[0])

    def afficher_pot(self):
        """
        Affiche le montant total du pot.
        """
        print(f"Le pot est de {self.pot} €\n")
