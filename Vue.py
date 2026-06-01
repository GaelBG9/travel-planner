ETAPES = ["Recherche", "Trains", "Hôtel", "Activités", "Planning", "Carnet"]


class Vue(ctk.CTk):
    """
    Interface utilisateur graphique (IHM) basée sur CustomTkinter. 
    """

    def __init__(self, ctrl):
        """
        Initialise la fenêtre dans laquelle se crée l'application, importe les variables de styles (thèmes, polices)
        """
        super().__init__()
        self.ctrl = ctrl
        self.title("Voyage Voyage")
        self.geometry("1200x850")

        self.c = THEME["couleurs"]
        self.p = THEME["polices"]

        self.barre_etapes = ctk.CTkFrame(self, height=65, fg_color=self.c["primaire"], corner_radius=0)
        self.barre_etapes.pack(fill="x")

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True, padx=20, pady=(10, 20))

    def afficher_barre(self, etape_active):
        """
        Génère la barre de progression 
        en colorant différemment les étapes passées et les futures.
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
                couleur_trait = self.c["succes"] if i < etape_active else self.c["secondaire"]
                ctk.CTkFrame(self.barre_etapes, height=2, width=30, fg_color=couleur_trait, corner_radius=0).pack(side="left", pady=(0, 22))

    def vider_ecran(self):
        """
        Méthode qui détruit l'intégralité des widgets Tkinter existants 
        dans le conteneur central pour le préparer à l'affichage de la prochaine vue.
        """
        for widget in self.container.winfo_children():
            widget.destroy()

    def afficher_chargement(self, message):
        """
        Affiche temporairement un écran d'attente pendant que le contrôleur 
        effectue des calculs ou interroge des API.
        """
        self.vider_ecran()
        ctk.CTkLabel(self.container, text=message, font=self.p["h2"], text_color=self.c["texte_fonce"]).pack(expand=True)

    def creer_selecteur_date(self, parent, row, label):
        """
        Crée une interface composée d'une étiquette (Label) et de trois listes 
        déroulantes (OptionMenus) permettant à l'utilisateur de composer facilement une date.
        """
        aujourdhui = datetime.today()

        jours = []
        for j in range(1, 32): jours.append(f"{j:02d}")

        mois = []
        for m in range(1, 13): mois.append(f"{m:02d}")

        annees = []
        for a in range(aujourdhui.year, aujourdhui.year + 2): annees.append(str(a))

        ctk.CTkLabel(parent, text=label, font=self.p["corps_gras"], text_color=self.c["texte_fonce"]).grid(row=row, column=0, padx=20, pady=15, sticky="e")
        frame_date = ctk.CTkFrame(parent, fg_color="transparent")
        frame_date.grid(row=row, column=1, pady=15, sticky="w")

        v_j = ctk.StringVar(value=f"{aujourdhui.day:02d}")
        v_m = ctk.StringVar(value=f"{aujourdhui.month:02d}")
        v_a = ctk.StringVar(value=str(aujourdhui.year))

        ctk.CTkOptionMenu(frame_date, variable=v_j, values=jours, width=65, fg_color=self.c["primaire"]).pack(side="left", padx=2)
        ctk.CTkLabel(frame_date, text="/", text_color=self.c["texte_fonce"]).pack(side="left")
        ctk.CTkOptionMenu(frame_date, variable=v_m, values=mois, width=65, fg_color=self.c["primaire"]).pack(side="left", padx=2)
        ctk.CTkLabel(frame_date, text="/", text_color=self.c["texte_fonce"]).pack(side="left")
        ctk.CTkOptionMenu(frame_date, variable=v_a, values=annees, width=85, fg_color=self.c["primaire"]).pack(side="left", padx=2)
        return v_j, v_m, v_a

    def lire_date(self, var_j, var_m, var_a):
        """
        Fonction qui extrait et concatène les valeurs des variables Tkinter 
        liées aux menus déroulants pour former une date au format dont a besoin l'API.
        """
        return f"{var_a.get()}-{var_m.get()}-{var_j.get()}"

    def afficher_recherche(self):
        """
        Dessine le formulaire initial. Entrées de texte pour les villes, sélecteurs 
        de dates, cases à cocher pour les intérêts, et la génération aléatoire des images.
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

        toutes_les_villes = list(GARES.keys())
        villes_finales = random.sample(toutes_les_villes, 4)

        for ville in villes_finales:
            card_img = ctk.CTkFrame(frame_img, height=150, fg_color=self.c["primaire"], corner_radius=10)
            card_img.pack(side="left", expand=True, fill="both", padx=10)
            card_img.pack_propagate(False)

            if os.path.exists(ville + ".jpg"):
                photo = Image.open(photos/ville + ".jpg")
                photo = photo.resize((280, 150))
                photo_ctk = ctk.CTkImage(light_image=photo, size=(350, 200))
                lbl_photo = ctk.CTkLabel(card_img, image=photo_ctk, text="")
                lbl_photo.place(relx=0, rely=0, relwidth=1, relheight=1)

            bandeau = ctk.CTkFrame(card_img, fg_color=self.c["primaire"], corner_radius=0, height=40)
            bandeau.place(relx=0, rely=1.0, anchor="sw", relwidth=1)
            ctk.CTkLabel(bandeau, text=f"📍 {ville}", font=self.p["corps_gras"], text_color=self.c["texte_clair"]).place(relx=0.5, rely=0.5, anchor="center")
            card_img.bind("<Button-1>", lambda e, v=ville: self.ctrl.definir_destination(v))
            for enfant in card_img.winfo_children():
                enfant.bind("<Button-1>", lambda e, v=ville: self.ctrl.definir_destination(v))
            
    def mettre_a_jour_destination(self, ville):
        self.ent_arr.delete(0, "end")
        self.ent_arr.insert(0, ville)
        
        
    def valider_recherche(self):

        self.ctrl.valider_recherche_globale(
        self.ent_dep.get(), self.ent_arr.get(),
        self.var_j_all.get(), self.var_m_all.get(), self.var_a_all.get(), self.ent_h_all.get(),
        self.var_j_ret.get(), self.var_m_ret.get(), self.var_a_ret.get(), self.ent_h_ret.get(),
        self.cat_vars
    )

    def afficher_selection_trains(self, trains_aller, trains_retour, idx_rapide_aller, idx_rapide_retour):
        """
        Cree deux zones d'affichage (colonnes) 
        pour présenter les des trajets allers à gauche et retours à droite.
        """
        self.afficher_barre(1)
        self.vider_ecran()
        self.train_buttons = {"ALLER": [], "RETOUR": []}

        ctk.CTkLabel(self.container, text="Choisissez vos horaires de train", font=self.p["h2"], text_color=self.c["texte_fonce"]).pack(pady=(10, 20))
        main_f = ctk.CTkFrame(self.container, fg_color="transparent")
        main_f.pack(fill="both", expand=True)

        self.afficher_colonne_trains(main_f, trains_aller, "ALLER", "left", idx_rapide_aller)
        self.afficher_colonne_trains(main_f, trains_retour, "RETOUR", "right", idx_rapide_retour)

        ctk.CTkButton(self.container, text="Valider les Trains ➔", height=50, fg_color=self.c["accent"], hover_color=self.c["accent_hover"], font=self.p["h3"], text_color=self.c["texte_clair"], command=self.ctrl.lancer_recherche_hotels).pack(pady=20)

    def afficher_colonne_trains(self, parent, liste_trains, titre, cote, idx_rapide):
        """
        Affiche les données de train spécifiques à une colonne. 
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
                color_direct = self.c["texte_fonce"]
            else:
                label_direct = f"VIA {t['transfert'].upper()}"
                color_direct = self.c["avertissement"]

            ctk.CTkLabel(haut, text=label_direct, font=self.p["mini_gras"], text_color=color_direct).pack(side="left", padx=5)

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
        Modifie la couleur et le texte des boutons de la liste des trains. 
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
        Affiche une grille d' hôtel récupéré via OSMnx. Un bouton permet sa réservation.
        """
        self.afficher_barre(2)
        self.vider_ecran()
        ctk.CTkLabel(self.container, text="Choisissez votre Hébergement", font=self.p["h2"], text_color=self.c["texte_fonce"]).pack(pady=(10, 20))

        scroll = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10)
        scroll.grid_columnconfigure((0, 1, 2), weight=1)

        for i in range(len(hotels)):
            h = hotels[i]
            row = i // 3
            col = i % 3

            card = ctk.CTkFrame(scroll, corner_radius=10, fg_color=self.c["texte_clair"])
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")

            ctk.CTkLabel(card, text="🏨", font=("Arial", 30)).pack(pady=(15, 5))
            ctk.CTkLabel(card, text=h["nom"], font=self.p["corps_gras"], text_color=self.c["texte_fonce"], wraplength=200).pack(pady=5, padx=10)
            ctk.CTkButton(card, text="Réserver", fg_color=self.c["primaire"], hover_color=self.c["secondaire"], text_color=self.c["texte_clair"], command=lambda x=h: self.ctrl.choisir_hotel(x)).pack(pady=15, side="bottom")

    def afficher_selection_activites(self, activites, max_activites):
        """
        Permet à l'utilisateur de cocher les activités qu'il souhaite faire. 
        Met un compteur pour limiter le choix final (3 / jour).
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

            def notification_clic(act=a, var=var_chk):
                """Fonction de relais très légère : avertit le contrôleur du clic."""
                autorise = self.ctrl.gerer_selection_activite(act, var.get())
                if not autorise:
                    var.set(False)

            chk = ctk.CTkCheckBox(card, text="Ajouter", variable=var_chk, command=notification_clic, fg_color=self.c["succes"], hover_color=self.c["succes_hover"], text_color=self.c["texte_fonce"], font=self.p["corps"])
            chk.pack(anchor="e", padx=10, pady=10, side="bottom")

        ctk.CTkButton(self.container, text="Planifier mes journées ➔", height=45, font=self.p["h3"], fg_color=self.c["accent"], hover_color=self.c["accent_hover"], text_color=self.c["texte_clair"], command=self.ctrl.lancer_planification).pack(pady=20)

    def afficher_planification(self, planning):
        self.afficher_barre(4)
        self.vider_ecran()
        ctk.CTkLabel(self.container, text="Planifier mes journées", font=self.p["h2"], text_color=self.c["texte_fonce"]).pack(pady=(20, 5))
        ctk.CTkLabel(self.container, text="Clique sur ⇄ pour sélectionner deux activités à échanger", font=self.p["corps"], text_color=self.c["texte_gris"]).pack(pady=(0, 15))

        self.scroll_planning = ctk.CTkScrollableFrame(self.container, fg_color="transparent")
        self.scroll_planning.pack(fill="both", expand=True, padx=20)
        self.afficher_jours(planning, None)
        ctk.CTkButton(self.container, text="Générer le Carnet ➔", height=45, font=self.p["h3"], fg_color=self.c["accent"], hover_color=self.c["accent_hover"], text_color=self.c["texte_clair"], command=self.ctrl.lancer_generation_carnet).pack(pady=20)

    def actualiser_compteur_activites(self, actuel, max_act, alerte=False):
        """Méthode de vue : met à jour le texte et la couleur du compteur."""
        if alerte:
            self.lbl_compteur.configure(text="Limite atteinte !", text_color=self.c["texte_clair"], fg_color=self.c["accent"])
        else:
            self.lbl_compteur.configure(text=f"{actuel} / {max_act} (3 par jour)", text_color=self.c["accent"], fg_color=self.c["fond_clair"])

    def afficher_jours(self, planning, index_selectionne):
        """
        Reçoit directement les données calculées par le Contrôleur 
        pour afficher le planning et colorer l'élément sélectionné si besoin.
        """
        for widget in self.scroll_planning.winfo_children():
            widget.destroy()

        jours_ordonnes = sorted(planning.keys())
        for jour in jours_ordonnes:
            acts = planning[jour]

            bloc = ctk.CTkFrame(self.scroll_planning, fg_color=self.c["texte_clair"], corner_radius=10)
            bloc.pack(fill="x", pady=8, padx=5)

            header = ctk.CTkFrame(bloc, fg_color=self.c["primaire"], corner_radius=8)
            header.pack(fill="x", padx=4, pady=4)
            ctk.CTkLabel(header, text=f"  Jour {jour + 1}  —  {len(acts)}/3 activités", font=self.p["corps_gras"], text_color=self.c["texte_clair"]).pack(side="left", padx=10, pady=6)

            for idx in range(len(acts)):
                act = acts[idx]
                # On utilise l'argument fourni par le Contrôleur
                est_selectionnee = (index_selectionne == (jour, idx))

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
                ctk.CTkButton(ligne, text=texte_btn, width=120, height=28, font=self.p["corps"], fg_color=couleur_btn, text_color=self.c["texte_clair"], corner_radius=6, command=lambda j=jour, i=idx: self.ctrl.reordonner_planning(j, i)).pack(side="right", padx=8, pady=6)

    def afficher_final(self, itineraire, lat_ville, lon_ville, hotel, activites):
        """
        Affiche la carte interactive de tkintermapview avec l'itinéraire 
        complet généré. Positionne les marqueurs.
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

        coordonnees_chemin = []
        hotel_coords = None

        if hotel:
            hotel_coords = (hotel["lat"], hotel["lon"])
            coordonnees_chemin.append(hotel_coords)
            carte.set_marker(hotel["lat"], hotel["lon"], text="🏨 Hôtel", marker_color_circle=self.c["accent"])

        for i in range(len(activites)):
            act = activites[i]
            numero = str(i + 1)
            texte_marqueur = f"{numero}. {act['nom']}"

            if i > 0 and i % 3 == 0 and hotel_coords:
                coordonnees_chemin.append(hotel_coords)

            act_coords = (act["lat"], act["lon"])
            coordonnees_chemin.append(act_coords)
            carte.set_marker(act["lat"], act["lon"], text=texte_marqueur, marker_color_outside=self.c["primaire"])

            if (i + 1) % 3 == 0 and hotel_coords:
                coordonnees_chemin.append(hotel_coords)

        if hotel_coords and len(activites) % 3 != 0:
            coordonnees_chemin.append(hotel_coords)