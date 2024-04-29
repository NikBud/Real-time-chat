Budeanski Nikita.
A travaillé seul.
Je note mon travail 20/20. Toutes les fonctionnalités ont été implémenté à partir d'un barem pour 1 personne.

En plus fait:
1. Gestion des statuts des joueurs
2. Terminaison correcte de tous les processus-fils (sans laisser de processus zombies)
3. Ajout d'une fonctionnalité permettant à l'administrateur, dans une fenêtre de terminal séparée, de voir tous les messages envoyés, y compris mêmes les messages privés des utilisateurs.
4. L'administrateur peut envoyer et recevoir des messages de la part des utilisateurs.
5. Si un joueur est bloqué pendant une partie, il ne pourra plus se reconnecter à la partie en cours.
6. Le serveur peut informer tous les joueurs si quelqu'un est bloqué.
7. Lorsqu'un joueur est bloqué, tous les fichiers associés à ce joueur sont supprimés. En cas de déconnexion autonome ou de panne du système, tous les fichiers sont supprimés à l'exception du dossier contenant les cookies de l'utilisateur, afin qu'il puisse se reconnecter ultérieurement.



Дополнительно сделано:
    1. Управление статусами игроков
    2. Правильное завершение всех дочерних процессов (без того, чтобы оставлять процессы-зомби)
    3. Добавлена возможность Админу видеть абсолютно все отправленные сообщения, даже личные.
    4. Админ может отправлять и получать сообщения от пользователей
    5. Если игрока забанили во время игры, то он уже не сможет переподключиться к текущей игре.
    6. Сервер может сообщает всем игрокам если кого-то забанили.
    7. При заблокировании игрока удаляются все файлы, которые связаны с этим игроком. При этом при самостоятельном отключении или в случае сбоя системы удаляются все файлы, кроме папки с cookies пользователя. Чтобы пользователь мог переводключиться в дальнейшем.

Что еще сделать:
    1. Реализовать протокол HEARTBEAT ?