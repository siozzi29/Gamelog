# Gamelog: VideoGame Intellect & Discovery

Progetto individuale per l'esame di **Ingegneria della Conoscenza (ICon)** - Università degli Studi di Bari Aldo Moro.

## Gruppo di lavoro
* **Studente:** Simone Iozzi
* **Matricola:** 796970
* **Email:** s.iozzi@studenti.uniba.it
* **Anno Accademico:** 2025/2026

---

## Descrizione del Progetto
**Gamelog** è un Knowledge-Based System (KBS) progettato per l'analisi e l'ottimizzazione nel dominio videoludico. Il sistema integra tre moduli principali che coprono diverse aree del programma:

1.  **Rappresentazione Relazionale (Cap. 15-16):** Modellazione logica per la classificazione semantica dei generi e delle meccaniche di gioco.
2.  **Ragionamento con Incertezza (Cap. 9-10):** Rete Bayesiana per stimare la probabilità di successo di un titolo in base a variabili stocastiche.
3.  **Ragionamento con Vincoli (Cap. 4):** Risoluzione di un CSP (Constraint Satisfaction Problem) per l'ottimizzazione di setup hardware per il gaming.

## Struttura della Repository
* `📁 data/`: Dataset e file della Knowledge Base.
* `📁 src/`: Codice sorgente (Python/Prolog).
* `📁 doc/`: Documentazione ufficiale (Template Word/PDF).
* `📁 img/`: file immagini.

---

# STEAM AI ADVISOR
### Sistema Intelligente di Raccomandazione Videogiochi e Hardware

Un'applicazione Python che combina **logica deduttiva**, **ragionamento probabilistico** e **ottimizzazione con vincoli** per consigliare i migliori videogiochi e configurazioni hardware in base al genere e al budget dell'utente.

---

## Caratteristiche Principali

✅ **Knowledge Base** - Ragionamento deduttivo su generi di giochi  
✅ **Rete Bayesiana** - Previsione di successo commerciale con incertezza  
✅ **CSP Solver** - Ottimizzazione hardware rispetto al budget  
✅ **Dataset Steam** - Analisi di migliaia di titoli e loro caratteristiche  

---

## Prerequisiti

- **Python 3.13+**
- pip (gestore pacchetti Python)

---

## Setup Iniziale

### 1. Clonare il repository
```bash
git clone https://github.com/username/steam-ai-advisor.git
cd steam-ai-advisor
```

### 2. Installare le dipendenze
```bash
pip install -r requirements.txt
```

Le dipendenze richieste sono:
- **pandas** - Manipolazione dati
- **pgmpy** - Modelli grafici probabilistici (Reti Bayesiane)
- **pyDatalog** - Logica deduttiva
- **python-constraint** - Constraint Satisfaction Problem (CSP)
- **scikit-learn** - Machine Learning utilities

---

## Utilizzo

### Avvio Principale
Dalla directory del progetto, esegui:

```bash
python main.py
```

**Quello che succede:**
1. **Inizializzazione Knowledge Base** - Carica le regole su generi e giochi
2. **Input Utente** - Ti chiede:
   - Genere preferito (es. Action, Indie, RPG, Strategy, etc.)
   - Budget per hardware (in €)
3. **Previsione Successo** - Usa una Rete Bayesiana per stimare il successo commerciale del genere
4. **Raccomandazioni** - Restituisce i 5 titoli più di successo per quel genere
5. **Configurazioni Hardware** - Suggerisce le migliori configurazioni PC entro il budget

**Esempio di interazione:**
```
==============================
 STEAM AI ADVISOR - STARTUP 
==============================

[1/3] Inizializzazione Knowledge Base...

Inserisci un genere di gioco (es. Action, Indie, RPG): Action
Inserisci il tuo budget per l'hardware (€): 800

==============================
 ANALISI PER IL GENERE: Action 
==============================

--- Previsione Successo (Rete Bayesiana) ---
[Risultati della Rete Bayesiana...]

--- Titoli Consigliati (Knowledge Base) ---
Ecco 5 titoli di successo nel mercato Action:
 - Call of Duty: Modern Warfare
 - Counter-Strike 2
 - ...

--- Ottimizzazione Hardware (CSP) ---
Con 800€ puoi acquistare:
 ✅ RTX 4060 Ti + Ryzen 5 7600X + 16GB RAM
 ✅ RTX 4070 + Ryzen 5 5600X + 16GB RAM
 ...
```

