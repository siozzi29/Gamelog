import pandas as pd
import numpy as np

from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, brier_score_loss

from pgmpy.models import DiscreteBayesianNetwork as BayesianNetwork
from pgmpy.estimators import BayesianEstimator, MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination


def cross_validate_bayes(
    df: pd.DataFrame,
    k: int = 10,
    use_bayesian_estimator: bool = True,
    random_state: int = 42
):
    """
    df: DataFrame già pulito con colonne: Genre, Price_Tier, Quality, Success
    """
    required_cols = {"Genre", "Price_Tier", "Quality", "Success"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Colonne mancanti: {missing}")

    data = df[list(required_cols)].dropna().copy()

    kf = KFold(n_splits=k, shuffle=True, random_state=random_state)

    accuracies = []
    briers = []

    for train_idx, test_idx in kf.split(data):
        train_df = data.iloc[train_idx].copy()
        test_df = data.iloc[test_idx].copy()

        # Encoding fold-specifico (gestisce unseen test labels)
        enc_genre = LabelEncoder()
        enc_price = LabelEncoder()
        enc_quality = LabelEncoder()

        train_df["Genre_enc"] = enc_genre.fit_transform(train_df["Genre"])
        train_df["Price_enc"] = enc_price.fit_transform(train_df["Price_Tier"])
        train_df["Quality_enc"] = enc_quality.fit_transform(train_df["Quality"])
        train_df["Success"] = train_df["Success"].astype(int)

        model = BayesianNetwork(
            [("Genre", "Success"), ("Price_Tier", "Success"), ("Quality", "Success")]
        )

        train_for_fit = pd.DataFrame({
            "Genre": train_df["Genre_enc"],
            "Price_Tier": train_df["Price_enc"],
            "Quality": train_df["Quality_enc"],
            "Success": train_df["Success"]
        })

        if use_bayesian_estimator:
            model.fit(
                train_for_fit,
                estimator=BayesianEstimator,
                prior_type="dirichlet",
                pseudo_counts=1
            )
        else:
            model.fit(train_for_fit, estimator=MaximumLikelihoodEstimator)

        infer = VariableElimination(model)

        y_true = []
        y_prob = []

        for _, row in test_df.iterrows():
            genre = row["Genre"]
            price = row["Price_Tier"]
            quality = row["Quality"]
            true_label = int(row["Success"])

            try:
                g = enc_genre.transform([genre])[0]
                p = enc_price.transform([price])[0]
                q = enc_quality.transform([quality])[0]

                result = infer.query(
                    variables=["Success"],
                    evidence={"Genre": g, "Price_Tier": p, "Quality": q}
                )
            except ValueError:
                # Fallback: prior su Success quando compaiono stati mai visti
                result = infer.query(variables=["Success"])

            # Probabilità di Success=1
            states = result.state_names.get("Success")
            if states and 1 in states:
                idx = states.index(1)
            elif states and "1" in states:
                idx = states.index("1")
            else:
                idx = 1  # fallback standard per binario
            prob_success = float(result.values[idx])

            y_true.append(true_label)
            y_prob.append(prob_success)

        y_pred = [1 if p >= 0.5 else 0 for p in y_prob]

        accuracies.append(accuracy_score(y_true, y_pred))
        briers.append(brier_score_loss(y_true, y_prob))

    acc_mean = np.mean(accuracies)
    acc_std = np.std(accuracies, ddof=1)
    brier_mean = np.mean(briers)
    brier_std = np.std(briers, ddof=1)

    print(f"Accuracy: {acc_mean:.2f} ± {acc_std:.2f}")
    print(f"Brier Score: {brier_mean:.2f} ± {brier_std:.2f}")


if __name__ == "__main__":
    # Sostituisci il path del CSV
    csv_path = "data/steam.csv"
    df = pd.read_csv(csv_path)

    # Esegui CV
    cross_validate_bayes(df, k=10, use_bayesian_estimator=True)