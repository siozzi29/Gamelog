import pandas as pd
import os

def get_clean_data():
    try:
        # Trova la cartella dove si trova questo file (data_loader.py)
        base_path = os.path.dirname(os.path.abspath(__file__))
        # Costruisce il percorso corretto verso data/steam.csv
        csv_path = os.path.join(base_path, 'data', 'steam.csv')
        
        df = pd.read_csv(csv_path)
        
        # Pulizia base
        df = df.dropna(subset=['name', 'genres', 'categories'])
        
        # Trasformiamo le stringhe in liste
        df['genres_list'] = df['genres'].apply(lambda x: x.split(';'))
        df['genres_list'] = df['genres_list'].apply(lambda lista: [g.lower() for g in lista])
        df['cat_list'] = df['categories'].apply(lambda x: x.split(';'))
        
        # Metrica di successo
        df['success_rate'] = df['positive_ratings'] / (df['positive_ratings'] + df['negative_ratings'])
        df['is_success'] = df['success_rate'].apply(lambda x: 1 if x >= 0.8 else 0)
        
        return df
    except Exception as e:
        print(f"Errore nel caricamento dati: {e}")
        return None