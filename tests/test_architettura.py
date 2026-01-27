import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import data_loader
import bayesian_learner
import logic_engine
import hardware_optimizer

print("--- TEST FASE 1: Dati ---")
df = data_loader.get_clean_data()
print("✅ Dataset OK")

print("\n--- TEST FASE 2: Probabilità ---")
print(bayesian_learner.predict_success('Action'))
print("✅ Fase 2 completata")

print("\n--- TEST FASE 3: Logica ---")
logic_engine.setup_logic()
risultati = logic_engine.query_action_hits()
# risultati è una lista di tuple, es: [('Counter-Strike',), ('Portal',)]
if risultati:
    print(f"✅ Query Logica OK. Trovati {len(risultati)} giochi.")
    # Estraiamo i primi 3 nomi per vederli puliti
    nomi_puliti = [r[0] for r in risultati[:3]]
    print(f"Esempi: {nomi_puliti}")
else:
    print("⚠️ Nessun gioco trovato con questi criteri.")

print("\n--- TEST FASE 4: Vincoli (CSP) ---")
print("Sto calcolando le configurazioni hardware...")
configs = hardware_optimizer.find_hardware_configs(500)
print(f"✅ CSP OK. Trovate {len(configs)} soluzioni.")