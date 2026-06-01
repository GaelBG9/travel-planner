#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
"""Created on Thu Apr 23 08:10:31 2026

@author: lvernayfrecon
"""

from urllib.parse import quote
import requests


API_KEY = "bea16a42-8800-43ba-8725-673b558b99ec"

class Train:
     """
    Classe gérant les interactions avec l'API SNCF pour la recherche d'itinéraires ferroviaires.
    Elle ne comporte pas de init vu qu'elle ne garde aucune information.
    """   
     def chercher_trajets(self, origine, destination, date, heure):
         """
         Interroge l'API SNCF pour récupérer une liste de 5 trajets maximum entre deux gares.
         Elle filtre les résultats pour identifier les correspondances et extraire les horaires.
         Retourne une liste de dictionnaires contenant les données nettoyées du trajet.
         """
         id_dep =  self.trouver_code_gare(origine)
         id_arr =  self.trouver_code_gare(destination)

         if not id_dep or not id_arr:
             return []

         chaine_dt = date.replace("-", "") + "T" + heure.replace(":", "") + "00"
         url = f"https://api.sncf.com/v1/coverage/sncf/journeys?from={quote(id_dep)}&to={quote(id_arr)}&datetime={chaine_dt}&count=5"

         reponse = requests.get(url, auth=(API_KEY, ""), timeout=10)
         reponse.raise_for_status()
         donnees = reponse.json()
         trajets_bruts = donnees.get("journeys", [])

         resultats = []
         for t in trajets_bruts:
             sections_transport = []
             for s in t.get("sections", []):
                 if s.get("type") == "public_transport":
                     sections_transport.append(s)

             if len(sections_transport) == 0:
                 continue

             est_direct = len(sections_transport) == 1
             info_correspondance = ""
             if not est_direct:
                 arret = sections_transport[0].get("to", {})
                 info_correspondance = arret.get("display_informations", {}).get("label") or arret.get("name", "Correspondance")
                 info_correspondance = info_correspondance.replace("Gare de ", "")

             resultats.append({
                 "dep":       self.formater_heure(t.get("departure_date_time", "")),
                 "arr":       self.formater_heure(t.get("arrival_date_time", "")),
                 "duree":     self.formater_duree(t.get("duration", 0)),
                 "duree_sec": t.get("duration", 0),
                 "type":      sections_transport[0].get("display_informations", {}).get("commercial_mode", "TRAIN"),
                 "direct":    est_direct,
                 "transfert": info_correspondance
             })
         return resultats
                
                
            
     def formater_heure(self, chaine):
        """
        Extrait et formate l'heure au format 'HH:MM' à partir de la chaîne temporelle
        brute renvoyée par l'API SNCF (par exemple : '20261025T083000' devient '08:30').
        """
        if len(chaine) >= 13:
            return f"{chaine[9:11]}:{chaine[11:13]}"
        else:
            return "--:--"

     def formater_duree(self, secondes):
        """convertit la durée donnée par l'API en heure ah bmin"""
        h, m = divmod(secondes // 60, 60)
        return f"{h}h{m:02d}"    

     def trouver_code_gare(self, nombre_ciudad):
        """
        Effectue une requête à l'API SNCF pour trouver l'identifiant unique 
        (de type zone administrative) correspondant au nom d'une ville saisie par l'utilisateur.
        """
        url = f"https://api.sncf.com/v1/coverage/sncf/places?q={quote(nombre_ciudad)}&type[]=stop_area"
        r = requests.get(url, auth=(API_KEY, ""))
        if r.status_code == 200:
            datos = r.json()
            if "places" in datos and len(datos["places"]) > 0:
                return datos["places"][0]["id"]
        return None

    def trouver_index_rapide(self, liste_trains):
        """
        Parcourt une liste de dictionnaires représentant des trajets de train 
        et retourne l'index de la liste correspondant au trajet ayant la durée la  plus courte.
        """
        if len(liste_trains) == 0:
            return -1
        idx_rapide = 0
        for i in range(len(liste_trains)):
            if liste_trains[i]["duree_sec"] < liste_trains[idx_rapide]["duree_sec"]:
                idx_rapide = i
        return idx_rapide
