import argparse
import data_loader
import bayesian_learner
import logic_engine
import hardware_optimizer

def main():
    parser = argparse.ArgumentParser(description="GAMELOG - Sistema di Supporto alle Decisioni")
    parser.add_argument("--cross-validate", action="store_true", help="Esegue K-Fold CV sulla rete bayesiana")
    parser.add_argument("--k", type=int, default=5, choices=[5, 10], help="Numero di fold (5 o 10)")
    args = parser.parse_args()

    if args.cross_validate:
        print("--- K-Fold Cross-Validation (Rete Bayesiana) ---")
        bayesian_learner.cross_validate_bayesian_network(k=args.k)
        return

    print("="*30)
    print(" GAMELOG - STARTUP ")
    print("="*30)

    # 1. Caricamento Iniziale
    print("\n[1/3] Inizializzazione Knowledge Base...")
    logic_engine.setup_logic()
    
    # 2. Input Utente
    genere = input("\nInserisci un genere di gioco (es. Action, Indie, RPG): ").strip()
    budget = float(input("Inserisci il tuo budget per l'hardware (€): "))

    print("\n" + "="*30)
    print(f" ANALISI PER IL GENERE: {genere} ")
    print("="*30)

    # 3. Ragionamento Probabilistico (Incertezza)
    print("\n--- Previsione Successo (Rete Bayesiana) ---")
    prob = bayesian_learner.predict_success(genere)
    print(prob)

    # 4. Ragionamento Deduttivo (Logica)
    print(f"\n--- Titoli Consigliati (Knowledge Base) ---")
    successi_logici = logic_engine.query_custom_genre(genere)
    if successi_logici:
        # Estraiamo i primi 5 nomi dai risultati della query
        nomi = [r[0] for r in successi_logici[:5]]
        print(f"Ecco 5 titoli di successo nel mercato {genere}:")
        for n in nomi:
            print(f" - {n}")
    else:
        print(f"⚠️ Nessun titolo trovato per il genere '{genere}'.")

    # 5. Ottimizzazione (Vincoli)
    print(f"\n--- Ottimizzazione Hardware (CSP) ---")
    configurazioni = hardware_optimizer.find_hardware_configs(budget)
    if configurazioni:
        print(f"Con {budget}€ puoi acquistare:")
        for c in configurazioni[:3]: # Mostriamo le prime 3
            print(f" ✅ {c}")
    else:
        print("⚠️ Nessuna configurazione trovata per questo budget.")

    print("\n" + "="*30)
    print(" FINE ANALISI ")
    print("="*30)

if __name__ == "__main__":
    main()