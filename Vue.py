import customtkinter as ctk
import tkintermapview
from datetime import datetime
from PIL import Image
import os
import random

from config import THEME, STATIONS, CATEGORIES_ACTIVITES

ETAPES = ["Recherche", "Trains", "Hôtel", "Activités", "Planning", "Carnet"]


class Vue(ctk.CTk):
    """
    Interface utilisateur graphique principale, construite avec CustomTkinter.
    La Vue ne contient aucune logique métier : elle délègue toutes les actions
    au Contrôleur via self.ctrl.<methode>().
    """

    def __init__(self, ctrl):
        """Initialise la fenêtre principale et crée la barre d'étapes et le conteneur de contenu."""
        super().__init__()
        self.ctrl = ctrl
        self.title("Voyage Voyage")
        self.geometry("1200x850")

        # self.c et self.p sont des raccourcis vers les couleurs et polices du thème
        # pour éviter d'écrire THEME["couleurs"]["primaire"] à chaque fois
        self.c = THEME["couleurs"]
        self.p = THEME["polices"]

        self.barre_etapes = ctk.CTkFrame(self, height=65, fg_color=self.c["primaire"], corner_radius=0)
        self.barre_etapes.pack(fill="x")

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=20, pady=(10, 20))

    def afficher_barre(self, etape_active):
        """
        Génère visuellement la barre de progression en haut de l'écran selon l'étape actuelle.
        Les étapes passées apparaissent en vert avec une coche, l'étape active en rouge,
        les étapes futures en gris.
        """
        for widget in self.barre_etapes.winfo_children():
            widget.destroy()

        for i in range(len(ETAPES)):
            nom_etape = ETAPES[i]
            col = ctk.CTkFrame(self.barre_etapes, fg_color="transparent")
            col.pack(side="left", expand=True)

            if i < etape_active:
                cercle = ctk.CTkButton(col, text="✓", width=28, height=28, corner_radius=14, font=self.p["mini_gras"], fg_color=self.c["succes"], hover_color=self.c["succes"])
                couleur_label = self.c["succes"]
            elif i == etape_active:
                cercle = ctk.CTkButton(col, text=str(i + 1), width=28, height=28, corner_radius=14, font=self.p["mini_gras"], fg_color=self.c["accent"], hover_color=self.c["accent_hover"])
                couleur_label = self.c["fond_clair"]
            else:
                cercle = ctk.CTkButton(col, text=str(i + 1), width=28, height=28, corner_radius=14, font=self.p["petit"], fg_color=self.c["fond_clair"], hover_color=self.c["fond_clair"], text_color=self.c["texte_gris"])
                couleur_label = self.c["texte_gris"]

            cercle.pack(pady=(8, 2))
            ctk.CTkLabel(col, text=nom_etape, font=self.p["petit"], text_color=couleur_label).pack()

            if i < len(ETAPES) - 1:
                # Le trait est vert si l'étape est passée, gris sinon
                couleur_trait = self.c["succes"] if i < etape_active else self.c["secondaire"]
                ctk.CTkFrame(self.barre_etapes, height=2, width=30, fg_color=couleur_trait, corner_radius=0).pack(side="left", pady=(0, 22))

    def vider_ecran(self):
        """Supprime tous les widgets du conteneur principal avant d'afficher une nouvelle page."""
        for widget in self.container.winfo_children():
            widget.destroy()

    def afficher_chargement(self, message):
        """Affiche un écran d'attente avec un message pendant le traitement des requêtes réseau."""
        self.vider_ecran()
        ctk.CTkLabel(self.container, text=message, font=self.p["h2"], text_color=self.c["texte_fonce"]).pack(expand=True)

    def creer_selecteur_date(self, parent, row, label):
        """
        Instancie trois menus déroulants (jour, mois, année) dans une ligne de grille.

        Args:
            parent: le widget parent dans lequel placer le sélecteur
            row (int): le numéro de ligne dans la grille du parent
            label (str): le texte affiché à gauche du sélecteur

        Returns:
            tuple: (v_j, v_m, v_a) — trois StringVar tkinter contenant les valeurs sélectionnées
        """
        aujourd_hui = datetime.today()

        jours = []
        for j in range(1, 32):
            jours.append(f"{j:02d}")

        mois = []
        for m in range(1, 13):
            mois.append(f"{m:02d}")

        annees = []
        for a in range(aujourd_hui.year, aujourd_hui.year + 2):
            annees.append(str(a))

        ctk.CTkLabel(parent, text=label, font=self.p["corps_gras"], text_color=self.c["texte_fonce"]).grid(row=row, column=0, padx=20, pady=15, sticky="e")
        frame_date = ctk.CTkFrame(parent, fg_color="transparent")
        frame_date.grid(row=row, column=1, pady=15, sticky="w")

        # StringVar : variable tkinter qui stocke une valeur texte et se met à jour automatiquement
        # quand l'utilisateur change la sélection dans le menu déroulant
        v_j = ctk.StringVar(value=f"{aujourd_hui.day:02d}")
        v_m = ctk.StringVar(value=f"{aujourd_hui.month:02d}")
        v_a = ctk.StringVar(value=str(aujourd_hui.year))

        ctk.CTkOptionMenu(frame_date, variable=v_j, values=jours, width=65, fg_color=self.c["primaire"]).pack(side="left", padx=2)
        ctk.CTkLabel(frame_date, text="/", text_color=self.c["texte_fonce"]).pack(side="left")
        ctk.CTkOptionMenu(frame_date, variable=v_m, values=mois, width=65, fg_color=self.c["primaire"]).pack(side="left", padx=2)
        ctk.CTkLabel(frame_date, text="/", text_color=self.c["texte_fonce"]).pack(side="left")
        ctk.CTkOptionMenu(frame_date, variable=v_a, values=annees, width=85, fg_color=self.c["primaire"]).pack(side="left", padx=2)
        return v_j, v_m, v_a

    def lire_date(self, var_j, var_m, var_a):
        """
        Recombine les trois StringVar en une chaîne au format ISO AAAA-MM-JJ.

        Returns:
            str: la date formatée, ex: "2026-06-15"
        """
        return f"{var_a.get()}-{var_m.get()}-{var_j.get()}"

    def afficher_recherche(self):
        """
        Affiche le formulaire initial de configuration du voyage :
        villes de départ/arrivée, dates, heures et catégories d'activités.
        Affiche aussi 4 cartes de villes tirées au hasard en bas de page.
        """
        self.afficher_barre(0)
        self.vider_ecran()

        ctk.CTkLabel(self.container, text="Configuration du Voyage", font=self.p["h1"], text_color=self.c["texte_fonce"]).pack(pady=(20, 10))

        f = ctk.CTkFrame(self.container, fg_color=self.c["fond_clair"], corner_radius=15, border_width=1)
        f.pack(pady=10, padx=50, fill="x")
        f.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(f, text="Départ :", font=self.p["corps_gras"], text_color=self.c["texte_fonce"]).grid(row=0, column=0, padx=20, pady=25, sticky="e")
        self.ent_dep = ctk.CTkEntry(f, placeholder_text="Ex: Paris", width=200)
        self.ent_dep.insert(0, "Paris")
        self.ent_dep.grid(row=0, column=1, pady=25, sticky="w")

        ctk.CTkLabel(f, text="Arrivée :", font=self.p["corps_gras"], text_color=self.c["texte_fonce"]).grid(row=0, column=2, padx=20, pady=25, sticky="e")
        self.ent_arr = ctk.CTkEntry(f, placeholder_text="Ex: Lyon", width=200)
        self.ent_arr.insert(0, "Lyon")
        self.ent_arr.grid(row=0, column=3, pady=25, sticky="w")

        self.var_j_all, self.var_m_all, self.var_a_all = self.creer_selecteur_date(f, row=1, label="Date Aller :")
        ctk.CTkLabel(f, text="Heure aller :", font=self.p["corps_gras"], text_color=self.c["texte_fonce"]).grid(row=1, column=2, padx=20, sticky="e")
        self.ent_h_all = ctk.CTkEntry(f, width=100)
        self.ent_h_all.insert(0, "08:00")
        self.ent_h_all.grid(row=1, column=3, sticky="w")

        self.var_j_ret, self.var_m_ret, self.var_a_ret = self.creer_selecteur_date(f, row=2, label="Date Retour :")
        ctk.CTkLabel(f, text="Heure retour :", font=self.p["corps_gras"], text_color=self.c["texte_fonce"]).grid(row=2, column=2, padx=20, sticky="e")
        self.ent_h_ret = ctk.CTkEntry(f, width=100)
        self.ent_h_ret.insert(0, "16:00")
        self.ent_h_ret.grid(row=2, column=3, sticky="w")

        # self.cat_vars stocke une BooleanVar par catégorie pour savoir lesquelles sont cochées
        self.cat_vars = {}
        frame_cats = ctk.CTkFrame(self.container, fg_color="transparent")
        frame_cats.pack(pady=15)

        noms_categories = list(CATEGORIES_ACTIVITES.keys())
        for i in range(len(noms_categories)):
            cat = noms_categories[i]
            var = ctk.BooleanVar(value=True)
            ctk.CTkCheckBox(frame_cats, text=cat, variable=var, fg_color=self.c["accent"], hover_color=self.c["accent_hover"], text_color=self.c["texte_fonce"], font=self.p["corps"]).pack(side="left", padx=15)
            self.cat_vars[cat] = var

        ctk.CTkButton(self.container, text="Rechercher Itinéraires", height=45, width=250, font=self.p["h3"], fg_color=self.c["accent"], hover_color=self.c["accent_hover"], text_color=self.c["texte_clair"], command=self.valider_recherche).pack(pady=20)

        frame_img = ctk.CTkFrame(self.container, fg_color="transparent")
        frame_img.pack(fill="x", expand=True, padx=20)

        # On tire 4 villes au hasard parmi toutes les villes du dictionnaire STATIONS
        toutes_les_villes = list(STATIONS.keys())
        villes_finales = random.sample(toutes_les_villes, 4)

        for ville in villes_finales:
            card_img = ctk.CTkFrame(frame_img, height=150, fg_color=self.c["primaire"], corner_radius=10)
            card_img.pack(side="left", expand=True, fill="both", padx=10)
            # pack_propagate(False) empêche la carte de rétrécir selon la taille de son contenu
            card_img.pack_propagate(False)

            if os.path.exists(ville + ".jpg"):
                photo = Image.open(ville + ".jpg")
                photo = photo.resize((280, 150))
                photo_ctk = ctk.CTkImage(light_image=photo, size=(280, 150))
                lbl_photo = ctk.CTkLabel(card_img, image=photo_ctk, text="")
                lbl_photo.place(relx=0, rely=0, relwidth=1, relheight=1)

            bandeau = ctk.CTkFrame(card_img, fg_color=self.c["primaire"], corner_radius=0, height=40)
            bandeau.place(relx=0, rely=1.0, anchor="sw", relwidth=1)
            ctk.CTkLabel(bandeau, text=f"📍 {ville}", font=self.p["corps_gras"], text_color=self.c["texte_clair"]).place(relx=0.5, rely=0.5, anchor="center")

            def remplir_arrivee(v=ville):
                self.ent_arr.delete(0, "end")
                self.ent_arr.insert(0, v)

            # Le lambda capture la valeur de ville au moment de la création du bouton
            # pour que chaque carte se souvienne de sa propre ville au clic
            card_img.bind("<Button-1>", lambda e, v=ville: remplir_arrivee(v))
            for enfant in card_img.winfo_children():
                enfant.bind("<Button-1>", lambda e, v=ville: remplir_arrivee(v))

    def valider_recherche(self):
        """
        Vérifie la cohérence des dates saisies puis délègue la recherche au Contrôleur.
        Affiche un message d'erreur si la date de retour est avant ou égale à la date d'aller.
        """
        d_all = self.lire_date(self.var_j_all, self.var_m_all, self.var_a_all)
        d_ret = self.lire_date(self.var_j_ret, self.var_m_ret, self.var_a_ret)

        dt_all = datetime.strptime(d_all, "%Y-%m-%d")
        dt_ret = datetime.strptime(d_ret, "%Y-%m-%d")

        if dt_ret <= dt_all:
            ctk.CTkLabel(self.container, text="⚠️ La date de retour doit être après la date d'aller !", text_color=self.c["accent"]).pack()
            return

        cats = []
        for cat in self.cat_vars:
            if self.cat_vars[cat].get() == True:
                cats.append(cat)

        self.ctrl.lancer_recherche_trains(
            self.ent_dep.get(), self.ent_arr.get(),
            d_all, self.ent_h_all.get(),
            d_ret, self.ent_h_ret.get(),
            cats, dt_all, dt_ret
        )

    def afficher_selection_trains(self, trains_aller, trains_retour, idx_rapide_aller, idx_rapide_retour):
        """
        Affiche les options de trains disponibles pour l'aller et le retour.

        Args:
            trains_aller (list): liste des trains pour l'aller
            trains_retour (list): liste des trains pour le retour
            idx_rapide_aller (int): index du train le plus rapide à l'aller
            idx_rapide_retour (int): index du train le plus rapide au retour
        """
        self.afficher_barre(1)
        self.vider_ecran()
        # train_buttons stocke les boutons par direction pour pouvoir les mettre à jour au clic
        self.train_buttons = {"ALLER": [], "RETOUR": []}

        ctk.CTkLabel(self.container, text="Choisissez vos horaires de train", font=self.p["h2"], text_color=self.c["texte_fonce"]).pack(pady=(10, 20))
        main_f = ctk.CTkFrame(self.container, fg_color="transparent")
        main_f.pack(fill="both", expand=True)

        self.afficher_colonne_trains(main_f, trains_aller, "ALLER", "left", idx_rapide_aller)
        self.afficher_colonne_trains(main_f, trains_retour, "RETOUR", "right", idx_rapide_retour)

        ctk.CTkButton(self.container, text="Valider les Trains ➔", height=50, fg_color=self.c["accent"], hover_color=self.c["accent_hover"], font=self.p["h3"], text_color=self.c["texte_clair"], command=self.ctrl.lancer_recherche_hotels).pack(pady=20)

    def afficher_colonne_trains(self, parent, liste_trains, titre, cote, idx_rapide):
        """
        Génère une colonne de cartes trains pour un trajet donné (aller ou retour).

        Args:
            parent: widget parent contenant la colonne
            liste_trains (list): liste des trains à afficher
            titre (str): "ALLER" ou "RETOUR"
            cote (str): "left" ou "right" pour le positionnement
            idx_rapide (int): index du train le plus rapide, reçu du Contrôleur
        """
        if len(liste_trains) == 0:
            return

        col = ctk.CTkFrame(parent, fg_color="transparent")
        col.pack(side=cote, fill="both", expand=True, padx=15)
        ctk.CTkLabel(col, text=titre, font=self.p["h3"], text_color=self.c["texte_fonce"]).pack(pady=5)

        scroll = ctk.CTkScrollableFrame(col, fg_color=self.c["fond_clair"], corner_radius=15)
        scroll.pack(fill="both", expand=True)

        for i in range(len(liste_trains)):
            t = liste_trains[i]
            card = ctk.CTkFrame(scroll, fg_color=self.c["texte_clair"], corner_radius=10)
            card.pack(pady=6, padx=5, fill="x")

            haut = ctk.CTkFrame(card, fg_color="transparent")
            haut.pack(fill="x", padx=10, pady=5)
            if i == idx_rapide:
                ctk.CTkLabel(haut, text="⚡ RAPIDE", font=self.p["mini_gras"], text_color=self.c["succes"]).pack(side="left", padx=2)

            if t["direct"] == True:
                label_direct = "DIRECT"
                couleur_direct = self.c["texte_fonce"]
            else:
                label_direct = f"VIA {t['transfert'].upper()}"
                couleur_direct = self.c["avertissement"]

            ctk.CTkLabel(haut, text=label_direct, font=self.p["mini_gras"], text_color=couleur_direct).pack(side="left", padx=5)

            milieu = ctk.CTkFrame(card, fg_color="transparent")
            milieu.pack(fill="x", padx=10)
            ctk.CTkLabel(milieu, text=f"{t['dep']} ➔ {t['arr']}", font=self.p["h2"], text_color=self.c["texte_fonce"]).pack(side="left")
            ctk.CTkLabel(milieu, text=t["duree"], font=self.p["corps_gras"], text_color=self.c["texte_gris"]).pack(side="right")

            bas = ctk.CTkFrame(card, fg_color="transparent")
            bas.pack(fill="x", padx=10, pady=10)
            ctk.CTkLabel(bas, text="📶 🔌 ☕", font=self.p["corps"], text_color=self.c["texte_gris"]).pack(side="left")

            btn = ctk.CTkButton(bas, text="Choisir", width=90, height=32, corner_radius=6, fg_color=self.c["accent"], hover_color=self.c["accent_hover"], text_color=self.c["texte_clair"], command=lambda x=t, k=titre: self.ctrl.choisir_train(x, k))
            btn.pack(side="right")
            self.train_buttons[titre].append((btn, t))

    def mettre_a_jour_boutons_train(self, train_choisi, cle):
        """
        Actualise l'état visuel des boutons train après qu'un train a été sélectionné.
        Le bouton du train choisi passe en vert, les autres repassent en rouge.

        Args:
            train_choisi (dict): le train sélectionné par l'utilisateur
            cle (str): "ALLER" ou "RETOUR"
        """
        for i in range(len(self.train_buttons[cle])):
            btn = self.train_buttons[cle][i][0]
            data = self.train_buttons[cle][i][1]
            if data == train_choisi:
                btn.configure(fg_color=self.c["succes"], text="✓ OK")
            else:
                btn.configure(fg_color=self.c["accent"], text="Choisir")

    def afficher_selection_hotels(self, hotels):
        """
        Affiche la grille d'hôtels disponibles dans la ville de destination.

        Args:
            hotels (list[dict]): liste des hôtels avec leur nom et coordonnées GPS
        """
        self.afficher_barre(2)
        self.vider_ecran()
        ctk.CTkLabel(self.container, text="Choisissez votre Hébergement", font=self.p["h2"], text_color=self.c["texte_fonce"]).pack(pady=(10, 20))

        scroll = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10)
        scroll.grid_columnconfigure((0, 1, 2), weight=1)

        for i in range(len(hotels)):
            h = hotels[i]
            # row et col calculent la position dans la grille à 3 colonnes
            row = i // 3
            col = i % 3

            card = ctk.CTkFrame(scroll, corner_radius=10, fg_color=self.c["texte_clair"])
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            ctk.CTkLabel(card, text="🏨", font=("Arial", 30)).pack(pady=(15, 5))
            ctk.CTkLabel(card, text=h["nom"], font=self.p["corps_gras"], text_color=self.c["texte_fonce"], wraplength=200).pack(pady=5, padx=10)
            ctk.CTkButton(card, text="Réserver", fg_color=self.c["primaire"], hover_color=self.c["secondaire"], text_color=self.c["texte_clair"], command=lambda x=h: self.ctrl.choisir_hotel(x)).pack(pady=15, side="bottom")

    def afficher_selection_activites(self, activites, max_activites):
        """
        Présente les points d'intérêt disponibles avec un compteur de sélection.

        Args:
            activites (list[dict]): liste des activités disponibles
            max_activites (int): nombre maximum d'activités autorisées (3 par jour)
        """
        self.afficher_barre(3)
        self.vider_ecran()

        entete = ctk.CTkFrame(self.container, fg_color="transparent")
        entete.pack(fill="x", pady=10)
        ctk.CTkLabel(entete, text="Sélectionnez vos Activités", font=self.p["h2"], text_color=self.c["texte_fonce"]).pack(side="left")

        self.lbl_compteur = ctk.CTkLabel(entete, text=f"0 / {max_activites} (3 par jour)", font=self.p["h3"], text_color=self.c["accent"], fg_color=self.c["fond_clair"], corner_radius=8, padx=10)
        self.lbl_compteur.pack(side="right")

        scroll = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10)
        scroll.grid_columnconfigure((0, 1, 2), weight=1)

        # Liste qui accumule les activités cochées par l'utilisateur
        self._activites_cochees = []

        for i in range(len(activites)):
            a = activites[i]
            row = i // 3
            col = i % 3

            card = ctk.CTkFrame(scroll, fg_color=self.c["texte_clair"], corner_radius=10)
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            ctk.CTkLabel(card, text=a["cat"], font=self.p["mini_gras"], text_color=self.c["texte_gris"]).pack(anchor="w", padx=10, pady=(10, 0))
            ctk.CTkLabel(card, text=a["nom"], font=self.p["corps_gras"], text_color=self.c["texte_fonce"], wraplength=220, justify="left").pack(anchor="w", padx=10, pady=(2, 10))

            var_chk = ctk.BooleanVar(value=False)

            def basculer(act=a, var=var_chk):
                act_sel = self._activites_cochees
                if var.get() == True:
                    if len(act_sel) >= max_activites:
                        var.set(False)
                        self.lbl_compteur.configure(text="Limite atteinte !", text_color=self.c["texte_clair"], fg_color=self.c["accent"])
                        return
                    act_sel.append(act)
                else:
                    if act in act_sel:
                        act_sel.remove(act)
                self.lbl_compteur.configure(text=f"{len(act_sel)} / {max_activites} (3 par jour)", text_color=self.c["accent"], fg_color=self.c["fond_clair"])

            chk = ctk.CTkCheckBox(card, text="Ajouter", variable=var_chk, command=basculer, fg_color=self.c["succes"], hover_color=self.c["succes_hover"], text_color=self.c["texte_fonce"], font=self.p["corps"])
            chk.pack(anchor="e", padx=10, pady=10, side="bottom")

        ctk.CTkButton(self.container, text="Planifier mes journées ➔", height=45, font=self.p["h3"], fg_color=self.c["accent"], hover_color=self.c["accent_hover"], text_color=self.c["texte_clair"], command=lambda: self.ctrl.lancer_planification(self._activites_cochees)).pack(pady=20)

    def afficher_planification(self, planning):
        """
        Organise l'interface permettant de réorganiser les activités par journée.

        Args:
            planning (dict[int, list]): dictionnaire {index_jour: [activites]} fourni par le Contrôleur
        """
        self.afficher_barre(4)
        self.vider_ecran()
        ctk.CTkLabel(self.container, text="Planifier mes journées", font=self.p["h2"], text_color=self.c["texte_fonce"]).pack(pady=(20, 5))
        ctk.CTkLabel(self.container, text="Clique sur ⇄ pour sélectionner deux activités à échanger", font=self.p["corps"], text_color=self.c["texte_gris"]).pack(pady=(0, 15))

        self._planning_data = planning
        # None signifie qu'aucune activité n'est en attente d'échange
        self._activite_selectionnee = None

        self.scroll_planning = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        self.scroll_planning.pack(fill="both", expand=True, padx=20)

        self.afficher_jours()

        ctk.CTkButton(self.container, text="Générer le Carnet ➔", height=45, font=self.p["h3"], fg_color=self.c["accent"], hover_color=self.c["accent_hover"], text_color=self.c["texte_clair"], command=lambda: self.ctrl.lancer_generation_carnet(self._planning_data)).pack(pady=20)

    def afficher_jours(self):
        """
        Met à jour l'affichage des journées d'activités dans le gestionnaire de planning.
        Appelée à chaque échange pour rafraîchir l'interface.
        """
        for widget in self.scroll_planning.winfo_children():
            widget.destroy()

        jours_ordonnes = sorted(self._planning_data.keys())
        for jour in jours_ordonnes:
            acts = self._planning_data[jour]

            bloc = ctk.CTkFrame(self.scroll_planning, fg_color=self.c["texte_clair"], corner_radius=10)
            bloc.pack(fill="x", pady=8, padx=5)

            header = ctk.CTkFrame(bloc, fg_color=self.c["primaire"], corner_radius=8)
            header.pack(fill="x", padx=4, pady=4)
            ctk.CTkLabel(header, text=f"  Jour {jour + 1}  —  {len(acts)}/3 activités", font=self.p["corps_gras"], text_color=self.c["texte_clair"]).pack(side="left", padx=10, pady=6)

            for idx in range(len(acts)):
                act = acts[idx]
                est_selectionnee = (self._activite_selectionnee == (jour, idx))

                if est_selectionnee:
                    couleur_fond = self.c["fond_clair"]
                    couleur_txt = self.c["primaire"]
                    texte_btn = "✓ Sélectionné"
                    couleur_btn = self.c["succes"]
                else:
                    couleur_fond = "transparent"
                    couleur_txt = self.c["texte_fonce"]
                    texte_btn = "⇄ Échanger"
                    couleur_btn = self.c["accent"]

                ligne = ctk.CTkFrame(bloc, fg_color=couleur_fond, corner_radius=6)
                ligne.pack(fill="x", padx=8, pady=3)

                ctk.CTkLabel(ligne, text=f"{idx + 1}.", width=25, font=self.p["corps_gras"], text_color=self.c["texte_gris"]).pack(side="left", padx=(8, 0), pady=6)

                info = ctk.CTkFrame(ligne, fg_color="transparent")
                info.pack(side="left", fill="x", expand=True, padx=8)
                ctk.CTkLabel(info, text=act["nom"], font=self.p["corps_gras"], text_color=couleur_txt, anchor="w").pack(anchor="w")
                ctk.CTkLabel(info, text=act["cat"], font=self.p["petit"], text_color=self.c["texte_gris"], anchor="w").pack(anchor="w")

                ctk.CTkButton(ligne, text=texte_btn, width=120, height=28, font=self.p["corps"], fg_color=couleur_btn, text_color=self.c["texte_clair"], corner_radius=6, command=lambda j=jour, i=idx: self.echanger_activite(j, i)).pack(side="right", padx=8, pady=6)

    def echanger_activite(self, jour, idx):
        """
        Gère la sélection et la permutation de deux activités dans le planning.
        Premier clic : mémorise l'activité. Deuxième clic : effectue l'échange et notifie le Contrôleur.

        Args:
            jour (int): index du jour de l'activité cliquée
            idx (int): index de l'activité dans sa journée
        """
        if self._activite_selectionnee is None:
            self._activite_selectionnee = (jour, idx)
        else:
            j1 = self._activite_selectionnee[0]
            i1 = self._activite_selectionnee[1]
            j2 = jour
            i2 = idx

            if not (j1 == j2 and i1 == i2):
                act1 = self._planning_data[j1][i1]
                act2 = self._planning_data[j2][i2]
                self._planning_data[j1][i1] = act2
                self._planning_data[j2][i2] = act1
                self.ctrl.mettre_a_jour_planning(self._planning_data)

            self._activite_selectionnee = None
        self.afficher_jours()

    def afficher_final(self, itineraire, lat_ville, lon_ville, hotel, activites):
        """
        Rend la vue finale avec la carte interactive et le carnet de route.
        Toutes les données sont fournies par le Contrôleur, sans accès direct au modèle.
        Trace également le chemin entre l'hôtel et les activités sur la carte.

        Args:
            itineraire (list[dict]): liste des étapes du voyage
            lat_ville (float): latitude du centre de la ville de destination
            lon_ville (float): longitude du centre de la ville de destination
            hotel (dict): informations de l'hôtel choisi
            activites (list[dict]): liste ordonnée des activités sélectionnées
        """
        self.afficher_barre(5)
        self.vider_ecran()

        carnet = ctk.CTkScrollableFrame(self.container, width=400, fg_color=self.c["primaire"])
        carnet.pack(side="right", fill="y", padx=(15, 0))

        header_carnet = ctk.CTkFrame(carnet, fg_color=self.c["accent"], corner_radius=5)
        header_carnet.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(header_carnet, text="CARNET DE ROUTE", font=self.p["h3"], text_color=self.c["texte_clair"]).pack(pady=10)

        carte = tkintermapview.TkinterMapView(self.container, corner_radius=10, bg_color=self.c["fond_clair"])
        carte.pack(side="left", fill="both", expand=True)
        carte.set_position(lat_ville, lon_ville)
        carte.set_zoom(14)

        for i in range(len(itineraire)):
            etape = itineraire[i]
            if etape["jour"]:
                ctk.CTkLabel(carnet, text=etape["jour"], font=self.p["corps_gras"], text_color=self.c["fond_clair"]).pack(pady=(15, 5), anchor="w", padx=10)

            ligne = ctk.CTkFrame(carnet, fg_color=self.c["secondaire"], corner_radius=6)
            ligne.pack(fill="x", pady=4, padx=5)

            ctk.CTkLabel(ligne, text=etape['txt'], font=self.p["corps"], text_color=self.c["texte_clair"], wraplength=220, justify="left").pack(side="left", anchor="w", padx=10, pady=8)

            if etape["transit"]:
                ctk.CTkLabel(ligne, text=etape["transit"], font=self.p["petit_italique"], text_color=self.c["fond_clair"]).pack(side="right", padx=10)

        # coordonnees_chemin accumule les points GPS pour tracer le chemin sur la carte
        coordonnees_chemin = []
        hotel_coords = None

        if hotel:
            hotel_coords = (hotel["lat"], hotel["lon"])
            coordonnees_chemin.append(hotel_coords)
            carte.set_marker(hotel["lat"], hotel["lon"], text="🏨 Hôtel", marker_color_circle=self.c["accent"])

        for i in range(len(activites)):
            act = activites[i]
            texte_marqueur = f"{i + 1}. {act['nom']}"

            # Toutes les 3 activités on repasse par l'hôtel sur la carte
            if i > 0 and i % 3 == 0 and hotel_coords:
                coordonnees_chemin.append(hotel_coords)

            act_coords = (act["lat"], act["lon"])
            coordonnees_chemin.append(act_coords)
            carte.set_marker(act["lat"], act["lon"], text=texte_marqueur, marker_color_outside=self.c["primaire"])

            if (i + 1) % 3 == 0 and hotel_coords:
                coordonnees_chemin.append(hotel_coords)

        if hotel_coords and len(activites) % 3 != 0:
            coordonnees_chemin.append(hotel_coords)

        if len(coordonnees_chemin) > 1:
            carte.set_path(coordonnees_chemin, color=self.c["accent"], width=3)
