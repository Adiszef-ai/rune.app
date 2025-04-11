####################################
#TODO "supp" - FUNKCJE POMOCZNICZE
#*##################################

import os
import json
import random
from PIL import Image
import streamlit as st
from constants import MAIN_PATH, RUNE_PATH, IMG_WIDTH, IMG_HEIGHT, DATA_MAIN_PATH, DATA_FRONT_PATH, COLORS
from models import Runa, RunaPelna
from dotenv import load_dotenv
import openai


def load_rune_data_from_json(path=DATA_MAIN_PATH):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def init_rune_data():
    """Inicjalizuje dane run z odpowiednich plików"""
    # Ładowanie danych frontendowych
    try:
        with open(DATA_FRONT_PATH, encoding="utf-8") as f:
            frontend_data = json.load(f)
        is_valid, message = validate_rune_data(frontend_data, is_frontend=True)
        if not is_valid:
            st.error(f"Błąd w pliku runes_data.json: {message}")
            return None, None
    except Exception as e:
        st.error(f"Nie można załadować pliku runes_data.json: {e}")
        return None, None
    
    # Ładowanie pełnych danych
    try:
        with open(DATA_MAIN_PATH, "r", encoding="utf-8") as f:
            full_data = json.load(f)
        is_valid, message = validate_rune_data(full_data, is_frontend=False)
        if not is_valid:
            st.error(f"Błąd w pliku big_data_rune.json: {message}")
            return frontend_data, None
    except Exception as e:
        st.error(f"Nie można załadować pliku big_data_rune.json: {e}")
        return frontend_data, None
    
    return frontend_data, full_data


def load_all_runes():
    """Ładuje uproszczone dane run do wyświetlania w interfejsie"""
    try:
        with open(DATA_FRONT_PATH, encoding="utf-8") as f:
            data = json.load(f)
        print(f"Załadowano {len(data)} rekordów z runes_data.json")
        
        # Standardowa kolejność run w Futharku
        futhark_order = [
            "Fehu", "Uruz", "Thurisaz", "Ansuz", "Raidho", 
            "Kenaz", "Gebo", "Wunjo", "Hagalaz", "Nauthiz", 
            "Isa", "Jera", "Eihwaz", "Perthro", "Algiz", 
            "Sowilo", "Tiwaz", "Berkano", "Ehwaz", "Mannaz",
            "Laguz", "Ingwaz", "Dagaz", "Othala"
        ]
        
        runes = []
        for nazwa in futhark_order:
            if nazwa in data:
                # Używamy poprawnej ścieżki do obrazów run
                obraz_path = os.path.join(RUNE_PATH, f"{nazwa.split()[0].lower()}.jpg")
                
                # Tworzymy obiekt Runa i ładujemy opis
                runa = Runa(nazwa=nazwa, obraz=obraz_path)
                runa.załaduj_opis()
                
                runes.append(runa)
        
        print(f"Utworzono {len(runes)} obiektów Runa")
        return runes
    except Exception as e:
        print(f"Błąd podczas ładowania run z runes_data.json: {e}")
        st.error(f"Błąd ładowania run: {e}")
        return []



