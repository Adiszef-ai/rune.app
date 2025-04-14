###########################################################################
#! features.py - Funkcje związane z funkcjonalnościami aplikacji runicznych
###########################################################################

import random
import streamlit as st
from PIL import Image
from supp import losuj_rune, load_main_images, load_full_rune_data
from models import RunaPelna, Runa
from constants import COLORS
import openai



#?##########################################################################################################
#TODO#######################################################################################################
#?                                                  Wyświetlanie run

def display_browse_runes(runy: list[RunaPelna]) -> None:
    """Wyświetla wszystkie runy nordyckie wraz z ich informacjami."""
    st.markdown(
        f"""
        <h1 style="font-size: 53px; font-weight: bold; text-align: center; color: {COLORS['accent']};">
        Runy Nordyckie
        </h1>
        """,
        unsafe_allow_html=True,
    )

    if main_image := load_main_images():
        st.image(main_image, use_container_width=True)

    st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <h1 style="font-size: 35px; font-weight: bold; text-align: left; color: {COLORS['accent']};">
        Przeglądaj runy
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("", divider="rainbow")
    for runa in runy:
        st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
        display_rune_info(runa)
        st.header("", divider="rainbow")

def display_rune_info(runa: Runa) -> None:
    """Wyświetla szczegółowe informacje o pojedynczej runie."""
    # Górna część z obrazem i nazwą
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(
            f"<h1 style='color: {COLORS['accent']}; font-size: 66px;'>{runa.nazwa}</h1>",
            unsafe_allow_html=True
        )
        # Wyświetl symbol, aett i pozycję w pierwszej kolumnie z większą czcionką i przerwą
        st.markdown(f"<p style='color: {COLORS['accent']}; font-size: 30px;'>Symbol:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='color: {COLORS['text']}; font-weight: bold;'>{runa.symbol}</span></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: {COLORS['accent']}; font-size: 30px;'>Aett:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='color: {COLORS['text']}; font-weight: bold;'>{runa.aett}</span></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: {COLORS['accent']}; font-size: 30px;'>Pozycja:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style='color: {COLORS['text']}; font-weight: bold;'>{runa.pozycja}</span></p>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
        runa.pokaz_interaktywny_obraz()
    
    # Dolna część z detalami rozciągnięta na całą szerokość
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    display_rune_details(runa, show_all=False)

def display_rune_details(runa: Runa, show_all: bool = True) -> None:
    """Wyświetla szczegółowe dane o runie w ustandaryzowanym formacie."""
    if show_all:
        sections = {
            "Symbol": runa.symbol,
            "Aett": runa.aett,
            "Pozycja": runa.pozycja,
            "Znaczenie": runa.znaczenie,
            "Symbolika": runa.symbolika,
            "Potencjał": runa.potencjal,
            "Praktyczne zastosowanie": runa.prakt_zastosowanie,
            "Dodatkowe informacje": runa.dodatkowe_info
        }
    else:
        sections = {
            "Znaczenie": runa.znaczenie,
            "Symbolika": runa.symbolika,
            "Potencjał": runa.potencjal
        }
    
    for section, content in sections.items():
        if not content:
            continue
        st.markdown(f"<h4 style='color: {COLORS['accent']};'>{section}</h4>", unsafe_allow_html=True)
        if isinstance(content, dict):
            for key, value in content.items():
                st.markdown(f"<p style='color: {COLORS['text']};'>▪️ <b>{key}:</b> {value}</p>", unsafe_allow_html=True)
        elif isinstance(content, list):
            for item in content:
                st.markdown(f"<p style='color: {COLORS['text']};'>▪️ {item}</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p style='color: {COLORS['text']};'>{content}</p>", unsafe_allow_html=True)
    

#?##########################################################################################################
#TODO#######################################################################################################
#?                                                  Runa dnia

def display_rune_of_the_day(runy: list[RunaPelna]) -> None:
    """Wyświetla funkcję runy dnia z pełnym opisem."""
    st.markdown(
        f"""
        <h1 style="font-size: 53px; font-weight: bold; text-align: center; color: {COLORS['accent']};">
        Runa Dnia
        </h1>
        """,
        unsafe_allow_html=True,
    )

    if main_image := load_main_images():
        st.image(main_image, use_container_width=True)
    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)

    # Button above the divider, outside of columns
    if st.button("**Wylosuj runę dnia**", use_container_width=True, type="primary"):
        losuj_rune(runy)

    st.subheader("", divider="rainbow")

    st.markdown(
        f"""
        <h1 style="font-size: 35px; font-weight: bold; text-align: left; color: {COLORS['accent']};">
        Twoja runa dnia:
        </h1>
        """,
        unsafe_allow_html=True,
    )
    # Display the rune if it exists in session state
    if "Runa dnia" in st.session_state:
        runa = st.session_state["Runa dnia"]
        display_daily_rune(runa)

