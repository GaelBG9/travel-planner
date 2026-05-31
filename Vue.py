import osmnx as ox
from config import CATEGORIES_ACTIVITES


class ModelePointsInteret:

    def chercher_hotels(self, ciudad):
        gdf = ox.features_from_place(f"{ciudad}, France", tags={"tourism": "hotel"})
        hoteles = []
        lista_hoteles = list(gdf.head(20).iterrows())

        for i in range(len(lista_hoteles)):
            numero_linea, lugar = lista_hoteles[i]
            nombre = lugar.get("name")
            if isinstance(nombre, str):
                hoteles.append({
                    "nom": nombre,
                    "lat": lugar.geometry.centroid.y,
                    "lon": lugar.geometry.centroid.x
                })
        return hoteles

    def chercher_activites(self, ciudad, categorias_lista):
        actividades = []
        for categoria in categorias_lista:
            nombre_categoria = CATEGORIES_ACTIVITES.get(categoria)
            gdf = ox.features_from_place(f"{ciudad}, France", tags=nombre_categoria)
            for linea, columna in gdf.head(8).iterrows():
                nombre = columna.get("name")
                if isinstance(nombre, str):
                    actividades.append({
                        "nom": nombre,
                        "lat": columna.geometry.centroid.y,
                        "lon": columna.geometry.centroid.x,
                        "cat": categoria
                    })
        return actividades

    def obtenir_coordonnees_ville(self, ciudad):
        # Récupère les coordonnées GPS du centre de la ville
        ciudad_gdf = ox.geocode_to_gdf(f"{ciudad}, France")
        lat = ciudad_gdf.iloc[0].geometry.centroid.y
        lon = ciudad_gdf.iloc[0].geometry.centroid.x
        return lat, lon

        frame_cats = ctk.CTkFrame(self.container, fg_color="transparent")
        frame_cats.pack()
        for cat in CATEGORIES_ACTIVITES.keys():
            var = ctk.BooleanVar()
            ctk.CTkCheckBox(frame_cats, text=cat, variable=var).pack(side="left", padx=10)
            self.cat_vars[cat] = var

        ctk.CTkButton(self.container, text="Rechercher", height=45, command=self.valider_recherche).pack(pady=30)
