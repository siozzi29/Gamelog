from pgmpy.models import DiscreteBayesianNetwork as BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator, BayesianEstimator
from pgmpy.inference import VariableElimination
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score, brier_score_loss
import data_loader
import pandas as pd
import numpy as np
import logging
logging.getLogger("pgmpy").setLevel(logging.ERROR)

# Creiamo un encoder globale per ricordarci a quale numero corrisponde ogni genere
encoder = LabelEncoder()

def train_model():
    df = data_loader.get_clean_data()
    
    data = pd.DataFrame()
    # Prendiamo solo il genere principale
    generi_testuali = df['genres_list'].apply(lambda x: x[0])
    
    # TRASFORMAZIONE: 'Action' -> 0, 'Indie' -> 1, ecc.
    data['Genere'] = encoder.fit_transform(generi_testuali)
    data['Successo'] = df['is_success']
    
    model = BayesianNetwork([('Genere', 'Successo')])
    
    # Ora i dati sono numeri, pgmpy sarà felice
    model.fit(data, estimator=MaximumLikelihoodEstimator)
    
    return model

def predict_success(nome_genere):
    model = train_model()
    infer = VariableElimination(model)
    
    # Trasformiamo il nome cercato nel suo numero corrispondente
    try:
        genere_id = encoder.transform([nome_genere])[0]
        result = infer.query(variables=['Successo'], evidence={'Genere': genere_id})
        return result
    except ValueError:
        return f"Genere '{nome_genere}' non trovato nel dataset."

def cross_validate_bayesian_network(k=5, random_state=42):
    df = data_loader.get_clean_data()

    def _extract_main_genre(value):
        if isinstance(value, (list, tuple)) and value:
            return value[0]
        return value

    def _success_prob(factor):
        states = factor.state_names.get('Successo') if hasattr(factor, 'state_names') else None
        if states:
            if 1 in states:
                idx = states.index(1)
            elif '1' in states:
                idx = states.index('1')
            elif True in states:
                idx = states.index(True)
            else:
                idx = 0
        else:
            idx = 1 if len(factor.values) > 1 else 0
        return float(factor.values[idx])

    data = pd.DataFrame({
        'Genere_txt': df['genres_list'].apply(_extract_main_genre),
        'Successo': df['is_success']
    }).dropna()

    k = 10 if k == 10 else 5
    kf = KFold(n_splits=k, shuffle=True, random_state=random_state)

    accuracies = []
    briers = []

    for train_idx, test_idx in kf.split(data):
        train_df = data.iloc[train_idx]
        test_df = data.iloc[test_idx]

        fold_encoder = LabelEncoder()
        train_data = pd.DataFrame({
            'Genere': fold_encoder.fit_transform(train_df['Genere_txt']),
            'Successo': train_df['Successo'].astype(int)
        })

        model = BayesianNetwork([('Genere', 'Successo')])
        model.fit(
            train_data,
            estimator=BayesianEstimator,
            prior_type="dirichlet",
            pseudo_counts=1
        )
        infer = VariableElimination(model)

        y_true = []
        y_prob = []

        for _, row in test_df.iterrows():
            genre = row['Genere_txt']
            true_label = int(row['Successo'])

            if genre in fold_encoder.classes_:
                genre_id = fold_encoder.transform([genre])[0]
                result = infer.query(variables=['Successo'], evidence={'Genere': genre_id})
            else:
                result = infer.query(variables=['Successo'])

            prob_success = _success_prob(result)
            y_true.append(true_label)
            y_prob.append(prob_success)

        y_pred = [1 if p >= 0.5 else 0 for p in y_prob]
        accuracies.append(accuracy_score(y_true, y_pred))
        briers.append(brier_score_loss(y_true, y_prob))

    acc_mean = float(np.mean(accuracies))
    acc_std = float(np.std(accuracies, ddof=1))
    brier_mean = float(np.mean(briers))
    brier_std = float(np.std(briers, ddof=1))

    print(f"Accuracy: {acc_mean:.2f} ± {acc_std:.2f}")
    print(f"Brier Score: {brier_mean:.2f} ± {brier_std:.2f}")

    return {
        "accuracy_mean": acc_mean,
        "accuracy_std": acc_std,
        "brier_mean": brier_mean,
        "brier_std": brier_std
    }