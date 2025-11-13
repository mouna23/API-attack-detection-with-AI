# scripts/train_model.py
"""
Entraîne un modèle simple de détection SQL/XSS/benign à partir du dataset nettoyé.
Usage :
    python scripts/train_model.py
"""

from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix
import joblib

TRAIN = Path("data/train.csv")
TEST = Path("data/test.csv")
MODEL_DIR = Path("models")
MODEL_PATH = MODEL_DIR / "api_attack_detector.joblib"

def main():
    if not TRAIN.exists() or not TEST.exists():
        print("[ERREUR] Les fichiers train/test sont introuvables. Exécute d'abord clean_and_split.py")
        return

    print("Chargement des données...")
    train_df = pd.read_csv(TRAIN)
    test_df = pd.read_csv(TEST)

    X_train, y_train = train_df["text"], train_df["label"]
    X_test, y_test = test_df["text"], test_df["label"]

    print("Entraînement du modèle TF-IDF + Logistic Regression...")
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            stop_words=None,
            max_features=5000,
            ngram_range=(1, 2)
        )),
        ("clf", LogisticRegression(max_iter=1000))
    ])

    pipeline.fit(X_train, y_train)

    print("Évaluation sur le jeu de test :")
    y_pred = pipeline.predict(X_test)
    print(classification_report(y_test, y_pred))
    print("Matrice de confusion :")
    print(confusion_matrix(y_test, y_pred))

    # Sauvegarde du modèle
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)
    print(f"✔ Modèle sauvegardé : {MODEL_PATH}")

if __name__ == "__main__":
    main()
