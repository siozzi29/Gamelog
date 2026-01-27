import sys
import os
# Aggiunge la cartella superiore al percorso di ricerca di Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import data_loader
import bayesian_learner
import pandas as pd

print("--- TEST FASE 1: Caricamento e Pulizia ---")
df = data_loader.get_clean_data()
if df is not None:
    print(f"✅ Successo! Dataset caricato.")
    print(f"Esempio di metrica successo (is_success) per i primi 3 giochi:")
    print(df[['name', 'is_success']].head(3))
else:
    print("❌ Errore nel caricamento dei dati.")

print("\n--- TEST FASE 2: Apprendimento Bayesiano ---")
try:
    # Testiamo la predizione per il genere 'Action'
    # Il modello leggerà il CSV e calcolerà la probabilità reale
    risultato = bayesian_learner.predict_success('Action')
    print("✅ Il modello ha imparato dai dati!")
    print("Probabilità di successo per un gioco 'Action' basata sul dataset:")
    print(risultato)
except Exception as e:
    print(f"❌ Errore nell'apprendimento: {e}")