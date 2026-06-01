# Projet ISN S4 - VOYAGE VOYAGE

### Description

Ce projet permet de planifier un voyage complet en train et de créer des itinéraires optimisés pour visiter des lieux une fois sur place. L’ordre de visite est défini de manière à minimiser la distance de marche entre les lieux successifs.

L'utilisateur saisit :

* une ville de départ et une ville d'arrivée (en France),
* une date et heure d'aller, ainsi qu'une date et heure de retour,
* les catégories de lieux qu’il souhaite visiter (Musées, Parcs, Monuments, Gastronomie),
* ainsi que l’hébergement de son choix.

L’algorithme interroge d'abord l'API SNCF pour proposer les meilleurs trajets ferroviaires. Ensuite, il génère un itinéraire quotidien dont le point de départ et d’arrivée est l’hôtel fourni par l’utilisateur. Chaque jour comprend un maximum de 3 lieux à visiter, ordonnés pour minimiser les distances via un algorithme du plus proche voisin.

Les lieux et les hôtels sont sélectionnés à partir des données d’OpenStreetMap via la bibliothèque `osmnx`, garantissant des coordonnées réelles.

### Mise en route

**Installation:**

Cloner le dépôt : Sur linux :

```bash
git clone https://gitlab.insa-lyon.fr/projet-isn-[TON_GROUPE]/voyage-voyage.git && cd voyage-voyage

```

L'application a besoin de quelques librairies. Pour installer toutes les dépendances nécessaires, exécutez simplement la commande suivante dans votre terminal :

```bash
pip install customtkinter tkintermapview requests pandas osmnx Pillow
```
### Exécution de l'application

Dans le dossier du projet, exécutez simplement `python main.py` et tout devrait fonctionner normalement.

```bash
python main.py

```

### Instructions:

**Fenêtre de Configuration**

* L'utilisateur indique la ville de départ et d'arrivée - (IMPORTANT : en raison de l'utilisation de l'API SNCF, il doit s'agir de villes françaises desservies par le réseau).
* L'utilisateur saisit également les dates et heures, et coche les catégories souhaitées.
* Une fois toutes les étapes effectuées, pour passer à l'étape suivante, l'utilisateur clique sur « Rechercher Itinéraires ».

**Fenêtre des Trains :**

* Dans cette fenêtre, l'utilisateur voit les 5 meilleurs trajets trouvés. Le trajet le plus court est mis en évidence (⚡ RAPIDE).
* L'utilisateur doit choisir un trajet aller et un trajet retour, puis valider.

**Fenêtre de la carte (Hébergement) :**

* Des hébergements lui seront proposés sous forme de grille. En raison des limitations d'osmnx, certains hébergements mineurs peuvent ne pas être présents.
* L'utilisateur clique sur « Réserver » sous l'hôtel de son choix pour passer à la suite.

**Fenêtre de Sélection des Activités :**

* L'utilisateur peut cocher les activités qu'il souhaite réellement faire. Un compteur limite la sélection à 3 activités par jour sur place (calculé selon les dates de train).
* Une fois la sélection terminée, il clique sur « Planifier mes journées ».

**Fenêtre de Planification :**

* L'itinéraire optimisé est affiché jour par jour.
* Si l'ordre ne convient pas, l'utilisateur peut cliquer sur le bouton « ⇄ Échanger » de deux activités différentes pour modifier manuellement le planning.
* Pour conclure, il clique sur « Générer le Carnet ».

**Fenêtre du Carnet de Route :**

* Le programme affiche la carte finale interactive avec les marqueurs numérotés et un résumé textuel à droite incluant les estimations de temps de marche entre chaque étape.

### Auteurs

* Gaël Boënnec
* [Nom de tes éventuels camarades de binôme/groupe]