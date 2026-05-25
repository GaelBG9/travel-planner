class ModelePointsInteret:

    def chercher_hotels(self, ville):
        try:
            gdf = ox.features_from_place(f"{ville}, France", tags={"tourism": "hotel"}) #ce sont les hotels de la ville 
            hotels = []
            # On convertit le tableau OSMnx en liste Python classique
            liste_hotels = list(gdf.head(20).iterrows())

# itterrows prmet d"extraire les données sous forme de de tuple avec le numéro de ligne et le contenu de la ligne en l"occurence les infos de l"hotel 
            for i in range(len(liste_hotels)):
                numero_ligne, lieu = liste_hotels[i]
                nom = lieu.get("name")
                if nom is not None:
                    hotels.append({
                        "nom": nom,
                        "lat": lieu.geometry.centroid.y,
                        # lieu est un instance de classe on récupère geometry qui est sont coordonnées 
                        #POLYGON((4.831 45.764, 4.832 45.764, 4.832 45.765, 4.831 45.765, ...)) par exemple
                        "lon": lieu.geometry.centroid.x})
            return hotels
        except:
            return []

    def chercher_activites(self, ville, categories_list):
        activites = []
        for cat_name in categories_list:
            nom_categorie = CATEGORIES_ACTIVITES.get(cat_name)
            try:
                gdf = ox.features_from_place(f"{ville}, France", tags=nom_categorie)
                for ligne, colonne in gdf.head(8).iterrows():
                    nom = colonne.get("name")
                    if isinstance(nom, str):
                        activites.append({
                            "nom": nom,
                            "lat": colonne.geometry.centroid.y,
                            "lon": colonne.geometry.centroid.x,
                            "cat": cat_name
                        })
                        #la même que expliquait juste avant mais avec les activités et pas les hotels 
            except:
                continue
        return activites

    def obtenir_coordonnees_ville(self, ville):
        # Nécessaire pour centrer la carte sur la ville de destination
        try:
            ville = ox.geocode_to_gdf(f"{ville}, France") 
            #iloc permet dans l"instance de classe de ville de GeodataFrame d"avoir la première ligne qui est la pricipale car si on prend les lignes après ça peut être des quartiers ou arrondissement 
            lat = ville.iloc[0].geometry.centroid.y #permet de mettre en x la ville au centre de la map
            lon = ville.iloc[0].geometry.centroid.x
            return lat, lon
        except:
            return None, None
            
        
        
    
        