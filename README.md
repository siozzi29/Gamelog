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
### Project Overview
Developed by: [Your Name(s)]

## Initial Setup of the Working Environment:
**- Cloning**  
To execute the project, first clone the repository by running the following command:  
```
git clone <your-repository-url>
```
The project is developed entirely in Python version **3.13**. Therefore, Python is required.

**- Requirements**  
After installing Python, install the necessary dependencies for the project by executing the command:  
```
pip install -r requirements.txt
```
This will automatically install all dependencies listed in the `requirements.txt` file, ensuring the correct functioning of the project.

## Execution
Within the command line, navigate to the project directory and execute the following commands:  
```
python main.py eda --grafici
```
This command performs exploratory data analysis on the dataset: statistics, missing values, target distribution; with `--grafici`, it also shows histograms and correlation matrix.

```
python main.py kb
```
This command creates the Knowledge Base by mapping vocal features to canonical names, setting thresholds (refined from the data), and saving rules in `knowledge_base.json`.

```
python main.py train
```
This command trains the Random Forest model, calibrates probabilities, finds optimal thresholds (default F1), or you can insert `--thr youden`, evaluates on test, and saves everything in `parkinson_model.joblib`.

```
python main.py random_patient
```
This command can only be executed after training. It generates a JSON file with randomly generated but plausible patient data to test the model without manually entering all values.

```
python main.py predict --json paziente_random.json --thr youden
```
This command can only be executed after training. It uses the saved model to predict the state of a patient from a JSON file; it allows you to choose the threshold (F1, Youden, or fixed).

```
python main.py reason --json paziente_random.json
```
This command can only be executed after training. It applies KB rules and calculates fuzzy scores for a patient from JSON.

```
python main.py all-in-one --csv dataset.csv --json paziente_random.json --model parkinson_model.joblib --thr youden --out report.html
```
This command, executable only after training and prediction, performs a complete risk assessment for a patient: loads the dataset, model, and clinical data, calculates probability and diagnosis using the Youden threshold, estimates fuzzy risk, and generates an HTML report with results and explanations.

```
python main.py runs --repeats 1 --splits 5 --method sigmoid --n_estimators 200 --grid_points 101 --outdir results --csv cv_runs.csv --json cv_runs.json
```
