from table import Table
from joueur import Joueur
from treys import Card, Evaluator
from utils import clear_terminal
import time


class Jeu:
    """
    Représente le jeu de poker Texas Hold'em.

    Attributs :
        table (Table) : Instance de la classe Table représentant l'état de la table.
        joueurs (list) : Liste des joueurs participant à la partie.
        tour (int) : Numéro du tour actuel.
        result (list) : Résultat du dernier tour joué, contenant le gagnant, le type de main, et le pot.

    Méthodes :
        initialiser_joueurs():
            Initialise les joueurs en demandant leur nombre et leurs noms.

        distribuer_cartes():
            Mélange le paquet de cartes et distribue deux cartes à chaque joueur.

        afficher_joueurs():
            Affiche les informations de chaque joueur à la table.

        effectuer_phase(phase):
            Réalise une phase spécifique (flop, turn, river) et affiche les cartes communautaires.

        recuperer_mise_max(tab):
            Retourne la mise maximale dans une liste de mises.

        tour_de_mise():
            Gère un tour de mise, permettant aux joueurs de miser, suivre ou se coucher.

        jouer_partie():
            Lance une partie complète jusqu'à ce qu'il ne reste qu'un seul joueur avec des jetons.

        get_gagnant():
            Retourne le joueur gagnant de la partie.

        jouer():
            Gère un tour de jeu, y compris la distribution des cartes et les phases (flop, turn, river).

        nb_joueur_avec_jetons():
            Retourne le nombre de joueurs avec des jetons.

        joueur_en_jeu(i):
            Retourne le nombre de joueurs présents encore dans la manche.

        get_result():
            Évalue les mains des joueurs et détermine le gagnant du tour.

        restart_game():
            Réinitialise l'état des joueurs pour une nouvelle manche.
    """

    def __init__(self):
        self.table = Table()
        self.joueurs = self.table.joueurs
        self.tour = 0
        self.result = []

    def initialiser_joueurs(self):
        """
        Initialise les joueurs en demandant leur nombre et leurs noms.
        """
        while True:
            try:
                nombre_joueurs = int(input("Entrez le nombre de joueurs : "))
                if nombre_joueurs < 2:
                    print("Il faut au moins 2 joueurs pour jouer.")
                    continue
                break
            except ValueError:
                print("Veuillez entrer un nombre valide.")

        for i in range(nombre_joueurs):
            nom = input(f"Entrez le nom du joueur {i + 1} : ")
            self.table.ajouter_joueur(Joueur(nom, 100))

    def distribuer_cartes(self):
        """
        Mélange le paquet de cartes et distribue deux cartes à chaque joueur.
        """
        self.table.paquet.shuffle()
        self.table.distribuer_cartes()

    def afficher_joueurs(self):
        """
        Affiche les informations de chaque joueur à la table.
        """
        for joueur in self.table.joueurs:
            print("* ", joueur)
        print()

    def effectuer_phase(self, phase):
        """
        Réalise une phase spécifique (flop, turn, river) et affiche les cartes communautaires.
        """
        if phase == "flop":
            self.table.phase_flop()
        elif phase == "turn":
            self.table.phase_turn()
        elif phase == "river":
            self.table.phase_river()

        print(f"Cartes après la phase \"{phase}\" :",
              " ".join([Card.int_to_pretty_str(carte) for carte in self.table.cartes_communautaires]), "\n")

    def recuperer_mise_max(self, tab):
        """
        Retourne la mise maximale dans une liste de mises.
        """
        return max(tab)

    def tour_de_mise(self):
        """
        Gère un tour de mise, permettant aux joueurs de miser, suivre ou se coucher.
        """
        mises_joueurs = []
        for joueur in self.table.joueurs:
            if self.joueur_en_jeu(0) >= 2 and joueur.en_jeu and not joueur.hors_jeu():
                while True:
                    if mises_joueurs:
                        action = input(
                            f"{joueur.nom}, voulez-vous 'suivre', 'miser' ou 'se coucher' ? : ").strip().lower()
                    else:
                        action = input(
                            f"{joueur.nom}, voulez-vous 'miser' ou 'se coucher' ? : ").strip().lower()

                    if action == "miser":
                        try:
                            montant = int(input("Entrez le montant à miser : "))
                            if montant <= 0:
                                print("Le montant doit être supérieur à 0.")
                                continue
                            if mises_joueurs and self.recuperer_mise_max(mises_joueurs) > montant:
                                print("Le montant doit être égale ou supérieur à la mise minimale qui est de ",
                                      self.recuperer_mise_max(mises_joueurs))
                                continue
                            self.table.pot += joueur.miser(montant)
                            mises_joueurs.append(montant)
                            break
                        except ValueError:
                            print("Veuillez entrer un montant valide.")
                        except Exception as e:
                            print(e)

                    elif action == "se coucher":
                        joueur.se_coucher()
                        break

                    elif action == "suivre":
                        try:
                            if len(mises_joueurs) == 0:
                                print(joueur.nom, " ne peut pas suivre car c'est la première mise du tour.")
                                continue
                            montant = self.recuperer_mise_max(mises_joueurs)
                            print(joueur.nom, " suivre en misant ", montant, " jetons.")
                            self.table.pot += joueur.miser(montant)
                            mises_joueurs.append(montant)
                            break
                        except Exception as e:
                            print(e)

                    else:
                        if mises_joueurs:
                            print("Action invalide. Veuillez choisir 'miser', 'suivre', ou 'se coucher'.")
                        else:
                            print("Action invalide. Veuillez choisir 'miser' ou 'se coucher'.")
            print()

    def jouer_partie(self):
        """
        Lance une partie complète jusqu'à ce qu'il ne reste qu'un seul joueur avec des jetons.
        """
        self.jouer()
        self.tour += 1
        while self.nb_joueur_avec_jetons() > 1:
            self.jouer()
            self.tour += 1
        print("La partie est terminée. Le gagnant est", self.get_gagnant().nom)

    def get_gagnant(self):
        """
        Retourne le joueur gagnant de la partie.
        """
        for joueur in self.joueurs:
            if joueur.jetons > 0:
                return joueur

    def jouer(self):
        """
        Gère un tour de jeu, y compris la distribution des cartes et les phases (flop, turn, river).
        """
        if self.tour == 0:
            self.initialiser_joueurs()
        else:
            self.table.nouveau_paquet()
            clear_terminal()
        if self.result:
            print(f'{self.result[0]} a gagné : {self.result[1]} ({self.result[2]} jetons)')
        print(f"\n------------------- Tour {self.tour + 1} -------------------\n")
        self.distribuer_cartes()

        phases = ["flop", "turn", "river"]
        for phase in phases:
            self.effectuer_phase(phase)
            if self.nb_joueur_avec_jetons() > 1:
                print("Joueurs après distribution des cartes :")
                self.afficher_joueurs()
                self.table.afficher_pot()
                self.tour_de_mise()
            else:
                time.sleep(3)
            clear_terminal()

        print("Phase finale :\n")

        print("Cartes sur la table :",
              " ".join([Card.int_to_pretty_str(carte) for carte in self.table.cartes_communautaires]))
        print("\nPot final :", self.table.pot)
        self.get_result()
        time.sleep(2)
        self.restart_game()

    def nb_joueur_avec_jetons(self):
        """
        Retourne le nombre de joueurs avec des jetons.
        """
        res = 0
        for joueur in self.joueurs:
            if joueur.jetons > 0 and joueur.en_jeu:
                res += 1
        return res

    def joueur_en_jeu(self, i):
        """
        Retourne le nombre de joueurs présents encore dans la manche.
        """
        if i >= len(self.joueurs):
            return 0
        elif not self.joueurs[i].hors_jeu() and self.joueurs[i].en_jeu:
            return self.joueur_en_jeu(i + 1) + 1
        else:
            return self.joueur_en_jeu(i + 1)

    def get_result(self):
        """
        Évalue les mains des joueurs et détermine le gagnant du tour.
        """
        evaluator = Evaluator()
        resultats = {}
        type_result = {}

        for joueur in self.joueurs:
            if joueur.en_jeu and not joueur.hors_jeu():
                res = evaluator.evaluate(self.table.cartes_communautaires, joueur.cartes_en_main)
                resultats[joueur] = res
                type_result[joueur] = evaluator.class_to_string(evaluator.get_rank_class(res))

        gagnant = max(resultats, key=resultats.get)
        gagnant.jetons += self.table.pot

        self.result = [gagnant.nom, type_result[gagnant], self.table.pot]

    def restart_game(self):
        """
        Réinitialise l'état des joueurs pour une nouvelle manche.
        """
        for joueur in self.joueurs:
            if joueur.hors_jeu():
                joueur.en_jeu = False
            else:
                joueur.en_jeu = True