def display_daily_rune(runa: RunaPelna) -> None:
    """Wyświetla szczegóły runy dnia."""
    st.markdown(
        f"""
        <h1 style="text-align: center; color: {COLORS['accent']}; font-size: 4rem;">
        {runa.nazwa}
        </h1>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
    # Wyświetlanie obrazu
    col_img1, col_img2, col_img3 = st.columns([1, 6, 1])
    with col_img2:
        runa.pokaz_obraz_dnia(size=(800, 800), losowa_orientacja=False)

    # Wyświetlanie szczegółów bez symbol, aett i pozycja
    with st.container():
        st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
        display_rune_details(runa, show_all=False)

#?##########################################################################################################
#TODO#######################################################################################################
#?                                                  Rozkłady Runiczne

def display_rune_layout(runy: list[RunaPelna]) -> None:
    """Wyświetla różne rozkłady runiczne."""
    st.markdown(
        f"""
        <h1 style="font-size: 53px; font-weight: bold; text-align: center; color: {COLORS['accent']};">
        Rozkłady Runiczne
        </h1>
        """,
        unsafe_allow_html=True,
    )
    if main_image := load_main_images():
        st.image(main_image, use_container_width=True)

    st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
    
    # Main panel buttons for different layouts
    st.markdown("### Wybierz układ run:")
    
    # Create a single row of buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("1 Runa", use_container_width=True, type="primary"):
            st.session_state["selected_layout"] = random.sample(runy, 1)
    
    with col2:
        if st.button("3 Runy", use_container_width=True, type="primary"):
            st.session_state["selected_layout"] = random.sample(runy, 3)
    
    with col3:
        if st.button("5 Run", use_container_width=True, type="primary"):
            st.session_state["selected_layout"] = random.sample(runy, 5)
    
    with col4:
        if st.button("8 Run", use_container_width=True, type="primary"):
            st.session_state["selected_layout"] = random.sample(runy, 8)

    # Display the selected layout in a new section
    if "selected_layout" in st.session_state:
        st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
        display_uklad_run(st.session_state["selected_layout"])

def display_uklad_run(uklad: list[RunaPelna]) -> None:
    """Wyświetla wylosowany układ run."""
    st.header("", divider="rainbow")
    st.markdown(
        f"""
        <h1 style="font-size: 26px; font-weight: bold; text-align: left; color: {COLORS['accent']}; text-shadow: 0 0 10px #C147E9;">
        Interpretacja układu Run
        </h1>
        """,
        unsafe_allow_html=True,
    )

    uklad_len = len(uklad)

    # ✨ Mistyczne opisy dla każdego układu
    if uklad_len == 1:
        st.markdown("""
        <div style="background-color: rgba(193, 71, 233, 0.1); padding: 20px; border-radius: 12px; box-shadow: 0 0 10px #C147E9;">
            <p style="color: #FFD700; font-size: 18px; text-align: center;">
            <strong>Układ 1 Runa</strong><br>
            Jedna runa – jedno objawienie. To serce twojego pytania, rdzeń sytuacji, klucz do zrozumienia.
            </p>
        </div>
        """, unsafe_allow_html=True)

    elif uklad_len == 3:
        st.markdown("""
        <div style="background-color: rgba(193, 71, 233, 0.1); padding: 20px; border-radius: 12px; box-shadow: 0 0 10px #C147E9;">
            <p style="color: #FFD700; font-size: 18px; text-align: center;">
            <strong>Układ 3 Runy – Triada Czasu</strong><br>
            <em>Lewa</em> – przeszłość: duchowe korzenie pytania<br>
            <em>Środek</em> – teraźniejszość: energie, które cię otaczają<br>
            <em>Prawa</em> – przyszłość: możliwy kierunek lub ostrzeżenie
            </p>
        </div>
        """, unsafe_allow_html=True)

    elif uklad_len == 5:
        st.markdown("""
        <div style="background-color: rgba(193, 71, 233, 0.1); padding: 20px; border-radius: 12px; box-shadow: 0 0 10px #C147E9;">
            <p style="color: #FFD700; font-size: 18px; text-align: center;">
            <strong>Układ 5 Run – Gwiazda Przemian</strong><br>
            1 – przeszłość, 2 – teraźniejszość, 3 – przyszłość<br>
            4 – twoja siła duchowa, 5 – dar lub ostrzeżenie z zewnątrz
            </p>
        </div>
        """, unsafe_allow_html=True)

    elif uklad_len == 8:
        st.markdown("""
        <div style="background-color: rgba(193, 71, 233, 0.1); padding: 20px; border-radius: 12px; box-shadow: 0 0 10px #C147E9;">
            <p style="color: #FFD700; font-size: 18px; text-align: center;">
            <strong>Układ 8 Run – Krąg Życia</strong><br>
            Osiem run tworzy pełen cykl: każdy znak odsłania inny aspekt twojej ścieżki – od narodzin idei po jej transformację.
            </p>
        </div>
        """, unsafe_allow_html=True)

    else:
        st.warning("Nieznany układ run – nie mogę zinterpretować.")

    # Wyświetl kolumny z runami
    st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
    cols = st.columns(uklad_len)

    for i, (col, runa) in enumerate(zip(cols, uklad)):
        with col:
            st.markdown('<div style="display: flex; justify-content: center; align-items: center; flex-direction: column;">', unsafe_allow_html=True)
            odwrocona = runa.pokaz_interaktywny_obraz(losowa_orientacja=True)
            nazwa = runa.get_nazwa_odwrocona() if odwrocona else runa.nazwa
            st.markdown(
                f"<p style='text-align: center; color: {COLORS['accent']}; margin-top: 10px; font-size: 20px;'>{nazwa}</p>",
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)


#?##########################################################################################################
#TODO#######################################################################################################
#?                                                  Krzyż celtycki

def display_celtic_cross(runy: list[RunaPelna]) -> None:
    """Wyświetla układ krzyża celtyckiego."""
    st.markdown(
        f"""
        <h1 style="font-size: 53px; font-weight: bold; text-align: center; color: {COLORS['accent']};">
        Krzyż Celtycki
        </h1>
        """,
        unsafe_allow_html=True,
    )
    if main_image := load_main_images():
        st.image(main_image, use_container_width=True)


    
    if len(runy) < 4:
        st.error("Potrzebujesz co najmniej 4 runy do tego układu!")
        return

    if st.button("Stwórz krzyż celtycki", type="primary"):
        uklad = random.sample(runy, 4)
        display_celtic_cross_layout(uklad)
        display_celtic_interpretation(uklad)


def display_celtic_cross_layout(uklad: list[RunaPelna]) -> None:
    """Wizualizacja układu krzyża celtyckiego."""
    st.header("", divider="rainbow")

    # Górna runa
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
        odwrocona1 = uklad[0].pokaz_interaktywny_obraz(losowa_orientacja=True)
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

    # Środkowy wiersz
    cols = st.columns(3)
    with cols[0]:
        odwrocona2 = uklad[1].pokaz_interaktywny_obraz(losowa_orientacja=True)
    with cols[2]:
        odwrocona3 = uklad[2].pokaz_interaktywny_obraz(losowa_orientacja=True)

    # Dolna runa
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        odwrocona4 = uklad[3].pokaz_interaktywny_obraz(losowa_orientacja=True)
    
    # Zapisz informacje o odwróceniu run w session_state
    st.session_state["odwrocone_runy"] = [odwrocona1, odwrocona2, odwrocona3, odwrocona4]

def display_celtic_interpretation(uklad: list[RunaPelna]) -> None:
    """Wyświetla interpretację układu celtyckiego."""
    st.subheader("", divider="rainbow")

    st.markdown(
        f"""
        <h1 style="font-size: 26px; font-weight: bold; text-align: left; color: {COLORS['accent']};">
        Interpretacja układu - "Krzyż Celtycki"
        </h1>
        """,
        unsafe_allow_html=True,
    )
    
    positions = [
        "Obecna sytuacja",
        "Wyzwania",
        "Przeszłość wpływająca na obecną sytuację",
        "Potencjalna przyszłość"
    ]
    
    # Pobierz informacje o odwróceniu run
    odwrocone_runy = st.session_state.get("odwrocone_runy", [False] * 4)
    
    for i, (runa, position) in enumerate(zip(uklad, positions)):
        with st.expander(f"{position}: {runa.nazwa} {'(odwrócona)' if odwrocone_runy[i] else ''}"):
            if odwrocone_runy[i]:
                st.info("Runa jest odwrócona - interpretuj jako cień znaczenia", icon="⚠️")
            display_rune_details(runa)

def display_rune_descriptions(uklad):
    """Wyświetla opisy wylosowanych run w układzie krzyża celtyckiego."""
    st.markdown("### Opisy run:")
    for i, runa in enumerate(uklad):
        st.subheader(f"Runa {i+1}: {runa.nazwa}")
        st.text(f"Znaczenie: {runa.znaczenie}")
        st.text("Symbolika:")
        for symbol, opis in runa.symbolika.items():
            st.text(f" - {symbol}: {opis}")
        st.text(f"Potencjał: {', '.join(runa.potencjal)}")
        st.markdown("---")


#?##########################################################################################################
#TODO#######################################################################################################

def find_rune_data(runa_nazwa, full_data):
    """Znajdź dane runy w pełnych danych JSON."""
    for runa_data in full_data:
        if runa_data.get("nazwa") == runa_nazwa or runa_nazwa in runa_data.get("nazwa", ""):
            return runa_data
    return None

def load_and_resize_rune_image(runa_obraz_path, size=(200, 200), rotate=False):
    """Ładuje obraz runy, zmienia jego rozmiar i opcjonalnie obraca."""
    try:
        img = Image.open(runa_obraz_path)
        if rotate:
            img = img.rotate(180)
        return img.resize(size)
    except Exception as e:
        st.error(f"Błąd podczas ładowania obrazu runy: {str(e)}")
        return None

def display_centered_image(image, width=None):
    """Wyświetla obraz wyśrodkowany w interfejsie."""
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if width:
            st.image(image, width=width)
        else:
            st.image(image, use_column_width=True)




    # print(f"Załadowano {len(rune_data)} runy.")
    # print(f"Przykładowa runa: {rune_data[0]}")  # Wydrukuj przykładową runę, aby zobaczyć, co zawiera lista
    # runa = random.choice(rune_data)  # rune_data to lista obiektów RunaPelna
    
    # # Przygotowujemy szczegóły do interpretacji
    # interpretacja = runa.interpretacja  # Z 'RunaPelna'
    # znaczenie = runa.znaczenie  # Z 'RunaPelna'
    # krotki_opis = runa.krotki_opis  # Krótkie streszczenie runy
    
    # # Generujemy odpowiedź z uwzględnieniem pytania użytkownika i pełnych danych o runie
    # response = f"""
    # **Wylosowana runa: {runa.nazwa}**
    
    # **Krótkie streszczenie:** {krotki_opis}
    
    # **Znaczenie:** {znaczenie}
    
    # **Interpretacja:** {interpretacja}
    
    # **Pytanie użytkownika:** {user_input}
    # """

    # return response




# def interpret_rune_with_question(user_input, runes, rune_data):
#     """Losuje runę i interpretuje ją w kontekście pytania użytkownika"""
#     runa = random.choice(RunaPelna)
#     jest_odwrocona = runa.pokaz_obraz_dnia(losowa_orientacja=True)
#     nazwa_runy = runa.get_nazwa_odwrocona() if jest_odwrocona else runa.nazwa

#     # Szukanie danych z JSON-a
#     dane_runy = next((r for r in rune_data if r.get("nazwa") == runa.nazwa), None)
#     znaczenie = dane_runy.get("znaczenie", "brak danych") if dane_runy else "brak danych"
    
#     # Budowanie promptu
#     cień_info = "Runa jest odwrócona – interpretuj jako cień znaczenia." if jest_odwrocona else ""
#     prompt = f"""
#     Jesteś Volvą, nordycką wieszczką. Udziel odpowiedzi w stylu mistycznym i refleksyjnym.
    
#     Użytkownik zadał pytanie: {user_input}
#     Wylosowana runa: {nazwa_runy}
#     Znaczenie tej runy to: {znaczenie}
#     {cień_info}

#     Na podstawie powyższego, udziel odpowiedzi zgodnie z duchem prastarej mądrości run.
    
#     Format:
#     ---
#     🌲 *{nazwa_runy}*  
#     **Znaczenie dla intencji:** ...  
#     **Ostrzeżenie:** ...  
#     **Rytuał:** ...  
#     ---
#     """

#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": prompt}],
#         temperature=0.85,
#         max_tokens=500
#     )

#     return response['choices'][0]['message']['content'].strip()
