#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 08:08:39 2026

@author: mddiop
"""

class Voyage:
    """Modèle de données centralisant l'état et l'organisation logique du voyage.

    Contient les informations sélectionnées par l'utilisateur (trains, hôtel, activités) et contient les algorithmes de calcul de distances, d'optimisation de parcours et de génération d'itinéraires.
    """ 
    def __init__(self, ville_depart, ville_arrivee, date_aller, date_retour, train_aller, train_retour, hotel, activites_selectionnees):
        """Initialise l'ensemble des variables nécessaires au suivi du voyage."""
        self.ville_depart = ville_depart
        self.ville_arrivee = ville_arrivee
        self.date_aller = date_aller
        self.date_retour = date_retour
        self.train_aller = train_aller 
        self.train_retour = train_retour
        self.hotel = hotel
        self.activites_selectionnees = activites_selectionnees 
        
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

        pos_actuelle = (self.hotel["lat"], self.hotel["lon"])
        restantes = list(liste_activites)
        ordenadas = []

        while restantes:
            mas_cercana = None
            distancia_min = float('inf')

            for act in restantes:
                dist = self.calculer_distance(pos_actuelle, (act["lat"], act["lon"]))
                if dist < distancia_min:
                    distancia_min = dist
                    mas_cercana = act

            ordenadas.append(mas_cercana)
            restantes.remove(mas_cercana)
            pos_actuelle = (mas_cercana["lat"], mas_cercana["lon"])

        return ordenadas

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
            dia = i // 3
            if dia not in planning:
                planning[dia] = []
            planning[dia].append(activites[i])
        return planning

    def liste_planning(self, planning):
        """transforme le dictionnaire de planning en une liste linéaire d'activités.

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
            Chaque élément possède les clés : `"jour"`, `"txt"` (libellé de l'action/activité) 
            et `"trajet"` (kilométrage et durée estimée).
        """
        itinerario = []

        if self.train_aller:
            itinerario.append({"jour": "Jour 1", "txt": f"Départ {self.ville_dep}", "transit": ""})
            itinerario.append({"jour": None, "txt": f"Arrivée {self.ville_arr}", "transit": ""})

        if self.hotel:
            itinerario.append({"jour": None, "txt": f"Installation: {self.hotel['nom']}", "transit": ""})
            svg_lat, svg_lon = self.hotel["lat"], self.hotel["lon"]
        else:
            svg_lat, svg_lon = 0, 0

        total_act = len(self.activites_selectionnees)
        i = 0
        dia_actual = 2

        while i < total_act:
            if i % 3 == 0:
                itinerario.append({"jour": f"— Jour {dia_actual} —", "txt": "Départ de l'hôtel", "transit": ""})
                if self.hotel:
                    svg_lat, svg_lon = self.hotel["lat"], self.hotel["lon"]

            act = self.activites_selectionnees[i]
            distancia = 0

            if svg_lat != 0 and svg_lon != 0:
                distancia = self.calculer_distance((svg_lat, svg_lon), (act["lat"], act["lon"]))

            tiempo = int(distancia / 5 * 60)
            info_transito = f"({round(distancia, 1)} km • {tiempo} min)" if distancia > 0 else ""

            itinerario.append({"jour": None, "txt": act["nom"], "transit": info_transito})
            svg_lat, svg_lon = act["lat"], act["lon"]

            if (i + 1) % 3 == 0 or (i + 1) == total_act:
                if self.hotel:
                    dist_retorno = self.calculer_distance((svg_lat, svg_lon), (self.hotel["lat"], self.hotel["lon"]))
                    tiempo_retorno = int(dist_retorno / 5 * 60)
                    itinerario.append({"jour": None, "txt": "Retour hôtel", "transit": f"({round(dist_retorno, 1)} km • {tiempo_retorno} min)"})
                dia_actual += 1

            i += 1

        if self.train_retour:
            itinerario.append({"jour": "Retour", "txt": f"Retour vers {self.ville_dep}", "transit": ""})

        return itinerario


  