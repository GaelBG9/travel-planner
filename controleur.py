class Controleur:

    def __init__(self):
        self.mod_train = ModeleTrain()
        self.mod_poi = ModelePointsInteret()
        self.voyage = ModeleVoyage()
        self.vue = Vue(self)

    def lancer(self):
        self.vue.afficher_recherche()
        self.vue.mainloop()

    def lancer_recherche_trains(self, v_dep, v_arr, d_all, h_all, d_ret, h_ret, cats):
        self.voyage.ville_dep = v_dep
        self.voyage.ville_arr = v_arr
        self.voyage.date_aller = d_all
        self.voyage.heure_aller = h_all
        self.voyage.date_retour = d_ret
        self.voyage.heure_retour = h_ret
        self.voyage.categories_souhaitees = cats
        self.vue.afficher_chargement("Connexion à l'API SNCF...")


    def lancer_recherche_hotels(self):
        self.vue.afficher_chargement(f"Recherche des hôtels à {self.voyage.ville_arr}...")
    def lancer_recherche_activites(self):
        self.vue.afficher_chargement("Recherche des activités...")