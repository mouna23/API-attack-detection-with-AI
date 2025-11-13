# scripts/clean_and_split.py
"""
Nettoyage minimal et split du dataset en train/test.
Usage :
    python scripts/clean_and_split.py
Résultats :
    data/combined.csv
    data/train.csv
    data/test.csv
"""
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

INPUT = Path('data/generated_payloads.csv')
COMBINED = Path('data/combined.csv')
TRAIN = Path('data/train.csv')
TEST = Path('data/test.csv')

def basic_clean_text(text: str) -> str:
    """Nettoyage simple du texte : strip, suppression des caractères de contrôle."""
    if not isinstance(text, str):
        return ""
    return (
        text.replace('\n', ' ')
            .replace('\r', ' ')
            .replace('\t', ' ')
            .strip()
    )

def main():
    if not INPUT.exists():
        print(f"[ERREUR] Fichier introuvable : {INPUT}")
        return

    print(f"Chargement du dataset : {INPUT}")
    df = pd.read_csv(INPUT)

    if 'text' not in df.columns or 'label' not in df.columns:
        raise ValueError("Le CSV doit contenir les colonnes 'text' et 'label'.")

    print("Nettoyage basique du texte...")
    df['text'] = df['text'].astype(str).apply(basic_clean_text)
    df['label'] = df['label'].astype(str).str.strip().str.lower()

    print("Suppression des doublons et lignes vides...")
    before = len(df)
    df = df.dropna(subset=['text', 'label'])
    df = df.drop_duplicates(subset=['text', 'label'])
    print(f" - {before - len(df)} lignes supprimées")

    print("Sauvegarde du dataset combiné nettoyé...")
    df.to_csv(COMBINED, index=False)

    print("Découpage en train/test...")
    train_df, test_df = train_test_split(df, test_size=0.2, stratify=df['label'], random_state=42)

    TRAIN.parent.mkdir(parents=True, exist_ok=True)
    train_df.to_csv(TRAIN, index=False)
    test_df.to_csv(TEST, index=False)

    print(f"✔ Sauvegardé : {TRAIN} ({len(train_df)} lignes)")
    print(f"✔ Sauvegardé : {TEST} ({len(test_df)} lignes)")

if __name__ == "__main__":
    main()
