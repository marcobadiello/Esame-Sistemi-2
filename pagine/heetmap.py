import streamlit as st
from datetime import datetime
import Tools
from Estrattore import df

def run_heetmap():
    """
    Visualizza una heatmap di Spotify Wrapped per un anno selezionato.

    Questa funzione crea un layout Streamlit con due colonne: una per il logo di Spotify e l'altra per il titolo "Spotify Wrapped Statistico". Successivamente, visualizza un selectbox per permettere all'utente di scegliere un anno degli ultimi 10 anni. In base all'anno selezionato, genera e mostra una heatmap che evidenzia i periodi di alta e bassa attività di ascolto, oltre a eventuali picchi nel corso dell'anno.

    La funzione include anche un footer con il nome del creatore.

    Nota:
    - La funzione presuppone che la data e l'ora correnti siano disponibili.
    - La funzione utilizza il metodo `Tools.stampa_heetmap` per generare la heatmap.
    - La funzione richiede i moduli `st` (Streamlit) e `datetime`.

    Args:
        Nessun argomento.

    Returns:
        Nessun valore (None).
    """
    # impostazioni della pagina
    st.set_page_config(
    layout="wide",  
    initial_sidebar_state="collapsed"  #"expanded" o "collapsed"
    )
    # Layout della pagina con colonne
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("spotify_logo.png", width=100)
    with col2:
        st.title("Spotify Wrapped Statistico")
    
    # Data corrente e anno
    oggi = datetime.now().date()
    anno_corrente = oggi.year
    
    # Lista degli anni (ultimi 10 anni)
    lista_anni = [i for i in range(anno_corrente, anno_corrente - 11, -1)]
    
    # Trova l'indice dell'anno precedente
    indice_anno_precedente = lista_anni.index(anno_corrente - 1)
    
    # Selectbox per scegliere l'anno
    anno_selezionato = st.selectbox(
        "Seleziona un anno",
        lista_anni,
        index=indice_anno_precedente
    )
    
    # Richiamo della funzione per stampare la heatmap
    xx = f'''
    In questo grafico è riporatata la HeetMap dell'anno {anno_selezionato} utilie per vedere periodo di forte ascolto o periodi di bassi ascolti.
    Inoltre è possibile vedere la loro distribuzione durante l'anno e l'idenificazione di eventulai picchi. 
    '''
    st.write(xx)
    Tools.stampa_heetmap(df, anno_selezionato)
    # Footer
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