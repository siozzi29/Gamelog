# Gamelog: VideoGame Intellect & Discovery
## Documentazione Tecnica di Progetto

**Studente:** Simone Iozzi
**Matricola:** 796970
**Corso:** Ingegneria della Conoscenza
**Anno Accademico:** 2025/2026

---

## Indice dei Contenuti

1.  [Capitolo 0: Introduzione](#capitolo-0-introduzione)
2.  [Capitolo 1: Il Dataset e Preprocessing](#capitolo-1-il-dataset-e-preprocessing)
3.  [Capitolo 2: Rappresentazione della Conoscenza (Logica)](#capitolo-2-rappresentazione-della-conoscenza-logica)
4.  [Capitolo 3: Ragionamento in Condizioni di Incertezza (Bayes)](#capitolo-3-ragionamento-in-condizioni-di-incertezza-bayes)
5.  [Capitolo 4: Soddisfacimento di Vincoli (CSP)](#capitolo-4-soddisfacimento-di-vincoli-csp)
6.  [Capitolo 5: Architettura del Sistema e Testing](#capitolo-5-architettura-del-sistema-e-testing)
7.  [Sviluppi Futuri](#sviluppi-futuri)
8.  [Riferimenti Bibliografici](#riferimenti-bibliografici)

---

## Capitolo 0) Introduzione

### Obiettivo del Progetto
L'obiettivo di **Gamelog** è la realizzazione di un Sistema Basato sulla Conoscenza (Knowledge-Based System) in grado di assistere un utente nel dominio videoludico. Il sistema non si limita a un semplice filtraggio di dati, ma integra tre diversi paradigmi dell'Intelligenza Artificiale per offrire una consulenza completa:
1.  **Analisi Logica:** Individuazione deduttiva di titoli validi basata su fatti certi.
2.  **Analisi Probabilistica:** Stima del successo di un genere basata sui trend storici di mercato.
3.  **Ottimizzazione Hardware:** Configurazione automatica di un PC da gaming rispettando vincoli di budget.

### Requisiti Funzionali
Il sistema deve essere in grado di:
* Caricare e pulire un dataset reale di videogiochi (Steam Store Games).
* Costruire una Knowledge Base dinamica per interrogazioni logiche.
* Apprendere dai dati le probabilità condizionate tra Genere e Successo.
* Risolvere problemi di soddisfacimento vincoli (CSP) per l'hardware.
* Interagire con l'utente tramite un'interfaccia a riga di comando (CLI) robusta (case-insensitive).

### Stack Tecnologico
Il progetto è stato sviluppato in **Python 3.13**, scelto per la sua vasta disponibilità di librerie per l'AI simbolica e statistica.

* **IDE:** Visual Studio Code
* **Librerie Utilizzate:**
    * `pandas`: Manipolazione e pulizia del dataset CSV.
    * `pyDatalog`: Motore di inferenza logica (Programmazione Logica in Python).
    * `pgmpy`: Costruzione e inferenza su Reti Bayesiane.
    * `python-constraint`: Risolutore per problemi CSP.
    * `scikit-learn`: Utilizzato per il `LabelEncoder` nella fase di preprocessing numerico.

---

## Capitolo 1) Il Dataset e Preprocessing

### Origine dei Dati
Il dataset utilizzato è `steam.csv`, contenente informazioni su circa 27.000 videogiochi pubblicati sulla piattaforma Steam. Le colonne principali di interesse sono:
* `name`: Titolo del gioco.
* `genres`: Lista dei generi (separati da punto e virgola).
* `positive_ratings`: Numero di recensioni positive.
* `negative_ratings`: Numero di recensioni negative.

### Pipeline di Preprocessing (`data_loader.py`)
Prima di essere utilizzati dai moduli di IA, i dati grezzi subiscono un processo di pulizia e trasformazione fondamentale per garantire la qualità del ragionamento.

1.  **Pulizia Valori Nulli:** Rimozione delle righe con dati mancanti nei campi essenziali (`name`, `genres`).
2.  **Normalizzazione del Testo:** Conversione di tutte le stringhe di genere in minuscolo (lowercase) per garantire una ricerca *case-insensitive* e robusta.
3.  **Feature Engineering (La metrica di successo):**
    Poiché il dataset non contiene un'etichetta esplicita "Successo", questa è stata derivata sinteticamente calcolando il *ratio* delle recensioni.

    $$\text{Success Rate} = \frac{\text{Positive Ratings}}{\text{Positive Ratings} + \text{Negative Ratings}}$$

    È stata applicata una soglia di discretizzazione:
    * Se `Success Rate` $\ge 0.8$ (80%) $\rightarrow$ `is_success = 1`
    * Altrimenti $\rightarrow$ `is_success = 0`

| Name | Genres (Raw) | Genres (Processed) | Positive | Negative | is_success |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Counter-Strike | Action | ['action'] | 124534 | 3339 | **1** |
| Bad Rats | Puzzle | ['puzzle'] | 400 | 9000 | **0** |

---

## Capitolo 2) Rappresentazione della Conoscenza (Logica)

### Teoria di Riferimento
Questo modulo si basa sulla **Logica del Primo Ordine** (FOL). Utilizzando il paradigma della programmazione logica, il sistema definisce relazioni tra oggetti e permette di derivare nuova conoscenza attraverso regole di inferenza.

### Implementazione (`logic_engine.py`)
È stata utilizzata la libreria `pyDatalog` per definire fatti e termini logici direttamente in Python.

#### 1. Definizione dei Termini
Sono stati creati i predicati atomici:
* `is_genre(Gioco, Genere)`: Asserisce che un gioco appartiene a un genere.
* `is_success(Gioco)`: Asserisce che un gioco è considerato un successo.

#### 2. Popolamento della Knowledge Base (KB)
Il sistema itera sul dataset pulito e asserisce i fatti dinamicamente. A differenza di un database SQL classico, qui stiamo costruendo una base di verità logiche.

```python
# Snippet di caricamento fatti
for index, row in df.iterrows():
    pyDatalog.assert_fact('is_genre', row['name'], row['genre'])
    if row['is_success'] == 1:
        pyDatalog.assert_fact('is_success', row['name'])