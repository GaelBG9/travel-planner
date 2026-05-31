#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 08:08:39 2026

@author: mddiop
"""

class Voyage:
    def __init__(self, ville_depart, ville_arrivee, date_aller, date_retour, train_aller, train_retour, hotel, activites_selectionnees):
        self.ville_depart = ville_depart
        self.ville_arrivee = ville_arrivee
        self.date_aller = date_aller
        self.date_retour = date_retour
        self.train_aller = train_aller #On a un objet qui a comme propiété la durée
        self.train_retour = train_retour
        self.hotel = hotel
        self.activites_selectionnees = activites_selectionnees #On a ue activité min par jour et 3 max
        
        
    def calcul_itineraire(self):
        " fonction qui construit un itinéraire sous forme de liste de dictionnaires dont les clés sont le départ, l'arrivée, hotel, le retour, les activitées et comme valeurs les horaires associées"
        it = []
        n = self.date_retour - self.date_aller
         #Si le reste de la division n'est pas nul on rajoute le reste des activités sur le premier jour de voyage
        #Pour le jour 1
        " il a le droit de faire une activité: - Si le train arrive avant 16h et si son train de retour part après 16h"
        jour1 = {
            "jour1": {
                "train_aller": f"Départ de {self.ville_depart} à {self.train_aller[0]}, arrivée à {self.train_aller[1]} à {self.ville_arrivee}",
                "hotel": f"Check-in à {self.hotel}",}}
        it.append(jour1)
        
        
        nbr_activite_par_jour = (n-1)//len(self.activites_selectionnees)
        reste = (n-1)%len(self.activites_selectionnees)
        index_activite = 0
        
        "Pour les jours entre l'arrivée et le retour"
        for i in range (n-1):
            jour_cle = f"jour{i+2}"
            jour = {}
            for j in range(nbr_activite_par_jour):
                if index_activite < len(self.activites_selectionnes):
                    jour[f"activite{j+1}"] = self.activites_selectionnees[index_activite]
                    index_activite += 1
        if reste != 0:
            m = 1
            while index_activite < len(self.activites_selectionnees):
                jour[f"activite{m+3}"] = self.activites_selectionnees[index_activite]
                index_activite += 1
                m += 1
                    
            it.append({jour_cle: jour})   
                
        dernierjour = {
            f"jour{n}": {
                "train_retour": f"Départ de {self.ville_arrivee} à {self.train_retour[0]}, arrivée à {self.train_retour[1]} à {self.ville_depart}"}}
        it.append(dernierjour)
        
    def calculer_distance(self, p1, p2):
        if not p1 or not p2:
            return 0

        R = 6371  # rayon de la Terre en km

        lat1, lat2 = math.radians(p1[0]), math.radians(p2[0])
        diff_lat  = math.radians(p2[0] - p1[0])
        diff_lon  = math.radians(p2[1] - p1[1])

        a = (math.sin(diff_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2)* math.sin(diff_lon / 2) ** 2)

        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            
        
            
        
        
            