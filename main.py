import pandas as pd
from pyDatalog import pyDatalog

# 1. Caricamento dati
df = pd.read_csv('data/steam.csv')

# 2. Definizione termini logici
# is_genre(Gioco, Genere), has_category(Gioco, Categoria), competitive_core(Gioco)
pyDatalog.create_terms('is_genre, has_category, competitive_core, X, Y')

print("--- Popolamento Knowledge Base ---")

# Carichiamo i primi 50 giochi per avere più varietà
for index, row in df.head(50).iterrows():
    gioco = row['name']
    
    # Aggiungiamo i generi
    for g in row['genres'].split(';'):
        + is_genre(gioco, g)
    
    # Aggiungiamo le categorie (es. Multi-player, Single-player)
    for c in row['categories'].split(';'):
        + has_category(gioco, c)

# 3. DEFINIZIONE DELLA REGOLA (Ragionamento)
# Un gioco X è competitive_core se è Action E è Multi-player
competitive_core(X) <= is_genre(X, 'Action') & has_category(X, 'Multi-player')

# 4. QUERY
print("\n--- Risultati del Ragionamento ---")
risultati = competitive_core(X)
print(f"Giochi identificati come 'Competitive-Core':\n{risultati}")