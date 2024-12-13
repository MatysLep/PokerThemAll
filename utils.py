import os
import subprocess


def clear_terminal():
    """
    Efface le contenu affiché dans le terminal ou la console.

    Fonctionnement :
        - Sur les systèmes Windows, utilise la commande 'cls'.
        - Sur les systèmes Unix/Linux/MacOS, utilise la commande 'clear'.

    Utilise la bibliothèque subprocess pour exécuter la commande appropriée en fonction du système
    d'exploitation.

    Exceptions :
        - La fonction suppose que les commandes 'cls' ou 'clear' sont disponibles dans l'environnement.

    Exemple d'utilisation :
        clear_terminal()
    """
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)
