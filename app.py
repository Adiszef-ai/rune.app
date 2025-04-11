#?##########################################################################################################
#TODO app.py" - główny plik uruchamiający aplikację
#?##########################################################################################################

import os
from PIL import Image
import streamlit as st
from styles import load_css
from supp import create_runes_list
from volva import display_volva
from constants import COLORS
from features import (
    display_browse_runes,
    display_rune_of_the_day,
    display_rune_layout,
    display_celtic_cross,
)


st.set_page_config(page_title="Rune Witch", page_icon="🔮")

#?##########################################################################################################
#TODO#######################################################################################################

def get_rune_image(rune_name):
    """Get the path to a rune image."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, "data", "img_rune", f"{rune_name.lower()}.jpg")
    return image_path

def display_rune_image(rune_name):
    """Display a rune image in Streamlit."""
    image_path = get_rune_image(rune_name)
    if os.path.exists(image_path):
        image = Image.open(image_path)
        st.image(image, caption=f"Rune: {rune_name}", use_column_width=True)
    else:
        st.warning(f"Image not found for rune: {rune_name}")

def main():

    # Wczytaj style
    load_css()

    # Utwórz listę run
    runy = create_runes_list()

    # Utwórz menu w panelu bocznym
    st.sidebar.title("Rune Witch")
    opcja = st.sidebar.selectbox(
        "Wybierz opcję", 
        ["Przeglądaj runy", "Runa dnia", "Krzyż celtycki", "Rozkłady Runiczne", "Völva"]
    )

    # Wywołanie funkcji przeglądania run
    if opcja == "Przeglądaj runy":
        display_browse_runes(runy)

    # Wywołanie funkcji losującej runę
    elif opcja == "Runa dnia":
        display_rune_of_the_day(runy)

    elif opcja == "Krzyż celtycki":
        display_celtic_cross(runy)

    # Wywołanie funkcji układu run
    elif opcja == "Rozkłady Runiczne":
        display_rune_layout(runy)

    elif opcja == "Völva":
        display_volva()  
        
if __name__ == "__main__":
    main()


# st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)
