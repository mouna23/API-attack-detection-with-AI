# tests/test_pipeline.py
"""
Test basique du modèle entraîné (vérifie chargement et prédiction).
Usage :
    pytest tests/test_pipeline.py
"""

from pathlib import Path
import joblib

MODEL_PATH = Path("models/api_attack_detector.joblib")

def test_model_load_and_predict():
    """Test que le modèle est chargeable et produit une prédiction."""
    assert MODEL_PATH.exists(), f"Le modèle {MODEL_PATH} n'existe pas. Exécute train_model.py d'abord."

    model = joblib.load(MODEL_PATH)

    # Quelques exemples simples
    examples = [
        ("/api/v1/user?id=1", "benign"),
        ("/customvoice/endpoints?api-version=2024-02-01-preview", "benign"),
        ("SELECT * FROM users WHERE id=1", "sql_injection"),
        ("/search?q=<script>alert('XSS')</script>", "xss")
    ]

    for text, expected_label in examples:
        pred = model.predict([text])[0]
        print(f"Texte: {text} → Prédit: {pred}")
        assert pred in ["sql_injection", "xss", "benign"], "Label inconnu"
