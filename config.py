import customtkinter as ctk

ctk.set_appearance_mode("light")

API_KEY = "bea16a42-8800-43ba-8725-673b558b99ec"

STATIONS = {
    "Paris":       "stop_area:SNCF:87686006",
    "Lyon":        "stop_area:SNCF:87723197",
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

THEME = {
    "couleurs": {
        "primaire":      "#1D3557",
        "secondaire":    "#2D4A6B",
        "accent":        "#E63946",
        "accent_hover":  "#C1121F",
        "succes":        "#2EC4B6",
        "succes_hover":  "#20998d",
        "fond_clair":    "#f8f9fa",
        "texte_fonce":   "#1D3557",
        "texte_clair":   "#ffffff",
        "texte_gris":    "#7f8c8d",
        "avertissement": "#e67e22"
    },
    "polices": {
        "h1":             ("Arial", 28, "bold"),
        "h2":             ("Arial", 24, "bold"),
        "h3":             ("Arial", 16, "bold"),
        "corps":          ("Arial", 14),
        "corps_gras":     ("Arial", 14, "bold"),
        "petit":          ("Arial", 12),
        "petit_italique": ("Arial", 11, "italic"),
        "mini_gras":      ("Arial", 10, "bold")
    }
}

CATEGORIES_ACTIVITES = {
    "Culture (Musées...)": {"tourism": ["museum", "artwork", "gallery"]},
    "Monuments":           {"tourism": ["attraction", "viewpoint", "monument"]},
    "Parcs & Loisirs":     {"leisure": ["park", "garden", "theme_park"]},
    "Gastronomie":         {"amenity": ["restaurant", "cafe"]}
}
