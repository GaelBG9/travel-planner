from datetime import datetime

from class_train import Train
from points_interets import PointsInteret
from classe_voyage import Voyage
from Vue import Vue

class Controleur:
    """
    Contrôleur (MVC). Reçoit les ordres de la vue, modifie l'état des modèles de données, et ordonne à la vue de se mettre à jour en conséquence.
    """
    def __init__(self):
        """
        Instancie les différents modèles métiers (APIs, algorithmes, variables d'état) 
        et initialise l'interface graphique (Vue).
        """
        self.mod_train = Train()
        self.mod_poi = PointsInteret()
        self.voyage = Voyage()
        self.vue = Vue(self)
        self.activites_temporaires = []
        self.planning_actuel = {}
        self.index_echange = None

    def lancer(self):
        """
        Commande à la vue d'afficher le tout premier écran (formulaire de configuration).
        """
        self.vue.afficher_recherche()
        self.vue.mainloop()

    def lancer_recherche_trains(self, v_dep, v_arr, d_all, h_all, d_ret, h_ret, cats, dt_all, dt_ret):
        """
        Appelée lors de la validation du formulaire. Elle calcule les jours sur place (pour borner les activités),
        récupère les itinéraires SNCF via le modèle, trouve le plus rapide, et déclenche l'affichage dans la vue.
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
        """
        Sauvegarde le trajet de train spécifique cliqué par l'utilisateur (aller ou retour)
        dans l'état global du modèle, puis indique à la vue de colorer le bouton pour valider l'action.
        """
        if cle == "ALLER":
            self.voyage.train_aller = train
        else:
            self.voyage.train_retour = train

        self.vue.mettre_a_jour_boutons_train(train, cle)

    def lancer_recherche_hotels(self):
        """
        Récupère le centre géographique de la ville d'arrivée,
        lance le téléchargement des hôtels depuis OpenStreetMap, puis demande à la vue d'afficher la grille.
        """
        self.vue.afficher_chargement(f"Recherche des hôtels à {self.voyage.ville_arr}...")
        self.vue.update()

        lat, lon = self.mod_poi.obtenir_coordonnees_ville(self.voyage.ville_arr)
        self.voyage.lat_ville = lat
        self.voyage.lon_ville = lon
        hotels = self.mod_poi.chercher_hotels(self.voyage.ville_arr)
        self.vue.afficher_selection_hotels(hotels)

    def choisir_hotel(self, hotel):
        """
        Stocke le dictionnaire de l'hôtel sélectionné par l'utilisateur dans l'objet ModeleVoyage
        et déclenche automatiquement la transition vers l'étape de recherche des activités.
        """
        self.voyage.hotel = hotel
        self.lancer_recherche_activites()

    def lancer_recherche_activites(self):
        """
        Déclenche l'extraction des points d'intérêt depuis OSMnx en fonction des 
        catégories souhaitées, puis ordonne à la Vue d'afficher le menu de sélection à l'utilisateur.
        """
        self.vue.afficher_chargement("Recherche des activités...")
        self.vue.update()

        activites = self.mod_poi.chercher_activites(self.voyage.ville_arr, self.voyage.categories_souhaitees)
        self.vue.afficher_selection_activites(activites, self.voyage.max_activites)

    
    def gerer_selection_activite(self, act, est_coche):
        """
        Vérifie si on a le droit d'ajouter une activité au panier.
        Retourne True si l'opération est autorisée, False sinon (limite atteinte).
        """
        if est_coche:
            if len(self.activites_temporaires) >= self.voyage.max_activites:
                self.vue.actualiser_compteur_activites(len(self.activites_temporaires), self.voyage.max_activites, alerte=True)
                return False 
            self.activites_temporaires.append(act)
        else:
            if act in self.activites_temporaires:
                self.activites_temporaires.remove(act)
                
        self.vue.actualiser_compteur_activites(len(self.activites_temporaires), self.voyage.max_activites, alerte=False)
        return True

    def lancer_planification(self):
        """
        Recoit la liste finale des activités souhaitées, appelle l'algorithme d'optimisation
        du parcours, structure le planning par jours, et déclenche l'affichage de l'édition 
        """
        activites_optimizadas = self.voyage.optimiser_parcours(self.activites_temporaires)
        self.planning_actuel = self.voyage.construire_planning(activites_optimizadas)
        self.index_echange = None
        self.vue.afficher_planification(self.planning_actuel)

    
    def reordonner_planning(self, jour, idx):
        """
        Logique d'échange de deux activités. Appelée par la Vue à chaque clic sur "Échanger".
        """
        if self.index_echange is None:
            self.index_echange = (jour, idx)
        else:
            j1, i1 = self.index_echange
            j2, i2 = jour, idx

            if not (j1 == j2 and i1 == i2):
                act1 = self.planning_actuel[j1][i1]
                act2 = self.planning_actuel[j2][i2]

                self.planning_actuel[j1][i1] = act2
                self.planning_actuel[j2][i2] = act1
                self.voyage.activites_selectionnees = self.voyage.liste_planning(self.planning_actuel)
            self.index_echange = None
        self.vue.afficher_jours(self.planning_actuel, self.index_echange)

    def mettre_a_jour_planning(self, planning):
        """
        Met à jour la mémoire interne du modèle lorsque l'utilisateur utilise l'interface
        pour échanger manuellement l'ordre chronologique des activités.
        """
        self.voyage.activites_selectionnees = self.voyage.liste_planning(planning)

    def lancer_generation_carnet(self):
        """
        Finalise le voyage complet. Extrait la dernière version du planning, 
        construit la chronologie détaillée de bout en bout (trains + hôtels + transits) et l'affiche.
        """
        self.voyage.activites_selectionnees = self.voyage.liste_planning(self.planning_actuel)
        itineraire = self.voyage.calculer_itineraire()
        self.vue.afficher_final(
            itineraire,
            self.voyage.lat_ville,
            self.voyage.lon_ville,
            self.voyage.hotel,
            self.voyage.activites_selectionnees
        )

    def definir_destination(self, ville):
        """Met à jour le modèle avec la nouvelle destination et notifie la vue."""
        self.voyage.ville_arr = ville
        self.vue.mettre_a_jour_destination(ville)

    def valider_recherche_globale(self, v_dep, v_arr, j_all, m_all, a_all, h_all, j_ret, m_ret, a_ret, h_ret, cat_vars):
        """
        Contrôle la logique des dates et prépare les données avant de lancer la recherche.
        """
        d_all = f"{a_all}-{m_all}-{j_all}"
        d_ret = f"{a_ret}-{m_ret}-{j_ret}"
        
        dt_all = datetime.strptime(d_all, "%Y-%m-%d")
        dt_ret = datetime.strptime(d_ret, "%Y-%m-%d")

        if dt_ret <= dt_all:
            self.vue.afficher_erreur("La date de retour doit être après la date d'aller !")
            return

        cats = [cat for cat, var in cat_vars.items() if var.get()]

        self.lancer_recherche_trains(v_dep, v_arr, d_all, h_all, d_ret, h_ret, cats, dt_all, dt_ret)
        