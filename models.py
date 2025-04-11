import os
import base64
import streamlit as st
from PIL import Image
import json
import random
from constants import DATA_FRONT_PATH, MAX_HEIGHT, MAX_WIDTH, MIN_WIDTH, MIN_HEIGHT
import io


class RunaPelna:
    """Baza danych run, glowna klasa do przechowywania informacji o runach.
    Klasa ta zawiera wszystkie atrybuty runy, takie jak nazwa, opis, znaczenie itp."""

    def __init__(self, nazwa, krotki_opis, opis, znaczenie, interpretacja, keywords,
                 url_zdjecia, url, aett, pozycja, **kwargs):
        self.nazwa = nazwa
        self.krotki_opis = krotki_opis
        self.opis = opis
        self.znaczenie = znaczenie
        self.interpretacja = interpretacja
        self.keywords = keywords
        self.url_zdjecia = url_zdjecia
        self.url = url
        self.aett = aett
        self.pozycja = pozycja
        self.kwargs = kwargs


class ImageProcessor:
    """Klasa odpowiedzialna za przetwarzanie obrazów run."""
    
    @staticmethod
    def open_image(image_path):
        """Otwiera i zwraca obraz jeśli istnieje, w przeciwnym razie zwraca None"""
        try:
            if not os.path.exists(image_path):
                st.error(f"Plik obrazu nie istnieje: {image_path}")
                return None
                
            return Image.open(image_path).convert("RGB")
        except Exception as e:
            st.error(f"Nie można otworzyć obrazu: {image_path}")
            st.text(f"Błąd: {e}")
            return None
    
    @staticmethod
    def resize_image(img, target_width, target_height):
        """Zmienia rozmiar obrazu zachowując proporcje"""
        if img is None:
            return None
            
        try:
            original_width, original_height = img.size
            scale = min(target_width / original_width, target_height / original_height)
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)
            
            return img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        except Exception as e:
            st.error(f"Nie można zmienić rozmiaru obrazu")
            st.text(f"Błąd: {e}")
            return None
    
    @staticmethod
    def process_orientation(img, is_reversed=False, random_orientation=False):
        """
        Przetwarza orientację obrazu runy.
        
        Args:
            img: Obiekt obrazu PIL
            is_reversed: Czy wymusić odwrócenie
            random_orientation: Czy losowo wybierać orientację
            
        Returns:
            tuple: (przetworzony_obraz, czy_odwrocony)
        """
        if img is None:
            return None, False
            
        is_reversed_result = is_reversed
        
        if random_orientation:
            # 33% szans na odwrócenie runy
            is_reversed_result = random.random() < 0.33
        
        if is_reversed_result:
            # Odwracamy obraz o 180 stopni
            img = img.rotate(180)
        
        return img, is_reversed_result
    
    @staticmethod
    def encode_image(img):
        """Koduje obraz do formatu base64 dla wyświetlenia w HTML."""
        if img is None:
            return ""
            
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        return base64.b64encode(buffer.getvalue()).decode()


