#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 08:08:03 2026

@author: radelgadoca
"""
import osmnx as ox

CATEGORIES_ACTIVITES = {
    "Culture (Musées...)": {"tourism": ["museum", "artwork", "gallery"]},
    "Monuments": {"tourism": ["attraction", "viewpoint", "monument"]},
        "Parcs & Loisirs": {"leisure": ["park", "garden", "theme_park"]},
    "Gastronomie": {"amenity": ["restaurant", "cafe"]}
}

class Points_Interets:
    """
    Fait la recherche de points d'interets possibles dans une ville donné
    """
    def __init__(self, liste_activites):
        self.liste_activites = liste_activites
        
    def chercher_hotels(self, ville):
        """
        Cherche les hôtels dans une ville et renvoie une liste des possibilités.
        """
        gdf = ox.features_from_place(f"{ville}, France", tags={"tourism": "hotel"}) 
        hotels = []
        for ligne, colonne in gdf.head(20).iterrows():
            nom = colonne.get("name")
            if isinstance (nom, str): 
                hotels = [{'Nom hôtel' : nom, 'Latitude' : colonne.geometry.centroid.x , 'Longitude' : colonne.geometry.centroid.y }]
        return hotels
        
         
    def chercher_activites(self, ville, categories_liste):
        """
        Renvoie une liste d'activites precedemment filtre selon les categories choisies par l'utilisateur
        """
        activites = []
        for categorie in categories_liste:
            tags = CATEGORIES_ACTIVITES.get(categorie)
            gdf = ox.features_from_place(f"{ville}, France", tags=tags)
            for ligne, colonne in gdf.head(8).iterrows():
                nom = colonne.get("name")
                if isinstance(nom, str):
                    activites.append({"Nom activité": nom,"lat": colonne.geometry.centroid.y, "lon": colonne.geometry.centroid.x, "cat": categorie })
        return activites

gdf = ox.features_from_place(f"Paris, France", tags={"tourism": "hotel"})
print(gdf)
            
        
        
    
        