---

## Struttura del Progetto

```
├── main.py                      # Entry point dell'applicazione
├── logic_engine.py              # Knowledge Base (Logica Deduttiva)
├── bayesian_learner.py          # Rete Bayesiana (Ragionamento Probabilistico)
├── hardware_optimizer.py        # CSP Solver (Ottimizzazione Hardware)
├── hardware_csp.py              # Definizioni Constraint
├── data_loader.py               # Caricamento dataset Steam
├── probabilita.py               # Utilità probabilistiche
├── requirements.txt             # Dipendenze Python
├── data/
│   ├── steam.csv                # Dataset principale Steam
│   └── steam_description_data.csv # Descrizioni dettagliate
└── tests/
    ├── test_architettura.py     # Test architettura
    └── test_prob.py             # Test probabilità
```

---

## Componenti Principali

### 🧠 Logic Engine (logic_engine.py)
Implementa la **logica deduttiva** usando pyDatalog:
- Crea una Knowledge Base su generi e titoli di successo
- Supporta query su generi personalizzati
- Ragionamento basato su regole

### 📊 Bayesian Learner (bayesian_learner.py)
Implementa una **Rete Bayesiana** usando pgmpy:
- Stima la probabilità di successo di un genere
- Gestisce variabili e dipendenze probabilistiche
- Fornisce distribuzioni di probabilità

### ⚙️ Hardware Optimizer (hardware_optimizer.py)
Risolve un **Constraint Satisfaction Problem**:
- Trova configurazioni hardware entro il budget
- Considera CPU, GPU, RAM e altri componenti
- Utilizza il solver python-constraint

### 📈 Data Loader (data_loader.py)
Carica e processa i dati:
- Legge steam.csv e steam_description_data.csv
- Estrae informazioni sui generi
- Prepara dati per Knowledge Base e Reti Bayesiane

---

## Esecuzione dei Test

Per eseguire i test unitari:

```bash
python -m pytest tests/test_architettura.py -v
python -m pytest tests/test_prob.py -v
```

---

## Flusso di Ragionamento

```
INPUT UTENTE (Genere + Budget)
        ↓
    ┌───┴───┐
    ↓       ↓
LOGICA  PROBABILITÀ  
(KB)    (Rete Bay.)
    ↓       ↓
    └───┬───┘
        ↓
  TITOLI CONSIGLIATI
        ↓
   ┌────┴────┐
   ↓         ↓
 CSP      OUTPUT
(Hardware) FINALE
```

---

## Estensioni Possibili

- [ ] Aggiungere filtri per rating utenti
- [ ] Integrare API Steam per dati real-time
- [ ] Interfaccia Web con Flask/FastAPI
- [ ] Machine Learning per predizioni di successo
- [ ] Analisi sentiment dalle recensioni

---

## Dipendenze e Versioni

```
pandas >= 1.0
pgmpy >= 1.10
pyDatalog >= 0.16
python-constraint >= 1.4.0
scikit-learn >= 1.0
```

---

## Troubleshooting

**Problema:** "ModuleNotFoundError: No module named 'pgmpy'"  
**Soluzione:** Esegui `pip install pgmpy`

**Problema:** "Nessun titolo trovato per il genere"  
**Soluzione:** Verifica che i file CSV siano nella cartella `/data`

**Problema:** "Nessuna configurazione trovata per questo budget"  
**Soluzione:** Aumenta il budget, il CSP potrebbe avere vincoli troppo stringenti

---

## Autori

Sviluppato come progetto di **Ingegneria della Conoscenza**

---

## Licenza

MIT License
