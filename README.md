# Cv_class

Agent de présélection de CV : **GO / NO GO**.

Le LLM lit chaque CV et juge trois critères, avec justification. La décision finale est prise en code (`decider`), donc lisible et modifiable sans toucher au prompt.

| Critère | Règle |
|---|---|
| Formation | TBS, ENIT, IHEC = prioritaires (classés en tête) |
| Langues | français **et** anglais de niveau professionnel |
| Expérience | conseil, stratégie, gestion de projets ou domaine proche, jugée sur le contenu des missions |

## Installation

```bash
pip install -r requirements.txt
cp .env.example .env      # puis renseigner ANTHROPIC_API_KEY
```

## Interface web

```bash
uvicorn app:app --reload
```

Ouvrir http://localhost:8000, déposer les CV : ils se rangent dans la pile GO ou NO GO, avec le détail par critère et un export CSV. Les fichiers envoyés sont supprimés dès l'analyse terminée.

## Déploiement sur Render

Le fichier `render.yaml` décrit le service. Sur Render : **New > Blueprint**, choisir ce dépôt, puis saisir `ANTHROPIC_API_KEY` et `APP_PASSWORD` quand ils sont demandés.

`APP_PASSWORD` protège l'interface : sans lui, toute personne ayant l'adresse pourrait utiliser la clé API.

## Ligne de commande

```bash
python cv_screener.py ./cvs -o resultats.csv
```

Formats lus : `.pdf`, `.docx`, `.txt`. Sortie : un CSV (ouvrable dans Excel) trié GO d'abord, avec les motifs de refus et les preuves tirées du CV.

## Réglages (`.env`)

- `ANTHROPIC_API_KEY` : clé API (obligatoire).
- `CV_MODEL` : modèle utilisé.
- `APP_PASSWORD` : mot de passe de l'interface web (vide = pas de protection, pour le local).
- `ECOLE_ELIMINATOIRE` : `false` par défaut (l'école est une priorité). `true` pour qu'une école hors liste donne NO GO.

La liste des écoles se modifie dans `ECOLES_PRIORITAIRES`, en haut de `cv_screener.py`.

Les CV marqués « À relire à la main » sont ambigus ou contiennent du texte destiné à manipuler l'agent.
