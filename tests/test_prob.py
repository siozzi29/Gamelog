try:
    from pgmpy.models import DiscreteBayesianNetwork as BayesianNetwork
    from pgmpy.factors.discrete import TabularCPD
    from pgmpy.inference import VariableElimination
    print("✅ Librerie caricate correttamente!")

    # Struttura minima: Genere -> Successo
    model = BayesianNetwork([('G', 'S')])

    # Probabilità del Genere (G): 0=Action, 1=Indie
    cpd_g = TabularCPD(variable='G', variable_card=2, values=[[0.7], [0.3]])

    # Probabilità di Successo (S) condizionata da G
    cpd_s = TabularCPD(variable='S', variable_card=2, 
                       values=[[0.8, 0.4], [0.2, 0.6]],
                       evidence=['G'], evidence_card=[2])

    model.add_cpds(cpd_g, cpd_s)
    
    if model.check_model():
        print("✅ Modello Bayesiano valido!")
        infer = VariableElimination(model)
        result = infer.query(variables=['S'], evidence={'G': 0})
        print("\nRisultato Query (Probabilità di Successo per gioco Action):")
        print(result)

except Exception as e:
    print(f"❌ Errore durante l'esecuzione: {e}")