def load_full_rune_data():
    """Ładuje pełne dane run do interpretacji"""
    try:
        with open(DATA_MAIN_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        print(f"Załadowanych rekordów z big_data_rune.json: {len(data)}")
        
        runes = []
        for r in data:
            try:
                # Upewniamy się, że wszystkie wymagane pola istnieją
                required_fields = ["nazwa", "krotki_opis", "opis", "znaczenie", 
                                  "interpretacja", "keywords", "url_zdjecia", 
                                  "url", "aett", "pozycja"]
                
                # Sprawdzamy czy obiekt ma wszystkie wymagane pola
                has_all_fields = all(field in r for field in required_fields)
                
                if not has_all_fields:
                    missing = [field for field in required_fields if field not in r]
                    print(f"Brakujące pola dla runy {r.get('nazwa', 'bez nazwy')}: {missing}")
                    continue
                
                # Tworzymy obiekt RunaPelna
                runa = RunaPelna(**r)
                runes.append(runa)
            except Exception as e:
                print(f"Błąd podczas przetwarzania runy {r.get('nazwa', 'bez nazwy')}: {e}")
                
        print(f"Pomyślnie załadowano {len(runes)} run z big_data_rune.json")
        return runes
    except FileNotFoundError:
        error_msg = "Plik big_data_rune.json nie znaleziony!"
        print(error_msg)
        st.error(error_msg)
        return []
    except json.JSONDecodeError as e:
        error_msg = f"Błąd parsowania pliku JSON: {e}"
        print(error_msg)
        st.error(error_msg)
        return []
    except Exception as e:
        error_msg = f"Nieoczekiwany błąd podczas ładowania danych run: {e}"
        print(error_msg)
        st.error(error_msg)
        return []


def load_main_images():
    """Ładuje główne obrazy z folderu i przekształca je do odpowiednich rozmiarów."""
    try:
        main_jpg = [f for f in os.listdir(MAIN_PATH) if f.endswith('.jpg')]
        if not main_jpg:
            st.warning("Brak dostępnych obrazów w folderze.")
            return None

        imain = {os.path.splitext(file)[0]: Image.open(os.path.join(MAIN_PATH, file)) for file in main_jpg}

        # Zmień rozmiar głównego obrazu
        if "maina" in imain:
            return imain["maina"].resize((IMG_WIDTH, IMG_HEIGHT))
        return None
    except Exception as e:
        st.error(f"Wystąpił błąd podczas ładowania obrazów: {e}")
        return None


def validate_rune_data(data, is_frontend=False):
    """Sprawdza poprawność struktury danych run"""
    if is_frontend:
        # Sprawdzenie struktury runes_data.json (baza frontendowa)
        if not isinstance(data, dict):
            return False, "Oczekiwano słownika z nazwami run jako kluczami"
        
        for rune_name, rune_data in data.items():
            required_fields = ["znaczenie", "symbolika", "energia", "praktyczne_zastosowanie"]
            for field in required_fields:
                if field not in rune_data:
                    return False, f"Brak wymaganego pola '{field}' dla runy '{rune_name}'"
    else:
        # Sprawdzenie struktury all_data_runes.json (baza główna)
        if not isinstance(data, list):
            return False, "Oczekiwano listy obiektów run"
        
        for rune in data:
            required_fields = ["nazwa", "krotki_opis", "opis", "znaczenie", 
                             "interpretacja", "keywords", "url_zdjecia", "url", "aett", "pozycja"]
            for field in required_fields:
                if field not in rune:
                    return False, f"Brak wymaganego pola '{field}' dla runy '{rune.get('nazwa', 'bez nazwy')}'"
    
    return True, "Dane są poprawne"

from PIL import Image
import io

def load_volva_image():
    try:
        # Otwieranie obrazu z ignorowaniem błędów
        with Image.open("./data/img_main/volva3.jpg") as img:
            img = img.convert("RGB")  # Konwertuj do RGB, jeśli to konieczne
            img.load()  # Wczytaj obraz
        return img
    except OSError:
        print("Błąd: Plik obrazu jest uszkodzony lub niekompletny.")
        return None


def create_runes_list():
    """Tworzy listę obiektów reprezentujących runy nordyckie i ich atrybuty."""
    runy = []
    for nazwa in [
        "Fehu", "Uruz", "Thurisaz", "Ansuz", "Raidho", 
        "Kenaz", "Gebo", "Wunjo", "Hagalaz", "Nauthiz", 
        "Isa", "Jera", "Eihwaz", "Perthro", "Algiz", 
        "Sowilo", "Tiwaz", "Berkano", "Ehwaz", "Mannaz",
        "Laguz", "Ingwaz", "Dagaz", "Othala"
    ]:
        runa = Runa(nazwa, os.path.join(RUNE_PATH, f"{nazwa.split()[0].lower()}.jpg"))
        runa.załaduj_opis()
        runy.append(runa)
    return runy


def losuj_rune(runy):
    """Losuje runę i zapisuje ją w stanie sesji."""
    try:
        wylosowana = random.choice(runy)
        st.session_state["Runa dnia"] = wylosowana  # Zapisz do stanu sesji
    except Exception as e:
        st.error(f"Wystąpił błąd przy losowaniu runy: {e}")



def get_api_key():
    """Rytuał składania ofiary dla Völvy"""
    # Check if API key is already in session state
    if "volva_key" in st.session_state and st.session_state.volva_key:
        return st.session_state.volva_key
        
    # Show title above the API key input
    st.markdown(
        f"""
        <h1 style="font-size: 53px; font-weight: bold; text-align: center; color: {COLORS['accent']};">
        Völva - Wieszczka Run
        </h1>
        """,
        unsafe_allow_html=True,
    )
    
    # Create a container for the API key input
    with st.container():
        st.markdown('''
        *„Mądrość run nie objawia się bez ofiary...*  
        *By Völva przemówiła, złóż w darze*  
        *magiczny klucz do bram wiedzy."*  
        ''')
        
        api_key = st.text_input(
            "Wprowadź swój **Klucz Mądrości** (API Key):",
            type="password",
            placeholder="sk-...twoja_ofiara_dla_bogów_wiedzy..."
        )
        
        st.caption('„Każda prawdziwa wiedza wymaga poświęcenia – Odin oddał oko za mądrość run"')
        
        if api_key:
            st.session_state.volva_key = api_key
            st.rerun()  # This will refresh the page and hide the input
            return api_key
        else:
            return None
