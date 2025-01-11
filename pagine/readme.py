import streamlit as st

def run_readme():
    """
    Legge il contenuto di un file 'README.md' e lo visualizza utilizzando la funzione markdown di Streamlit.  
    Inoltre, aggiunge un footer fisso nella parte inferiore della pagina con un messaggio personalizzato.

    Il footer è stilizzato utilizzando CSS inline e include il nome del creatore.

    Nota:
    - La funzione presuppone che il file 'README.md' si trovi nella stessa directory dello script.
    - Streamlit (`st`) deve essere importato e inizializzato nello script in cui viene utilizzata questa funzione.

    Eccezioni sollevate:
    - `FileNotFoundError`: Se il file 'README.md' non esiste nel percorso specificato.
    - `UnicodeDecodeError`: Se si verifica un errore nella decodifica del contenuto del file.
    """

    with open('README.md', 'r', encoding='utf-8') as file:
        data = file.read()
    st.markdown(data)
    st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #f5f5f5;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        color: #333;
        border-top: 1px solid #ddd;
    }
    </style>
    <div class="footer">
    Creato con ❤️ da <b>Marco Badiello</b>
    </div>
    """,
    unsafe_allow_html=True
)