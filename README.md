# Cv_class

Agent de présélection de CV : **GO / NO GO**.

Le LLM lit chaque CV et juge trois critères, avec justification. La décision finale est prise en code (`decider`), donc lisible et modifiable sans toucher au prompt.

| Critère | Règle |
|---|---|
| Formation | TBS, ENIT, IHEC = prioritaires (classés en tête) |
| Langues | français **et** anglais de niveau professionnel |
| Expérience | conseil, stratégie, gestion de projets ou domaine proche, jugée sur le contenu des missions |

## Utilisation

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
python cv_screener.py ./cvs -o resultats.csv
```

Formats lus : `.pdf`, `.docx`, `.txt`. Sortie : un CSV (ouvrable dans Excel) trié GO d'abord, avec les motifs de refus et les preuves tirées du CV.

## Réglages (haut de `cv_screener.py`)

- `ECOLES_PRIORITAIRES` : liste des écoles.
- `ECOLE_ELIMINATOIRE` : `False` par défaut (l'école est une priorité). `True` pour qu'une école hors liste donne NO GO.
- `CV_MODEL` (variable d'environnement) : modèle utilisé.

La colonne `a_verifier` signale les CV ambigus ou contenant du texte destiné à manipuler l'agent : à relire à la main.
