Budeanski Nikita.

Auto-evaluation:
    Travail seul
    Je note mon travail 20/20. Toutes les fonctionnalités ont été implémenté à partir d'un barème pour 1 personne.

Les points sur lesquels j'etais restés bloqués:
    Je ne suis resté bloqué sur aucun des points. Je voulais créer plus de fonctionnalités supplémentaires, mais je n’avais pas assez de temps.

Les points que j'ai pu améliorer entre la démo et le rendu:
    1. J'ai trouvé 2 bugs et les fixé.

REMARQUE: J'ai vu très tard un message sur la nécessité de faire constamment des copies de sauvegarde du projet. Je n'ai que 2 versions stables. J'ai utilisé un système de contrôle de version (git). Il n'y a que 2 commits (2 versions stables). Le deuxième commit diffère du premier en ce sens que 2 bugs ont été corrigés et que la possibilité d'envoyer un message privé à plus d'un utilisateur a été ajoutée.

En plus de ce qui était indiqué dans le barème pour 1 personne, etait fait:
1. Gestion des statuts des joueurs (disconnected manualy, banned, active)
2. Terminaison correcte de tous les processus-fils (sans laisser de processus zombies)
3. Ajout d'une fonctionnalité permettant à l'administrateur, dans une fenêtre de terminal séparée, de voir tous les messages envoyés, y compris mêmes les messages privés des utilisateurs.
4. L'administrateur peut envoyer et recevoir des messages de la part des utilisateurs.
5. Si un joueur est bloqué pendant une partie, il ne pourra plus se reconnecter à la partie en cours.
6. Le serveur peut informer tous les joueurs si quelqu'un est bloqué.
7. Lorsqu'un joueur est bloqué, tous les fichiers associés à ce joueur sont supprimés. En cas de déconnexion autonome ou de panne du système, tous les fichiers sont supprimés à l'exception du dossier contenant les cookies de l'utilisateur, afin qu'il puisse se reconnecter ultérieurement.
8. Le système est assez tolérant aux erreurs. J'ai effectué de nombreux tests sur une grande variété de cas et généralement le programme ne se termine pas en raison d'exceptions.

REMARQUE: J'ai redirigé la sortie d'erreur et des "warnings" vers un autre fichier. Autrement dit, vous ne verrez pas d'éventuelles erreurs dans le terminal. Ceci est dû au fait que xterm génère de nombreux "warnings" dans le terminal, ce qui obstrue la sortie standard de l'application.
Vous pouvez désactiver cette option en supprimant la ligne 165 sur le client et la ligne 98 sur le serveur.