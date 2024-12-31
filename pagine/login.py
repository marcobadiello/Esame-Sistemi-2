import streamlit as st


def run_login():
    # Titolo e logo Spotify
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("spotify_logo.png", width=100)
    with col2:
        st.title("Spotify Wrapped Statistico")

    # Input per Client ID e Client Secret
    id = st.text_input("Client ID", placeholder="Inserisci il tuo client_id")
    secret = st.text_input("Client Secret", type="password", placeholder="Inserisci il tuo client_secret")

    # Bottone per salvare le credenziali
    if st.button("Salva Credenziali"):
        if id and secret:
            salva_credenziali(id, secret)
            st.success("Credenziali salvate correttamente in credenziali.txt!")
        else:
            st.error("Inserisci entrambe le credenziali prima di salvare.")


def salva_credenziali(client_id, client_secret):
    """
    Salva le credenziali in un file di testo.
    """
    with open("credenziali.txt", "w") as file:
        file.write(f"{client_id}\n")
        file.write(f"{client_secret}\n")
        file.write('http://localhost:8888/callback')
