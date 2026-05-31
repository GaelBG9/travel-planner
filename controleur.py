from class_train import Train
from points_interets import PointsInteret
from classe_voyage import Voyage

class Controleur:

    def __init__(self):
        """Initialise les instances des modules du modèle et prépare l'attribut de la vue."""
        self.mod_train = Train()
        self.mod_poi = PointsInteret()
        self.voyage = Voyage()
        # La vue est assignée après, depuis main.py
        self.vue = None

    def lancer(self):
        """Démarre l'application en affichant l'écran de configuration initial."""
        self.vue.afficher_recherche()
        self.vue.mainloop()

    def lancer_recherche_trains(self, v_dep, v_arr, d_all, h_all, d_ret, h_ret, cats, dt_all, dt_ret):
       """Enregistre les données de base et effectue la recherche d'itinéraires ferroviaires.
       Calcule le nombre maximal d'activités possibles selon la durée du séjour,
       puis appelle le module de transport pour lister les trajets disponibles.

       Parametres:
           v_dep (string): Ville de départ.
           v_arr (string): Ville d'arrivée.
           d_all (string): Date du trajet aller.
           h_all (string): Heure souhaitée pour l'aller.
           d_ret (string): Date du trajet retour.
           h_ret (string): Heure souhaitée pour le retour.
           cats (liste de string): Liste des catégories d'activités filtrées.
           dt_all (datetime): Objet datetime de la date aller.
           dt_ret (datetime): Objet datetime de la date retour.
       """ 
       self.voyage.ville_dep = v_dep
       self.voyage.ville_arr = v_arr
       self.voyage.categories_souhaitees = cats

       jours_sur_place = (dt_ret - dt_all).days + 1
       self.voyage.max_activites = jours_sur_place * 3

       self.vue.afficher_chargement("Connexion à l'API SNCF...")
       self.vue.update()

       t_all = self.mod_train.chercher_trajets(v_dep, v_arr, d_all, h_all)
       t_ret = self.mod_train.chercher_trajets(v_arr, v_dep, d_ret, h_ret)

       idx_rapide_aller  = self.mod_train.trouver_index_rapide(t_all)
       idx_rapide_retour = self.mod_train.trouver_index_rapide(t_ret)

       self.vue.afficher_selection_trains(t_all, t_ret, idx_rapide_aller, idx_rapide_retour)

    def choisir_train(self, train, cle):
        """Assigne le train sélectionné par l'utilisateur au modèle et rafraîchit la vue.

        Parametres:
            train (dictionnaire): Données du train choisi.
            cle (string): Nature du billet concerné ("ALLER" ou "RETOUR").
        """
        if cle == "ALLER":
            self.voyage.train_aller = train
        else:
            self.voyage.train_retour = train
        self.vue.mettre_a_jour_boutons_train(train, cle)
        
    def lancer_recherche_hotels(self):
        """Récupère les coordonnées de la ville d'arrivée et recherche les hébergements disponibles."""
        self.vue.afficher_chargement(f"Recherche des hôtels à {self.voyage.ville_arr}...")
        self.vue.update()
        lat, lon = self.mod_poi.obtenir_coordonnees_ville(self.voyage.ville_arr)
        self.voyage.lat_ville = lat
        self.voyage.lon_ville = lon
        hotels = self.mod_poi.chercher_hotels(self.voyage.ville_arr)
        self.vue.afficher_selection_hotels(hotels)
    
    def choisir_hotel(self, hotel):
        """Assigne l'hôtel sélectionné et bascule automatiquement sur la recherche d'activités.

        Parametres:
            hotel (dictionnaire): Données de l'hôtel sélectionné.
        """
        self.voyage.hotel = hotel
        self.lancer_recherche_activites()

    def lancer_recherche_activites(self):
        """Interroge OpenStreetMap via le modèle pour lister les points d'intérêt disponibles selon les catégories."""
        self.vue.afficher_chargement("Recherche des activités...")
        self.vue.update()

        activites  = self.mod_poi.chercher_activites(self.voyage.ville_arr, self.voyage.categories_souhaitees)
        self.vue.afficher_selection_activites(activites, self.voyage.max_activites)

    def lancer_planification(self, activites_cochees):
        """Optimise géographiquement le parcours des activités choisies et génère le planning initial.

        Parametres:
            activites_cochees (liste de dictionnaires): Liste des activités cochées par l'utilisateur.
        """
        activites_optimisees = self.voyage.optimiser_parcours(activites_cochees)
        planning = self.voyage.construire_planning(activites_optimisees)
        self.vue.afficher_planification(planning)

    def mettre_a_jour_planning(self, planning):
        """Met à jour l'ordre à plat des activités stocké dans le modèle suite à une modification.

        Parametres:
            planning (dictionnaire): Dictionnaire représentant le planning modifié.
        """
        self.voyage.activites_selectionnees = self.voyage.liste_planning(planning)

    def lancer_generation_carnet(self, planning):
        """Compile les choix finaux, génère l'itinéraire chronologique et bascule sur l'écran final de synthèse.

        Parametres:
            planning (dictionnaire): Dictionnaire du planning validé par l'utilisateur.
        """
        self.voyage.activites_selectionnees = self.voyage.liste_planning(planning)
        itineraire = self.voyage.calculer_itineraire()
        self.vue.afficher_final(
            itineraire,
            self.voyage.lat_ville,
            self.voyage.lon_ville,
            self.voyage.hotel,
            self.voyage.activites_selectionnees
        )
        