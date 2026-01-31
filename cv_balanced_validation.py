"""
Script di Cross-Validation Robusto per Dataset Sbilanciati
-----------------------------------------------------------
Metriche: F1-Macro, Balanced Accuracy (evita Accuracy Paradox)
Pipeline: Scaling dentro CV (no data leakage)
Stratified 10-Fold CV per preservare distribuzione target
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.dummy import DummyClassifier
import data_loader

# ============================================================================
# CONFIGURAZIONE
# ============================================================================

# Carica dati
df = data_loader.get_clean_data()
if df is None:
    raise SystemExit("Dataset non caricato")

# Preparazione features
df = df.copy()
df["Genre"] = df["genres_list"].apply(lambda x: x[0] if isinstance(x, (list, tuple)) and x else None)
df["Rating"] = (df["success_rate"] * 10).astype(float)

# Discretizzazione per features categoriche
df["Quality"] = pd.cut(
    df["Rating"],
    bins=[-np.inf, 6.5, 7.5, np.inf],
    labels=["Low", "Medium", "High"]
)

df["Price_Tier"] = pd.cut(
    df["price"].astype(float),
    bins=[-np.inf, 10, 30, 60, np.inf],
    labels=["Budget", "Economy", "Standard", "Premium"]
)

# Target binario
df["Success"] = df["is_success"].astype(int)

# Dataset completo
data = df[["Genre", "Quality", "Price_Tier", "Success"]].dropna()

# Encoding categoriche PRIMA del split (no data leakage)
# LabelEncoder per ogni colonna categorica
encoders = {}
for col in ["Genre", "Quality", "Price_Tier"]:
    enc = LabelEncoder()
    data[col] = enc.fit_transform(data[col])
    encoders[col] = enc

X = data[["Genre", "Quality", "Price_Tier"]].values
y = data["Success"].values

print(f"Dataset shape: {X.shape}")
print(f"Target distribution: {np.bincount(y)} (class 0: {np.sum(y==0)}, class 1: {np.sum(y==1)})")
print(f"Baseline (majority class): {np.max(np.bincount(y)) / len(y):.2%}\n")

# ============================================================================
# MODELLI CON PIPELINE (Scaler + Estimator)
# ============================================================================

models = {
    "Baseline (Most Frequent)": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", DummyClassifier(strategy="most_frequent", random_state=42))
    ]),
    "Logistic Regression": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced"))
    ]),
    "Decision Tree": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", DecisionTreeClassifier(random_state=42, class_weight="balanced", max_depth=10))
    ]),
    "Naive Bayes": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", GaussianNB())
    ]),
    "Neural Network (MLP)": Pipeline([
        ("scaler", StandardScaler()),
        ("clf", MLPClassifier(
            hidden_layer_sizes=(50, 25),
            max_iter=500,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.1
        ))
    ])
}

# ============================================================================
# STRATIFIED 10-FOLD CROSS-VALIDATION
# ============================================================================

cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=42)

# Metriche: F1-Macro e Balanced Accuracy (NO simple accuracy!)
scoring = {
    "f1_macro": "f1_macro",
    "balanced_accuracy": "balanced_accuracy",
    "accuracy": "accuracy"  # Solo per confronto con baseline
}

results = {}

print("=" * 80)
print("CROSS-VALIDATION IN CORSO...")
print("=" * 80 + "\n")

for name, pipeline in models.items():
    print(f"Training: {name}...")
    
    cv_results = cross_validate(
        pipeline,
        X,
        y,
        cv=cv,
        scoring=scoring,
        n_jobs=-1,
        return_train_score=False
    )
    
    results[name] = {
        "f1_macro_mean": np.mean(cv_results["test_f1_macro"]),
        "f1_macro_std": np.std(cv_results["test_f1_macro"], ddof=1),
        "balanced_acc_mean": np.mean(cv_results["test_balanced_accuracy"]),
        "balanced_acc_std": np.std(cv_results["test_balanced_accuracy"], ddof=1),
        "accuracy_mean": np.mean(cv_results["test_accuracy"]),
        "accuracy_std": np.std(cv_results["test_accuracy"], ddof=1),
    }

# ============================================================================
# OUTPUT IN FORMATO MARKDOWN
# ============================================================================

print("\n" + "=" * 80)
print("RISULTATI FINALI (Stratified 10-Fold CV)")
print("=" * 80 + "\n")

print("| Modello | F1-Macro (mean ± std) | Balanced Accuracy (mean ± std) | Accuracy (mean ± std) |")
print("|---------|------------------------|--------------------------------|------------------------|")

for name, stats in results.items():
    print(
        f"| {name:<27} | "
        f"{stats['f1_macro_mean']:.3f} ± {stats['f1_macro_std']:.3f} | "
        f"{stats['balanced_acc_mean']:.3f} ± {stats['balanced_acc_std']:.3f} | "
        f"{stats['accuracy_mean']:.3f} ± {stats['accuracy_std']:.3f} |"
    )

print("\n" + "=" * 80)
print("INTERPRETAZIONE:")
print("=" * 80)
print("""
- F1-Macro: Media armonica di precision e recall per entrambe le classi.
  Valori bassi indicano che il modello predice solo la classe maggioritaria.
  
- Balanced Accuracy: Media delle recall per classe. Corregge l'Accuracy Paradox.
  Se ~0.50, il modello è equivalente al random guessing.
  
- Accuracy: Metrica standard, ma fuorviante su dataset sbilanciati.
  Se tutti i modelli hanno ~0.93, stanno predicendo solo la classe maggioritaria!

RACCOMANDAZIONI:
1. Se F1-Macro e Balanced Accuracy sono bassi, considera tecniche di resampling:
   - SMOTE (oversampling sintetico della classe minoritaria)
   - Random undersampling della classe maggioritaria
   - Class weights (già implementato in alcuni modelli)
   
2. Se il problema persiste, potrebbe essere necessario:
   - Feature engineering più sofisticato
   - Raccogliere più dati per la classe minoritaria
   - Usare ensemble methods (Random Forest, XGBoost)
""")

print("\n" + "=" * 80)
print("DISTRIBUZIONE TARGET:")
print("=" * 80)
print(f"Classe 0 (Fallimento): {np.sum(y==0)} ({np.sum(y==0)/len(y):.2%})")
print(f"Classe 1 (Successo):   {np.sum(y==1)} ({np.sum(y==1)/len(y):.2%})")
print(f"Ratio: {np.sum(y==0)/np.sum(y==1):.2f}:1")
