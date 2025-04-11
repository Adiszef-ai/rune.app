###########################################################################
#! "constants" - wszystkie stałe programu

import os
from dotenv import load_dotenv
import openai


# Ścieżki dostępu
BASE_PATH = os.getcwd()
MAIN_PATH = os.path.join(BASE_PATH, "data", "img_main")
RUNE_PATH = os.path.join(BASE_PATH, "data", "img_rune")


# Ścieżki do plików JSON
DATA_MAIN_PATH = os.path.join(BASE_PATH, "data", "processed", "big_data_rune.json")
DATA_FRONT_PATH = os.path.join(BASE_PATH, "data", "processed", "front_data_rune.json")

# Stałe kolorystyczne
COLORS = {
    "header": "#AA0061",
    "accent": "#E8C57A",
    "text": "#F0EAD6",
    "background": "#0E1117"
}

# Wymiary obrazów
IMG_WIDTH = 1080
IMG_HEIGHT = 600

# Minimalne wymiary dla run 300x300
MIN_WIDTH = 300
MIN_HEIGHT = 300

# Maxymalne wartości dla run 500x500
MAX_WIDTH = 500
MAX_HEIGHT = 500

# # ------------------------------------------------------------------------------
# # KONFIGURACJA API I MODELI
# # ------------------------------------------------------------------------------

# # Wczytaj zmienne środowiskowe z pliku .env
# load_dotenv(os.path.join('env', '.env'))

# # Sprawdzenie, czy klucz API został poprawnie załadowany
# if openai.api_key is None:
#     raise ValueError("Nie znaleziono klucza API w zmiennych środowiskowych.")

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

