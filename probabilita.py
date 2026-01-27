from pgmpy.models import DiscreteBayesianNetwork as BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

# 1. Definiamo la struttura: Il Genere influenza il Successo
# (In un caso reale, la rete sarebbe più complessa come descritto nel progetto)
model = BayesianNetwork([('Genere', 'Successo')])

# 2. Definiamo le probabilità condizionate (CPT)
# Esempio: Probabilità di successo se il gioco è Action (0) o Indie (1)
cpd_genere = TabularCPD(variable='Genere', variable_card=2, values=[[0.7], [0.3]])

cpd_successo = TabularCPD(variable='Successo', variable_card=2, 
                          values=[[0.8, 0.4],  # Prob di successo Alto
                                  [0.2, 0.6]], # Prob di successo Basso
                          evidence=['Genere'], evidence_card=[2])

# 3. Associamo le tabelle al modello
model.add_cpds(cpd_genere, cpd_successo)

# 4. Facciamo un'inferenza
infer = VariableElimination(model)
print("--- Inferenza Probabilistica ---")
# Chiediamo: qual è la probabilità di successo se sappiamo che il gioco è un Action?
query = infer.query(variables=['Successo'], evidence={'Genere': 0})
print(query)