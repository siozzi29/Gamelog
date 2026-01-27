from pyDatalog import pyDatalog
import data_loader

# Definiamo i termini globalmente
pyDatalog.create_terms('is_genre, is_success, X')

def setup_logic():
    pyDatalog.clear()
    df = data_loader.get_clean_data()
    if df is None: return

    for index, row in df.head(500).iterrows():
        gioco = row['name']
        for g in row['genres_list']:
            pyDatalog.assert_fact('is_genre', gioco, g)
        if row['is_success'] == 1:
            pyDatalog.assert_fact('is_success', gioco)

def query_custom_genre(genere_utente):
    # Trasformiamo l'input dell'utente in minuscolo per il confronto
    genere_cercato = genere_utente.lower()
    return is_genre(X, genere_cercato) & is_success(X)