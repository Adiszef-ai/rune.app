#?##########################################################################################################
#TODO app.py" - główny plik uruchamiający aplikację
#?##########################################################################################################

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
        st.caption('„Wieszczka runiczna jeszcze nie jest gotowa..."')
        display_celtic_cross(runy)

    # Wywołanie funkcji układu run
    elif opcja == "Rozkłady Runiczne":
        st.caption('"Gdy nadejdzie Ragnarok, to te runy będą miały znaczenie"')
        display_rune_layout(runy)

    elif opcja == "Völva":
        display_volva()  
        
if __name__ == "__main__":
    main()


# st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True)