import streamlit as st

# Usa la cache per inizializzare le variabili globali
@st.cache_data
def init_credentials():
    return {"id": None, "secret": None}

# Inizializza le variabili globali con i dati della cache
credentials = init_credentials()

def run_login():
    global credentials  # Usa le credenziali globali

    # Titolo e logo Spotify
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("spotify_logo.png", width=100)
    with col2:
        st.title("Spotify Wrapped Statistico")

    # Input per Client ID e Client Secret
    id_input = st.text_input(
        "Client ID",
        value=credentials["id"] or "",
        placeholder="Inserisci il tuo client_id"
    )
    secret_input = st.text_input(
        "Client Secret",
        type="password",
        value=credentials["secret"] or "",
        placeholder="Inserisci il tuo client_secret"
    )

    # Aggiorna le credenziali globali
    if id_input:
        credentials["id"] = id_input
    if secret_input:
        credentials["secret"] = secret_input

    # Visualizza le credenziali (solo per debug)
    st.write(f"Client ID: {credentials['id']}")
    st.write(f"Client Secret: {credentials['secret']}")

# Esegui la funzione di login
run_login()
