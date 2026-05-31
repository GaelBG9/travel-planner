# Projet ISN - Agence de voyage

Nous avons entrepris de créer un "kit de voyage" permettant de préparer à votre place vos vacances. Il organise l'ensemble du voyage, du transport aux activités, en passant par l'hôtel. Vous choisisez les dates et les villes de départ et d'arrivée, le type d'activité que vous souhaitez faire et l'application vous prépare votre voyage en fonctions de vos goûts et de la durée de vos vacances.

Nous avons réalisé ce projet dans le cadre de l'ISN : il s'agit d'un projet sur 5 séances. Celui-ci n'est donc pas parfait notamment au niveau de la durée des requêtes : nous vous demandons donc d'être patient. 

## Mise en route
### Installation
Cloner le dépôt ou copier les fichiers dans un même dossier. L'application nécessite plusieurs bibliothèques. Dans un terminal, exécuter :
pip install customtkinter tkintermapview requests osmnx pillow pandas
### Photos des villes (optionnel)
Pour afficher des photos sur la page d'accueil, placer des fichiers .jpg nommés exactement comme les villes dans le même dossier que les scripts :
Paris.jpg, Lyon.jpg, Marseille.jpg, Nice.jpg, Bordeaux.jpg ...
### Exécution de l'application
Dans le dossier du projet, exécuter simplement :
python main.py


## Utilisation

Pour utiliser l'application, rien de plus simple : il suffit de démarrer le programme Main.py. Grâce à l'interface graphique, les différentes étapes sont explicités. 
Il faudra ensuite renseigner les informations sur notre voyage telles que les dates et les villes de départ et de retour afin de vous proposez des trains qui vous confiennent.
Il faudra ensuite renseigner vos centres d'intérêt afin de vous proposez une liste d'activités qui vous conviennent : vous pourrez alors choisir les activités que vous souhaitez faire puis l'application vous proposera un programme adapter aux différentes contraintes.
