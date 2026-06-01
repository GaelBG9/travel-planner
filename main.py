#Librairies générales
import math
from datetime import datetime

#IHM
import customtkinter as ctk
import tkintermapview

#API
from urllib.parse import quote
import requests
import osmnx as ox
import pandas as pd

#Photos de présentation
from PIL import Image, ImageTk
import os
import random

from controleur.py import Controleur


if __name__ == "__main__":
    Controleur().lancer()
