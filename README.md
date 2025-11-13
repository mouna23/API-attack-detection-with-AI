# Détection SQL/XSS sur API Web avec machine learning

Ce projet vise à détecter les injections SQL et XSS dans des requêtes/params d'API en utilisant du machine learning.

## Présentation du projet

Ce projet vise à détecter les injections **SQL** et **XSS** dans des requêtes et paramètres d'API en utilisant des techniques de **Machine Learning**.  
L'objectif est de créer un pipeline simple permettant de :
- préparer et nettoyer un dataset de requêtes d'API,
- entraîner un modèle capable de classer automatiquement les requêtes comme `benign`, `sql_injection` ou `xss`,
- fournir un modèle réutilisable pour des tests ou une future API de détection en temps réel.

---

## Description du dépôt

Ce dépôt contient uniquement le code et les scripts nécessaires à l'entraînement et à la validation du modèle.  
Les données sensibles ou volumineuses (`generated_payloads.csv`, `train.csv`, `test.csv`, `combined.csv`) ainsi que le modèle entraîné (`models/`) **ne sont pas inclus** et doivent être générés localement.

---

## Workflow du projet

1. **Préparer le dataset**   
   Le fichier `generated_payloads.csv` dans le dossier `data/` contient des exemples de requêtes d'API étiquetées (`sql_injection`, `xss`, `benign`) provenant de sources externes comme Kaggle ou générées localement.

2. **Nettoyage et découpage du dataset**  
   ```bash
   python scripts/clean_and_split.py

Le script :

supprime les doublons et les lignes vides,

nettoie les textes (espaces, retours à la ligne, tabulations),

normalise les labels,

génère :

data/combined.csv : dataset complet nettoyé,

data/train.csv : données d'entraînement (80%),

data/test.csv : données de test (20%).

3. **Entraînement du modèle**  
   ```bash
   python scripts/train_model.py

Le modèle utilise un pipeline ML :

TF-IDF Vectorizer (TfidfVectorizer) : transforme les requêtes texte en vecteurs numériques, en capturant l’importance des mots ou symboles suspects.

Logistic Regression (LogisticRegression) : classifieur supervisé qui apprend à associer les vecteurs TF-IDF aux classes sql_injection, xss ou benign.

Après l’entraînement, le modèle est sauvegardé dans le dossier models, il peut ensuite être utilisé pour prédire la classe d’une nouvelle requête.

4. **Entraînement du modèle**  
  ```bash
   pytest -v -s tests/test_pipeline.py

Le test vérifie que :

le modèle est chargeable,

il prédit correctement plusieurs exemples simples,

aucune erreur de pipeline ne survient.

5. **Dépendances Python**  
  ```bash
   pip3 install -r requirements.txt

* pandas

* scikit-learn

* joblib

* pytest

5. **Notes**  
Les scripts sont conçus pour être exécutés localement, dans un environnement Python 3.13+ avec les dépendances listées.