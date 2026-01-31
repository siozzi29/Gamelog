from pyDatalog import pyDatalog
import data_loader

# Definiamo i termini globalmente
pyDatalog.create_terms(
    'is_genre, is_success, X, C, G, YC, YG, P, '
    'cpu_price, gpu_price, cpu_year, gpu_year, '
    'cpu_tier, gpu_tier, cpu_budget, gpu_premium, '
    'is_bottleneck'
)

def setup_logic():
    pyDatalog.clear()
    df = data_loader.get_clean_data()
    if df is None: return

    for index, row in df.head(500).iterrows():
        gioco = row['name']
        for g in row['genres_list']:
            pyDatalog.assert_fact('is_genre', gioco, g)
        if row['is_success'] == 1:
            pyDatalog.assert_fact('is_success', gioco)

    # --- Fatti hardware (KB) ---
    # Prezzi e anno rilascio: base conoscitiva per inferenza
    cpus = {
        "i5-12400": {"price": 180, "year": 2022, "tier": "Budget"},
        "i7-13700": {"price": 380, "year": 2023, "tier": "Mid"},
        "i9-14900": {"price": 550, "year": 2024, "tier": "Premium"},
        "Ryzen 5": {"price": 160, "year": 2020, "tier": "Budget"}
    }
    gpus = {
        "RTX 3060": {"price": 290, "year": 2021, "tier": "Mid"},
        "RTX 4070": {"price": 600, "year": 2023, "tier": "Premium"},
        "RX 6700": {"price": 320, "year": 2021, "tier": "Mid"},
        "GTX 1650": {"price": 150, "year": 2019, "tier": "Budget"}
    }

    for cpu, meta in cpus.items():
        pyDatalog.assert_fact('cpu_price', cpu, meta["price"])
        pyDatalog.assert_fact('cpu_year', cpu, meta["year"])
        pyDatalog.assert_fact('cpu_tier', cpu, meta["tier"])

    for gpu, meta in gpus.items():
        pyDatalog.assert_fact('gpu_price', gpu, meta["price"])
        pyDatalog.assert_fact('gpu_year', gpu, meta["year"])
        pyDatalog.assert_fact('gpu_tier', gpu, meta["tier"])

    # --- Regole di inferenza ---
    # Fascia Budget/Premium derivata dal prezzo (non tabellata direttamente)
    cpu_budget(X) <= cpu_price(X, P) & (P <= 200)
    gpu_premium(X) <= gpu_price(X, P) & (P >= 500)

    # Regola di collo di bottiglia: CPU Budget + GPU Premium
    is_bottleneck(C, G) <= cpu_budget(C) & gpu_premium(G)

    # Regola alternativa: differenza anno rilascio > 4 anni
    is_bottleneck(C, G) <= cpu_year(C, YC) & gpu_year(G, YG) & (abs(YC - YG) > 4)

def query_custom_genre(genere_utente):
    # Trasformiamo l'input dell'utente in minuscolo per il confronto
    genere_cercato = genere_utente.lower()
    return is_genre(X, genere_cercato) & is_success(X)

def query_bottlenecks():
    return is_bottleneck(C, G)