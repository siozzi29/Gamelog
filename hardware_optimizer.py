from constraint import Problem

def find_hardware_configs(budget):
    # Inizializziamo il problema CSP (Constraint Satisfaction Problem)
    problem = Problem()

    # Database componenti (Nome: Prezzo)
    cpus = {"i5-12400": 180, "i7-13700": 380, "i9-14900": 550, "Ryzen 5": 160}
    gpus = {"RTX 3060": 290, "RTX 4070": 600, "RX 6700": 320, "GTX 1650": 150}

    # Definiamo le variabili e i domini (le opzioni disponibili)
    problem.addVariable("CPU", list(cpus.keys()))
    problem.addVariable("GPU", list(gpus.keys()))

    # Vincolo: La somma dei prezzi deve essere inferiore o uguale al budget
    def budget_constraint(cpu, gpu):
        return cpus[cpu] + gpus[gpu] <= budget

    # Aggiungiamo il vincolo al risolutore
    problem.addConstraint(budget_constraint, ["CPU", "GPU"])

    # Il motore CSP calcola tutte le combinazioni valide
    solutions = problem.getSolutions()
    
    formatted_solutions = []
    for s in solutions:
        costo = cpus[s['CPU']] + gpus[s['GPU']]
        formatted_solutions.append(f"{s['CPU']} + {s['GPU']} (Totale: {costo}€)")
    
    return formatted_solutions