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
* `📁 notebooks/`: Sperimentazione e valutazione statistica.

---

# Gamelog Project
### Panoramica del Progetto
Sviluppato da: Simone Iozzi

## Setup iniziale dell'ambiente di lavoro:
**- Cloning**  
Per eseguire il progetto, prima clona il repository eseguendo il seguente comando:  
```
git clone <your-repository-url>
```
Il progetto è stato sviluppato interamente in Python versione **3.13**. Pertanto, Python è richiesto.

**- Requirements**  
Dopo aver installato Python, installa le dipendenze necessarie per il progetto eseguendo il comando:  
```
pip install -r requirements.txt
```
Questo installerà automaticamente tutte le dipendenze elencate nel file `requirements.txt`, garantendo il corretto funzionamento del progetto.

## Esecuzione
Dalla riga di comando, navigare nella directory del progetto ed eseguire i seguenti comandi:

```
python main.py eda --grafici
```
Questo comando esegue l'analisi esplorativa del dataset: statistiche, valori mancanti, distribuzione del target; con `--grafici` mostra anche istogrammi e matrice di correlazione.

```
python main.py kb
```
Questo comando crea la Knowledge Base mappando le feature vocali a nomi canonici, imposta soglie (affinate dai dati) e salva le regole in `knowledge_base.json`.

```
python main.py train
```
Questo comando addestra il modello Random Forest, calibra le probabilità, trova le soglie ottimali (F1 di default) oppure inserisci `--thr youden`, valuta sul test e salva tutto in `parkinson_model.joblib`.

```
python main.py random_patient
```
Effettuabile solamente dopo aver eseguito il train. Il comando genera automaticamente un file JSON con dati di un paziente generati in modo casuale ma plausibile, per testare il modello senza dover inserire manualmente tutti i valori.

```
python main.py predict --json paziente_random.json --thr youden
```
Effettuabile solamente dopo aver eseguito il train. Usa il modello salvato per predire lo stato di un paziente da file JSON; permette di scegliere la soglia (F1, Youden, o fixed).

```
python main.py reason --json paziente_random.json
```
Effettuabile solamente dopo aver eseguito il train. Applica le regole KB e calcola gli score fuzzy per un paziente da JSON.

```
python main.py all-in-one --csv dataset.csv --json paziente_random.json --model parkinson_model.joblib --thr youden --out report.html
```
Questo comando, effettuabile solo dopo aver eseguito il train e il predict, effettua una valutazione completa del rischio di Parkinson per un paziente: carica il dataset, il modello e i dati clinici, calcola la probabilità e la diagnosi usando la soglia di Youden, stima il rischio fuzzy e genera un report HTML con risultati e spiegazioni.

```
python main.py runs --repeats 1 --splits 5 --method sigmoid --n_estimators 200 --grid_points 101 --outdir results --csv cv_runs.csv --json cv_runs.json
```
