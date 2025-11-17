Le fichier `generated_payloads.csv` utilisé dans ce projet a été préparé à partir de sources publiques, notamment Kaggle et des listes de payloads connues.  
Il contient les colonnes suivantes :

- `text` : la requête API (paramètres inclus)  
- `label` : `sql_injection`, `xss` ou `benign`

Après exécution de `scripts/clean_and_split.py`, les fichiers suivants seront créés localement :
- `data/combined.csv`
- `data/train.csv`
- `data/test.csv`