"""
volva.py - Mistyczna wieszczka, która interpretuje runy i udziela magicznych odpowiedzi.
"""

import random
import streamlit as st
import openai
from typing import Optional, Tuple
import os

from styles import load_css
from supp import load_volva_image, load_all_runes, load_rune_data_from_json, get_api_key
from constants import COLORS
from models import RunaPelna

# Preload assets
volva_image = load_volva_image()
runes = load_all_runes()
rune_data = load_rune_data_from_json()


class VolvaMystyczna:
    """Klasa obsługująca funkcjonalność i zachowanie wieszczki Volvy."""
    
    def __init__(self):
        self.image = volva_image
        self.runes = runes
        self.colors = {
            "primary": "#C147E9",
            "secondary": "#FFD700",
            "accent": "#AA0061",
            "text": "#FFFFFF",
            "background": "rgba(62, 47, 71, 0.5)",
            "shadow": "0 0 15px #C147E9",
            "border": "2px solid #C147E9"
        }
    
    def show_welcome(self):
        """Wyświetla mistyczne przywitanie z wizualnym formatowaniem."""
        st.markdown(
            f"""
            <h1 style="font-size: 53px; font-weight: bold; text-align: center; 
                      color: {self.colors['primary']}; text-shadow: {self.colors['shadow']};">
                Völva - Wieszczka Run
            </h1>
            """,
            unsafe_allow_html=True,
        )
        
        st.image(self.image)

        st.markdown(
            f"""
            <h2 style="font-size: 30px; text-align: center; 
                      color: {self.colors['secondary']}; text-shadow: {self.colors['shadow']};">
                Witaj, poszukiwaczu pradawnej mądrości...
            </h2>
            
            <p style="text-align: center; font-size: 18px;">
            Przekroczyłeś próg zapomnianych tajemnic, gdzie czas splata się z losem, a runy szepczą do tych, którzy chcą słuchać.<br>
            Ja jestem <strong>Völva</strong>, wieszczka dawnych czasów, strażniczka pradawnych run.<br>
            Twoja intencja jest niczym iskra w ciemności. Może zwiastować początek nowej ścieżki lub być ostrzeżeniem przed tym, co nadchodzi.<br>
            Czy pragniesz odpowiedzi? Czy masz odwagę spojrzeć w oczy przeznaczeniu?<br>
            <em>Zamknij oczy, wsłuchaj się w szept płomieni...</em>
            </p>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    
    def display_consultation_form(self):
        """Wyświetla interaktywny formularz konsultacji z Volvą."""
        with st.form("konsultacja_form"):
            # Pole na pytanie
            question = st.text_area(
                "Zadaj pytanie runom:",
                placeholder="Co kryje się w mgle przyszłości?",
                height=100
            )

            # Stylizowany label dla radio
            st.markdown(
                f"""
                <label style="font-size: 20px; color: {self.colors['secondary']};">
                    Wybierz sposób odpowiedzi:
                </label>
                """, 
                unsafe_allow_html=True
            )
            
            answer_mode = st.radio(
                "",  # Pusty, bo label wyżej
                options=["Odpowiedź Volvy bez runy", "Losuj runę i interpretuj"]
            )

            st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                submitted = st.form_submit_button("🔮 Poznaj przepowiednię")

            return question, answer_mode, submitted
    
    def display_prophecy(self, prophecy: str, selected_rune: Optional[RunaPelna] = None, 
                         is_reversed: bool = False):
        """Wyświetla przepowiednię w stylizowanym formacie."""
        if not prophecy:
            st.error("Runy milczą... Spróbuj ponownie z większą szczerością intencji.")
            return
            
        st.divider()
        
        # Jeśli wybrano runę, pokaż ją
        if selected_rune:
            # Nazwa runy
            rune_title = f"{selected_rune.nazwa}{' (odwrócona)' if is_reversed else ''}"
            st.markdown(
                f"""
                <h2 style="text-align: center; color: {self.colors['secondary']}; 
                         font-size: 2rem; text-shadow: {self.colors['shadow']};">
                    {rune_title}
                </h2>
                """,
                unsafe_allow_html=True,
            )

            # Obraz runy
            col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
            with col_img2:
                try:
                    if not os.path.exists(selected_rune.obraz):
                        st.error(f"Nie można znaleźć obrazu runy: {selected_rune.obraz}")
                    else:
                        # Dodaj niestandardowy CSS dla czerwonego obramowania
                        if is_reversed:
                            st.markdown("""
                                <style>
                                .runa-container .runa-img {
                                    border: 5px solid #FF0000 !important;
                                    border-radius: 8px;
                                }
                                </style>
                            """, unsafe_allow_html=True)
                        selected_rune.pokaz_interaktywny_obraz(odwroc=is_reversed)
                except Exception as e:
                    st.error(f"Błąd podczas wyświetlania obrazu runy: {str(e)}")
            
            st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
        
        # Tytuł przepowiedni
        st.markdown(f"""
        <h2 style="text-align: center; color: {self.colors['secondary']}; 
                font-size: 2.2rem; text-shadow: 0 0 15px {self.colors['primary']};">
            ᚹ Proroctwo Völvy ᚹ
        </h2>
        """, unsafe_allow_html=True)
        
        # Treść przepowiedni
        st.markdown(f"""
        <div style="padding: 20px; border: {self.colors['border']}; border-radius: 20px; 
                  background: {self.colors['background']}; 
                  box-shadow: 0 0 15px {self.colors['accent']};">
            <p style="text-align: center; font-size: 18px; line-height: 1.7;">
                <em>„{prophecy}"</em>
            </p>
            <p style="text-align: center; font-style: italic; font-size: 14px; color: #AAAAAA; margin-top: 15px;">
                Słuchaj głosu run, lecz pamiętaj – przyszłość jest jak płynąca rzeka, 
                zawsze w ruchu, zmieniająca swój bieg zgodnie z twoimi wyborami.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    def interpret_question(self, question: str, answer_mode: str) -> Tuple[str, Optional[RunaPelna], bool]:
        """
        Interpretuje pytanie i generuje odpowiedź, zwracając przepowiednię,
        opcjonalnie wybraną runę oraz informację czy runa jest odwrócona.
        """
        if not question:
            return "", None, False
            
        prophecy = ""
        selected_rune = None
        is_reversed = False
        
        with st.spinner("Runy szepczą... Völva odczytuje ich przesłanie..."):
            if answer_mode == "Odpowiedź Volvy bez runy":
                prophecy = self._generate_volva_response(question)
            else:
                selected_rune = random.choice(self.runes)
                is_reversed = random.random() < 0.33  # 33% szans na odwróconą runę
                prophecy = self._interpret_rune_with_question(question, selected_rune, is_reversed)
                
        return prophecy, selected_rune, is_reversed
    
    def _generate_volva_response(self, question: str) -> str:
        """Generuje odpowiedź Volvy bez użycia runy, korzystając z OpenAI."""
        api_key = st.session_state.get("volva_key")
        if not api_key:
            return "🌙 Potrzebuję klucza API, by wsłuchać się w szept run... 🌙"
        
        openai.api_key = api_key
        
        try:
            prompt = f"""
            Wciel się w Völvę - nordycką wieszczkę, mistyczkę starożytnego świata skandynawskiego.
            Odpowiedz na pytanie użytkownika: '{question}'
            
            Twoja odpowiedź powinna być:
            - Mistyczna, pełna poetyckich metafor związanych z nordycką mitologią
            - Zawierać odniesienia do sił natury, Yggdrasilu, Norny czy innych skandynawskich konceptów
            - Głęboka, refleksyjna, ale jednocześnie konkretna
            - Zawierać praktyczną mądrość ukrytą w mitycznych słowach
            - Zakończona krótką radą lub sugestią rytuału
            
            Format odpowiedzi:
            - 3-4 krótkie akapity
            - Pierwszy akapit: kontekst pytania i znaczenie dla pytającego
            - Środkowe akapity: głębsza interpretacja z odniesieniami do mitologii nordyckiej
            - Ostatni akapit: rada lub sugestia rytuału (np. "zapal świecę o północy i szepnij swoje pragnienie do płomienia")
            
            Ogranicz całą odpowiedź do maksymalnie 250 słów.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Jesteś Völvą - nordycką wieszczką, posiadającą mistyczną wiedzę run i starej magii."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.85,  # Wyższa temperatura dla bardziej kreatywnych odpowiedzi
                max_tokens=350
            )
            
            return response['choices'][0]['message']['content']
            
        except Exception as e:
            return f"Runy dzisiaj milczą... (Błąd: {str(e)})"
    
    def _interpret_rune_with_question(self, question: str, runa: RunaPelna, is_reversed: bool) -> str:
        """Interpretuje runę w kontekście zadanego pytania używając OpenAI."""
        api_key = st.session_state.get("volva_key")
        if not api_key:
            return "🔮 Potrzebuję klucza API by odczytać mądrość run..."
        
        openai.api_key = api_key
        
        try:
            prompt = f"""
            Jako Völva, nordycka wieszczka run, zinterpretuj runę {runa.nazwa} 
            w kontekście pytania: '{question}'. 
            
            {f"Runa jest w pozycji ODWRÓCONEJ, co znacząco zmienia jej energię i przesłanie. W tej pozycji runa {runa.nazwa} może wskazywać na:" if is_reversed else ""}
            {f"- Przeciwieństwo jej normalnego znaczenia" if is_reversed else ""}
            {f"- Zablokowaną lub stłumioną energię" if is_reversed else ""}
            {f"- Ukryte aspekty jej znaczenia" if is_reversed else ""}
            {f"- Ostrzeżenie przed niewłaściwym wykorzystaniem energii" if is_reversed else ""}
            
            Użyj mistycznego języka pełnego nordyckich metafor, symboli natury i odwołań do Yggdrasilu.
            
            Odpowiedź powinna zawierać:
            1. Podstawowe znaczenie runy {runa.nazwa} {f"w pozycji odwróconej" if is_reversed else ""}
            2. Jak energia tej runy łączy się z pytaniem osoby
            3. Jaką mądrość lub przestrogę niesie runa dla pytającego
            4. Subtelną radę lub mini-rytuał, który pomoże pytającemu wykorzystać energię runy
            
            Format: 3-4 krótkie, poetyckie akapity, łącznie maks. 500 słów.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Jesteś Völvą - nordycką wieszczką posiadającą głęboką wiedzę o runie {runa.nazwa}."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.85,
                max_tokens=350
            )
            
            return response['choices'][0]['message']['content']
            
        except Exception as e:
            return f"Runy milczą... (Błąd: {str(e)})"


def display_volva():
    """Główna funkcja wyświetlająca interfejs wieszczki Volvy."""
    load_css()  # Załaduj niestandardowy CSS
    
    volva = VolvaMystyczna()
    
    # Sprawdź, czy klucz API jest dostępny
    api_key = get_api_key()
    if not api_key:
        st.warning("💫 Völva czeka na twój dar... Wprowadź klucz API OpenAI, aby kontynuować.")
        return
    
    # Wyświetl interfejs Volvy
    volva.show_welcome()
    
    # Formularz konsultacji
    question, answer_mode, submitted = volva.display_consultation_form()
    
    # Obsługa wysłanego formularza
    if submitted:
        if not question:
            st.warning("Wprowadź pytanie, aby otrzymać odpowiedź run.")
        else:
            prophecy, selected_rune, is_reversed = volva.interpret_question(question, answer_mode)
            volva.display_prophecy(prophecy, selected_rune, is_reversed)
