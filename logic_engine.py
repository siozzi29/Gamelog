from pyDatalog import pyDatalog
import data_loader

# Definiamo i termini globalmente
pyDatalog.create_terms(
    'is_genre, is_success, is_hidden_gem, X, C, G, YC, YG, P, R, RC, '
    'cpu_price, gpu_price, cpu_year, gpu_year, '
    'cpu_tier, gpu_tier, cpu_budget, gpu_premium, '
    'cpu_name, gpu_name, cpu_fascia, gpu_fascia, '
    'cpu_entry_model, gpu_high_model, '
    'rating, review_count, price, '
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

        # Fatti per hidden gem: rating (0-10), review_count, prezzo
        try:
            rating_value = float(row['success_rate']) * 10
            review_count_value = int(row['positive_ratings'] + row['negative_ratings'])
            price_value = float(row['price'])

            pyDatalog.assert_fact('rating', gioco, rating_value)
            pyDatalog.assert_fact('review_count', gioco, review_count_value)
            pyDatalog.assert_fact('price', gioco, price_value)
        except Exception:
            pass

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
        pyDatalog.assert_fact('cpu_name', cpu, cpu)

        cpu_lower = cpu.lower()
        if ("ryzen 3" in cpu_lower) or ("i3" in cpu_lower) or ("pentium" in cpu_lower):
            pyDatalog.assert_fact('cpu_entry_model', cpu)

    for gpu, meta in gpus.items():
        pyDatalog.assert_fact('gpu_price', gpu, meta["price"])
        pyDatalog.assert_fact('gpu_year', gpu, meta["year"])
        pyDatalog.assert_fact('gpu_tier', gpu, meta["tier"])
        pyDatalog.assert_fact('gpu_name', gpu, gpu)

        gpu_lower = gpu.lower()
        if ("rtx 4080" in gpu_lower) or ("rtx 4090" in gpu_lower) or ("rx 7900" in gpu_lower):
            pyDatalog.assert_fact('gpu_high_model', gpu)

    # --- Regole di inferenza ---
    # Fasce hardware derivate (regole intermedie)
    cpu_fascia(X, "Entry") <= cpu_entry_model(X)
    cpu_fascia(X, "Entry") <= cpu_price(X, P) & (P <= 130)

    gpu_fascia(X, "High") <= gpu_high_model(X)
    gpu_fascia(X, "High") <= gpu_price(X, P) & (P >= 900)

    # Regola di collo di bottiglia: CPU Entry + GPU High
    is_bottleneck(C, G) <= cpu_fascia(C, "Entry") & gpu_fascia(G, "High")

    # Regola alternativa: differenza anno rilascio > 4 anni
    is_bottleneck(C, G) <= cpu_year(C, YC) & gpu_year(G, YG) & (abs(YC - YG) > 4)

    # Regola Hidden Gem: alto rating, bassa popolarità, prezzo basso
    is_hidden_gem(X) <= rating(X, R) & (R > 8.5) & review_count(X, RC) & (RC < 1000) & price(X, P) & (P < 15)

def query_custom_genre(genere_utente):
    # Trasformiamo l'input dell'utente in minuscolo per il confronto
    genere_cercato = genere_utente.lower()
    return is_genre(X, genere_cercato) & is_success(X)

def query_bottlenecks():
    return is_bottleneck(C, G)

def query_hidden_gems():
    return is_hidden_gem(X)