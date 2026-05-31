#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""Created on Thu Apr 23 08:10:31 2026

@author: lvernayfrecon
"""
import requests

API_KEY = "bea16a42-8800-43ba-8725-673b558b99ec"

STATIONS = {
    "Paris":       "stop_area:SNCF:87686006",
    "Marseille":   "stop_area:SNCF:87751008",
    "Nice":        "stop_area:SNCF:87756056",
    "Bordeaux":    "stop_area:SNCF:87581009",
    "Strasbourg":  "stop_area:SNCF:87212027",
    "Lille":       "stop_area:SNCF:87286005",
    "Nantes":      "stop_area:SNCF:87481002",
    "Toulouse":    "stop_area:SNCF:87611004",
    "Montpellier": "stop_area:SNCF:87773002",
    "Rennes":      "stop_area:SNCF:87471003",
    "Avignon":     "stop_area:SNCF:87318964",
    "Grenoble":    "stop_area:SNCF:87747006",
    "Angers":      "stop_area:SNCF:87484006",
    "Perpignan":   "stop_area:SNCF:87784009",
    
}

class Train:
        
    def chercher_trajets(self,origine,destination,date,heure):
        """renvoie une liste contenant 5 trajets possibles avec le lieu de départ, d'arrivée, la durée et le type de train.
        Si il n'existe aucun train, il renvoie None
        Formatage date/heure : AAAAMMJJTHHMMSS"""
        
        dt_str = f"{date.replace('-', '')}T{heure.replace(':', '')}00"
        
        url = ("https://api.sncf.com/v1/coverage/sncf/journeys"
            f"?from={STATIONS[origine]}"
            f"&to={STATIONS[destination]}"
            f"&datetime={dt_str}"
            "&count=5")
        
        reponse = requests.get(url, auth=(API_KEY,""),timeout=10)
        reponse.raise_for_status()
        donnees = reponse.json
        trajets_bruts = donnees.get("journeys",[])
        
        liste_trajets = []
        for trajet in trajets_bruts:
            
            if trajet["nb_transfers"] == 0:
                est_direct = True
            else:
                est_direct = False
            
            info_transfert = ""
            
            if not est_direct:
                i = 0
                sections = trajet.get("sections", [])
                while sections[i].get("type") != "public_transport":
                    i += 1
                    
                arret = sections[i].get("to", {})
                info_transfert = arret["name"]
                
            liste_trajets.append({
            "dep": self._formater_heure(trajet.get("departure_date_time", "")),
            "arr": self._formater_heure(trajet.get("arrival_date_time", "")),
            "duree": self._formater_duree(trajet.get("duration", 0)),
            "type": trajet.get("sections", [{}])[0].get("display_informations", {}).get("commercial_mode", "TRAIN"),
            "direct": est_direct,
            "transfert": info_transfert})
            
        return liste_trajets
                
                
            
    def formater_heure(self, chaine):
        """convertit l'heure donnée par l'API en heure xh ymin"""
        if len(chaine) >= 13:
            return f"{chaine[9:11]}:{chaine[11:13]}"
        else:
            return "--:--"

    def formater_duree(self, secondes):
        """convertit la durée donnée par l'API en heure ah bmin"""
        h, m = divmod(secondes // 60, 60)
        return f"{h}h{m:02d}"    