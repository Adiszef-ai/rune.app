import streamlit as st

def load_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=MedievalSharp&display=swap');
@import url('https://fonts.googleapis.com/css2?family=UnifrakturMaguntia&display=swap');

/* Global background and font smoothing */
html, body {
    background: linear-gradient(135deg, #1E1E2E, #3E2F47);
    color: white;
    font-family: 'Cinzel', 'MedievalSharp', 'UnifrakturMaguntia', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    scroll-behavior: smooth;
    -webkit-font-smoothing: antialiased;
}

/* Main image styling */
img {
    border-radius: 20px;
    border: 5px solid #AA0061;
    box-shadow: 0 0 20px rgba(193, 71, 233, 0.4);
}

/* Rune interactive container styling */
.runa-container {
    position: relative;
    display: inline-block;
    cursor: pointer;
    transition: transform 0.8s ease-in-out, opacity 0.8s ease-in-out;
}
.runa-img {
    border: 5px solid transparent;
    border-radius: 12px;
    box-shadow: 0 0 15px rgba(255, 105, 180, 0.5);
    transition: border-color 0.5s ease-in-out, box-shadow 0.5s ease-in-out;
}
.runa-container:hover .runa-img {
    border-color: #FFD700;
    box-shadow: 0 0 25px rgba(255, 215, 0, 0.8);
}

/* Button styling */
div.stButton > button {
    font-size: 50px !important;
    background: linear-gradient(145deg, #5E2B97, #C147E9);
    color: white;
    border-radius: 15px;
    height: 50px;
    min-width: 140px;
    padding: 0 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    box-shadow: 0 0 20px rgba(193, 71, 233, 0.6);
    border: 2px solid #AA0061;
    transition: all 0.4s ease;
    white-space: nowrap;
}
div.stButton > button:hover {
    background: linear-gradient(145deg, #FFD700, #C147E9);
    color: #5E2B97;
    box-shadow: 0 0 30px rgba(255, 215, 0, 0.8);
}
div.stButton > button:active {
    background: linear-gradient(145deg, #931049, #e35995);
    color: white;
    box-shadow: inset 0 0 10px rgba(255, 255, 255, 0.3);
}

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(to bottom, #1e1e2e, #3e2f47);
    color: #FFFFFF;
    box-shadow: inset 0 0 10px rgba(170, 0, 97, 0.4);
}
[data-testid="stSidebar"] h1 {
    color: #C147E9;
    text-shadow: 0 0 6px rgba(193, 71, 233, 0.6);
    font-size: 35px !important;
}
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #C147E9;
    text-shadow: 0 0 6px rgba(193, 71, 233, 0.6);
}
[data-testid="stSidebar"] p {
    font-size: 18px;
    line-height: 1.6;
}
[data-testid="stSidebar"] a:hover {
    color: #FFD700;
    text-decoration: underline;
}

/* Input styling */
input, textarea {
    background-color: #2A2A3D;
    color: #FFFFFF;
    border: 1px solid #C147E9;
    box-shadow: 0 0 10px rgba(193, 71, 233, 0.2);
    padding: 8px;
    border-radius: 8px;
}

/* Primary buttons elsewhere */
button[kind="primary"] {
    background: linear-gradient(145deg, #5E2B97, #AA0061);
    color: white;
    border: 1px solid #AA0061;
}
button[kind="primary"]:hover {
    background: linear-gradient(145deg, #FFD700, #931049);
    color: #29293D;
}

/* Scrollbar for mystical feel */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: #C147E9;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #FFD700;
}

/* Glow headers and text for consistency */
h1, h2, h3, h4, h5, h6, p, span, label {
    text-shadow: 0 0 5px rgba(255, 255, 255, 0.1);
    font-family: 'Cinzel', 'MedievalSharp', 'UnifrakturMaguntia', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

}
</style>
    """, unsafe_allow_html=True)


