#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 09:36:13 2026

@author: mathso
"""

class Vue(ctk.CTk):

    def __init__(self, ctrl):
        super().__init__()
        self.ctrl = ctrl
        self.title("France Travel Expert")
        self.geometry("1200x850")
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
    def creer_selecteur_date(self, parent, row, label):
        aujourd_hui = datetime.today()
      
         jours  = [f"{j:02d}" for j in range(1, 32)]
         mois   = [f"{m:02d}" for m in range(1, 13)]
         annees = [str(a) for a in range(aujourd_hui.year, aujourd_hui.year + 2)]

         ctk.CTkLabel(parent, text=label).grid(row=row, column=0, padx=10, pady=8, sticky="e")

         frame_date = ctk.CTkFrame(parent, fg_color="transparent")
         frame_date.grid(row=row, column=1, pady=8, sticky="w")

         var_jour  = ctk.StringVar(value=f"{aujourd_hui.day:02d}")
         var_mois  = ctk.StringVar(value=f"{aujourd_hui.month:02d}")
         var_annee = ctk.StringVar(value=str(aujourd_hui.year))

         ctk.CTkOptionMenu(frame_date, variable=var_jour,  values=jours,  width=65).pack(side="left", padx=2)
         ctk.CTkLabel(frame_date, text="/").pack(side="left")
         ctk.CTkOptionMenu(frame_date, variable=var_mois,  values=mois,   width=65).pack(side="left", padx=2)
         ctk.CTkLabel(frame_date, text="/").pack(side="left")
         ctk.CTkOptionMenu(frame_date, variable=var_annee, values=annees, width=85).pack(side="left", padx=2)
    def afficher_recherche(self):
        self.vider_ecran()
        ctk.CTkLabel(self.container, text="Configuration du Voyage", font=("Arial", 26, "bold")).pack(pady=20)

        f = ctk.CTkFrame(self.container)
        f.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(f, text="Départ :").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.ent_dep = ctk.CTkEntry(f, placeholder_text="Ex: Paris")
        self.ent_dep.insert(0, "Paris")
        self.ent_dep.grid(row=0, column=1, pady=10, sticky="w")

        ctk.CTkLabel(f, text="Arrivée :").grid(row=0, column=2, padx=10, sticky="e")
        self.ent_arr = ctk.CTkEntry(f, placeholder_text="Ex: Lyon")
        self.ent_arr.insert(0, "Lyon")
        self.ent_arr.grid(row=0, column=3, sticky="w")

        self.var_j_all, self.var_m_all, self.var_a_all = self.creer_selecteur_date(f, row=1, label="Date Aller :")

        ctk.CTkLabel(f, text="Heure aller :").grid(row=1, column=2, padx=10, sticky="e")
        self.ent_h_all = ctk.CTkEntry(f, width=80)
        self.ent_h_all.insert(0, "08:00")
        self.ent_h_all.grid(row=1, column=3, sticky="w")

        self.var_j_ret, self.var_m_ret, self.var_a_ret = self.creer_selecteur_date(f, row=2, label="Date Retour :")

        ctk.CTkLabel(f, text="Heure retour :").grid(row=2, column=2, padx=10, sticky="e")
        self.ent_h_ret = ctk.CTkEntry(f, width=80)
        self.ent_h_ret.insert(0, "16:00")
        self.ent_h_ret.grid(row=2, column=3, sticky="w")

        # Cases à cocher pour les catégories d'activités
        self.cat_vars = {}
        frame_cats = ctk.CTkFrame(self.container, fg_color="transparent")
        frame_cats.pack()
        for cat in CATEGORIES_ACTIVITES.keys():
            var = ctk.BooleanVar()
            ctk.CTkCheckBox(frame_cats, text=cat, variable=var).pack(side="left", padx=10)
            self.cat_vars[cat] = var

        ctk.CTkButton(self.container, text="Rechercher", height=45, command=self.valider_recherche).pack(pady=30)
