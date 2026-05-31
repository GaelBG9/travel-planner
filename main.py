from controleur.py import Controleur
from Vue import Vue
if __name__ == "__main__":
    ctrl = Controleur()
    vue = Vue(ctrl)
    ctrl.vue = vue
    ctrl.lancer()
