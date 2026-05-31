import osmnx as ox
from config import CATEGORIES_ACTIVITES

class ModelePointsInteret:

    def chercher_hotels(self, ville):
        '''
        Recherche les hôtels d'une ville à travers OpenStreetMap.

        Parameters
        ----------
        ville : string
            Nom de la ville à rechercher

        Returns
        -------
        hotels : liste de dictionnaires
            Liste d'hôtels contenant des dictionnaires où chacun a:
                - "nom" (str) : nom de l'hôtel.
                - "lat" (float) : latitude du centroïde.
                - "lon" (float) : longitude du centroïde.
        '''
        gdf = ox.features_from_place(f"{ville}, France", tags={"tourism": "hotel"})
        hotels = []
        liste_hotels = list(gdf.head(20).iterrows())

        for i in range(len(liste_hotels)):
            numero_ligne, lieu = liste_hotels[i]
            nom = lieu.get("name")
            if isinstance(nom, str):
                hotels.append({"nom": nom, "lat": lieu.geometry.centroid.y, "lon": lieu.geometry.centroid.x})
        return hotels

    def chercher_activites(self, ville, categories_liste):
        '''
        Recherche les activités d'une ville selon une liste de catégories.

        Parameters
        ----------
        ville : string
            Nom de la ville à rechercher.
        categories_liste : liste de string
            Liste de catégories d'activités correspondant aux clés de CATEGORIES_ACTIVITES.

        Returns
        -------
        activites : liste de dictionnaires
            Liste d'activités, chaque dictionnaire contient :
                - "nom" (str)   : nom du lieu.
                - "lat" (float) : latitude du centroïde.
                - "lon" (float) : longitude du centroïde.
                - "cat" (str)   : catégorie de l'activité.

        '''
        activites = []
        for categorie in categories_liste:
            nom_categorie = CATEGORIES_ACTIVITES.get(categorie)
            gdf = ox.features_from_place(f"{ville}, France", tags=nom_categorie)
            for ligne, colonne in gdf.head(8).iterrows():
                nom = colonne.get("name")
                if isinstance(nom, str):
                    activites.append({"nom": nom, "lat": colonne.geometry.centroid.y, "lon": colonne.geometry.centroid.x,"cat": categorie})
        return activites

    def obtenir_coordonnees_ville(self, ville):
        '''
        Retourne les coordonnées géographiques du centre d'une ville.

        Parameters
        ----------
        ville : string
            Nom de la ville à géocoder.

        Returns
        -------
        tuple[float, float]: Latitude et longitude du centroïde de la ville

        ''' 
        ville = ox.geocode_to_gdf(f"{ville}, France") 
        lat = ville.iloc[0].geometry.centroid.y
        lon = ville.iloc[0].geometry.centroid.x
        return lat, lon   
    
        
    
        