class HTMLRenderer:
    """Klasa odpowiedzialna za rendering HTML dla wyświetlania run."""
    
    @staticmethod
    def get_border_style(is_reversed):
        """Zwraca styl obramowania w zależności od orientacji runy"""
        if is_reversed:
            return 'border-radius: 20px; border: 5px solid #AA0061;'
        return ''
    
    @staticmethod
    def display_image(encoded_img, display_name, max_width, border_style=""):
        """Generuje i wyświetla kod HTML dla obrazu runy"""
        if not encoded_img:
            st.error(f"Nie można wyświetlić obrazu")
            return
            
        st.markdown(
            f"""
            <div>
                <img src="data:image/jpeg;base64,{encoded_img}" alt="{display_name}" 
                    style="width:100%; max-width: {max_width}px; {border_style}"/>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    @staticmethod
    def display_interactive_image(encoded_img, display_name, max_width, border_style=""):
        """Wyświetla interaktywny obraz runy"""
        if not encoded_img:
            st.error(f"Nie można wyświetlić obrazu")
            return
            
        st.markdown(
            f"""
            <div class="runa-container">
                <img class="runa-img" src="data:image/jpeg;base64,{encoded_img}" alt="{display_name}" 
                    style="width:100%; max-width: {max_width}px; {border_style}"/>
            </div>
            """,
            unsafe_allow_html=True,
        )


class Runa:
    """Frontendowa klasa do pokazywania informacji o runach."""
    
    def __init__(self, nazwa, obraz, **kwargs):
        self.nazwa = nazwa
        self.obraz = obraz
        
        # Extract specific attributes from kwargs if they exist
        self.znaczenie = kwargs.get("znaczenie", "")
        self.symbolika = kwargs.get("symbolika", {})
        self.potencjal = kwargs.get("potencjal", [])
        self.prakt_zastosowanie = kwargs.get("prakt_zastosowanie", [])
        self.dodatkowe_info = kwargs.get("dodatkowe_info", "")
        self.symbol = kwargs.get("symbol", "")
        self.aett = kwargs.get("aett", "")
        self.pozycja = kwargs.get("pozycja", "")
        
        # Store remaining kwargs
        self.kwargs = {k: v for k, v in kwargs.items() 
                    if k not in ["znaczenie", "symbolika", "potencjal", 
                                "prakt_zastosowanie", "dodatkowe_info",
                                "symbol", "aett", "pozycja"]}
                                
        # Helper objects
        self.image_processor = ImageProcessor()
        self.renderer = HTMLRenderer()

    def get_nazwa_odwrocona(self):
        """Zwraca nazwę runy z oznaczeniem, że jest odwrócona."""
        return f"{self.nazwa} (odwrócona)"

    def zmniejsz_obraz(self, width=MIN_WIDTH, height=MIN_HEIGHT):
        """Zmniejsza obraz zachowując proporcje i jakość"""
        img = ImageProcessor.open_image(self.obraz)
        return ImageProcessor.resize_image(img, width, height)

    def zwieksz_obraz(self, width=MAX_WIDTH, height=MAX_HEIGHT):
        """Zwiększa obraz do maksymalnego rozmiaru, zachowując proporcje"""
        img = ImageProcessor.open_image(self.obraz)
        return ImageProcessor.resize_image(img, width, height)

    def pokaz_obraz(self, max_width=MAX_WIDTH, max_height=MAX_HEIGHT, odwroc=False, losowa_orientacja=False):
        """Wyświetla obraz runy z określonymi parametrami"""
        img = self.zmniejsz_obraz(max_width, max_height)
        if img:
            img, jest_odwrocony = ImageProcessor.process_orientation(img, odwroc, losowa_orientacja)
            encoded_img = ImageProcessor.encode_image(img)
            nazwa_wyswietlana = self.get_nazwa_odwrocona() if jest_odwrocony else self.nazwa
            border_style = HTMLRenderer.get_border_style(jest_odwrocony)
            
            HTMLRenderer.display_image(encoded_img, nazwa_wyswietlana, max_width, border_style)
            return jest_odwrocony
        return False

    def pokaz_obraz_dnia(self, odwroc=False, losowa_orientacja=False, size=(500, 500)):
        """Wyświetla obraz runy na dzień."""
        img = self.zwieksz_obraz(size[0], size[1])
        if img:
            img, jest_odwrocony = ImageProcessor.process_orientation(img, odwroc, losowa_orientacja)
            nazwa_wyswietlana = self.get_nazwa_odwrocona() if jest_odwrocony else self.nazwa
            encoded_img = ImageProcessor.encode_image(img)
            HTMLRenderer.display_image(encoded_img, nazwa_wyswietlana, size[0])
            return jest_odwrocony
        return False

    def pokaz_interaktywny_obraz(self, odwroc=False, losowa_orientacja=False, max_width=300):
        """
        Wyświetla obraz runy z interaktywnymi efektami
        
        Args:
            odwroc: Czy obraz powinien być odwrócony (True/False)
            losowa_orientacja: Czy losowo wybierać orientację (True/False)
            max_width: Maksymalna szerokość obrazu
            
        Returns:
            bool: Czy runa jest odwrócona
        """
        img = ImageProcessor.open_image(self.obraz)
        if img:
            img, jest_odwrocony = ImageProcessor.process_orientation(img, odwroc, losowa_orientacja)
            encoded_img = ImageProcessor.encode_image(img)
            nazwa_wyswietlana = self.get_nazwa_odwrocona() if jest_odwrocony else self.nazwa
            
            # Dodaj specjalne obramowanie dla odwróconych run
            border_style = 'border-radius: 20px; border: 5px solid hsl(349, 100%, 45%);' if jest_odwrocony else ''
            
            # Wyświetl interaktywny obraz
            HTMLRenderer.display_interactive_image(encoded_img, nazwa_wyswietlana, max_width, border_style)
            return jest_odwrocony
        return False

    def załaduj_opis(self):
        """Ładowanie opisu runy z pliku JSON."""
        try:
            with open(DATA_FRONT_PATH, 'r', encoding='utf-8') as f:
                opisy = json.load(f)
                if self.nazwa in opisy:
                    opis = opisy[self.nazwa]
                    self.znaczenie = opis.get('znaczenie', '')
                    self.symbolika = opis.get('symbolika', {})
                    self.potencjal = opis.get('potencjal', [])
                    self.prakt_zastosowanie = opis.get('praktyczne_zastosowanie', [])
                    self.dodatkowe_info = opis.get('dodatkowe_info', '')
                    self.symbol = opis.get('symbol', '')
                    self.aett = opis.get('aett', '')
                    self.pozycja = opis.get('pozycja', '')
                else:
                    st.warning(f"Brak opisu dla runy: {self.nazwa}")
        except Exception as e:
            st.error(f"Nie można załadować opisu runy: {str(e)}")