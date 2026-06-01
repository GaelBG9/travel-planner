import math

CATEGORIES_ACTIVITES = {
    "Culture (Musées...)": {"tourism": ["museum", "artwork", "gallery"]},
    "Monuments":           {"tourism": ["attraction", "viewpoint", "monument"]},
    "Parcs & Loisirs":     {"leisure": ["park", "garden", "theme_park"]},
    "Gastronomie":         {"amenity": ["restaurant", "cafe"]}
}

class Voyage:
     """
    Classe représentant l'état global du voyage planifié. 
    Elle stocke les choix de l'utilisateur à mesure qu'il avance dans les étapes.
    """

    def __init__(self):
        """Initialise l'ensemble des variables nécessaires au suivi du voyage."""
        self.ville_dep = "Paris"
        self.ville_arr = "Lyon"
        self.train_aller = None
        self.train_retour = None
        self.hotel = None
        self.activites_selectionnees = []
        self.categories_souhaitees = []
        self.max_activites = 0
        self.lat_ville = 0
        self.lon_ville = 0

    def calculer_distance(self, p1, p2):
        """Calcule la distance à vol d'oiseau entre deux coordonnées GPS.

        Utilise la formule de Haversine pour prendre en compte la courbure terrestre.

        Args:
            p1 (tuple[float, float]): Coordonnées (lat, lon) du premier point.
            p2 (tuple[float, float]): Coordonnées (lat, lon) du second point.

        Returns:
            float: La distance calculée en kilomètres.
        """
        if not p1 or not p2:
            return 0
        R = 6371
        lat1, lat2 = math.radians(p1[0]), math.radians(p2[0])
        diff_lat = math.radians(p2[0] - p1[0])
        diff_lon = math.radians(p2[1] - p1[1])
        a = math.sin(diff_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(diff_lon / 2) ** 2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    def optimiser_parcours(self, liste_activites):
        """Trie et réorganise une liste d'activités selon la proximité géographique.

        Applique la méthode heuristique du "voisin le plus proche" à partir de l'adresse de l'hôtel pour réduire le temps global de transport.

        Args:
            liste_activites (list[dict]): Liste brute des activités à trier.

        Returns:
            list[dict]: Une nouvelle liste d'activités ordonnée de façon optimale.
        """
        if not liste_activites:
            return []

        position_actuelle = (self.hotel["lat"], self.hotel["lon"])
        restantes = list(liste_activites)
        triees = []

        while restantes:
            plus_proche = None
            distance_min = float('inf')

            for act in restantes:
                dist = self.calculer_distance(position_actuelle, (act["lat"], act["lon"]))
                if dist < distance_min:
                    distance_min = dist
                    plus_proche = act

            triees.append(plus_proche)
            restantes.remove(plus_proche)
            position_actuelle = (plus_proche["lat"], plus_proche["lon"])

        return triees

    def construire_planning(self, activites):
        """Répartit de façon séquentielle les activités au sein d'un dictionnaire par journées.

        Le quota maximum appliqué ici est fixé à 3 activités par jour.

        Args:
            activites (list[dict]): Liste ordonnée des activités retenues.

        Returns:
            dict[int, list[dict]]: dictionnaire indexant chaque journée.
        """
        planning = {}
        for i in range(len(activites)):
            jour = i // 3
            if jour not in planning:
                planning[jour] = []
            planning[jour].append(activites[i])
        return planning

    def liste_planning(self, planning):
        """Transforme le dictionnaire de planning en une liste linéaire d'activités.

        Utile pour réinjecter les données modifiées après un réagencement manuel.

        Args:
            planning (dict[int, list[dict]]): Dictionnaire représentatif du planning actuel.

        Returns:
            list[dict]: Liste brute d'activités ordonnées chronologiquement selon l'index des jours.
        """
        liste = []
        jours_ordonnes = sorted(planning.keys())
        for j in jours_ordonnes:
            for act in planning[j]:
                liste.append(act)
        return liste

    def calculer_itineraire(self):
        """Génère la structure détaillée du carnet de route final.

        Calcule dynamiquement les distances réelles et estime le temps de trajet à pied (sur une base moyenne standard de 5 km/h) entre chaque activité et l'hôtel.

        Returns:
            list[dict]: Liste d'étapes décrivant le déroulement du séjour.
            Chaque élément possède les clés : "jour", "txt" (libellé de l'action/activité)
            et "transit" (kilométrage et durée estimée).
        """
        itineraire = []

        if self.train_aller:
            itineraire.append({"jour": "Jour 1", "txt": f"Départ {self.ville_dep}", "transit": ""})
            itineraire.append({"jour": None, "txt": f"Arrivée {self.ville_arr}", "transit": ""})

        if self.hotel:
            itineraire.append({"jour": None, "txt": f"Installation: {self.hotel['nom']}", "transit": ""})
            derniere_lat, derniere_lon = self.hotel["lat"], self.hotel["lon"]
        else:
            derniere_lat, derniere_lon = 0, 0

        total_act = len(self.activites_selectionnees)
        i = 0
        jour_actuel = 2

        while i < total_act:
            if i % 3 == 0:
                itineraire.append({"jour": f"— Jour {jour_actuel} —", "txt": "Départ de l'hôtel", "transit": ""})
                if self.hotel:
                    derniere_lat, derniere_lon = self.hotel["lat"], self.hotel["lon"]

            act = self.activites_selectionnees[i]
            distance = 0

            if derniere_lat != 0 and derniere_lon != 0:
                distance = self.calculer_distance((derniere_lat, derniere_lon), (act["lat"], act["lon"]))

            temps = int(distance / 5 * 60)
            info_transit = f"({round(distance, 1)} km • {temps} min)" if distance > 0 else ""

            itineraire.append({"jour": None, "txt": act["nom"], "transit": info_transit})
            derniere_lat, derniere_lon = act["lat"], act["lon"]

            if (i + 1) % 3 == 0 or (i + 1) == total_act:
                if self.hotel:
                    dist_retour = self.calculer_distance((derniere_lat, derniere_lon), (self.hotel["lat"], self.hotel["lon"]))
                    temps_retour = int(dist_retour / 5 * 60)
                    itineraire.append({"jour": None, "txt": "Retour hôtel", "transit": f"({round(dist_retour, 1)} km • {temps_retour} min)"})
                jour_actuel += 1

            i += 1

        if self.train_retour:
            itineraire.append({"jour": "Retour", "txt": f"Retour vers {self.ville_dep}", "transit": ""})

        return itineraire