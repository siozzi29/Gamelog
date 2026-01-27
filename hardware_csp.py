from constraint import Problem

# 1. Creiamo il problema
problem = Problem()

# 2. Definiamo le Variabili e i loro Domini (Componenti e Prezzi)
# CPU: (Nome, Prezzo)
cpus = {"i5": 200, "i7": 350, "i9": 500}
# GPU: (Nome, Prezzo)
gpus = {"GTX1650": 150, "RTX3060": 300, "RTX4080": 800}

problem.addVariable("CPU", list(cpus.keys()))
problem.addVariable("GPU", list(gpus.keys()))

# 3. Definiamo i Vincoli
budget = 600

# Vincolo di Budget: CPU + GPU <= budget
def budget_constraint(cpu, gpu):
    return cpus[cpu] + gpus[gpu] <= budget

problem.addConstraint(budget_constraint, ["CPU", "GPU"])

# 4. Cerchiamo le soluzioni
solutions = problem.getSolutions()

print(f"--- Configurazioni Hardware (Budget: {budget}€) ---")
for s in solutions:
    totale = cpus[s['CPU']] + gpus[s['GPU']]
    print(f"Soluzione: CPU {s['CPU']} + GPU {s['GPU']} | Totale: {totale}€")