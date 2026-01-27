from pgmpy.models import DiscreteBayesianNetwork as BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
from sklearn.preprocessing import LabelEncoder
import data_loader
import pandas as pd

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