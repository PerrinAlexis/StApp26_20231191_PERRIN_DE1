# Is France becoming more dangerous? - Streamlit data story

Individual project - Data Visualization (EFREI 2026)
Alexis PERRIN - 20231191 - DE1

App link: 
Demo video: https://youtu.be/1cUqHSdnNII
Storyboard: [assets/storyboard.pdf](assets/storyboard.pdf)

## 1. Subject
There is a pdf that explains the data given by the data.gouv website (documentation of the dataset).
The data represent the crimes and offences recorded by the police and the gendarmerie in France,
for every department, every year from 2016 to 2025 and 18 types of crime.

**Audience:** citizens and local elected officials.

**Questions:**
1. How has recorded crime evolved since 2016?
2. Which types of crime are increasing and which are decreasing?
3. Which departments are the most affected, once we take population into account?

## 2. Dataset

- **Name:** Bases statistiques communale, départementale et régionale de la délinquance enregistrée par la police
  et la gendarmerie nationales - *base départementale* (CSV, about 2 MB)
- **Producer:** SSMSI (Service statistique ministériel de la sécurité intérieure), Ministère de l'Intérieur
- **Link:** https://www.data.gouv.fr/datasets/bases-statistiques-communale-departementale-et-regionale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales
- **License:** Licence Ouverte / Open Licence 2.0 (Etalab)
- **Content:** one row per department x year x indicator (burglaries, vehicle thefts, physical violence,
  sexual violence, fraud, drugs...), with the number of facts, the rate per 1,000 inhabitants (or dwellings)
  and the INSEE population.
- **Map:** `data/departements.geojson` from https://github.com/gregoiredavid/france-geojson (IGN / INSEE data,
  Licence Ouverte).

## 3. How to run it

The CSV of the dataset must be in the `data/` folder (its name starts with `donnee-dep`).

```bash
python3 -m venv venv
source venv/bin/activate          
pip install -r requirements.txt
streamlit run app.py
```

## 4. Project structure

- `app.py`: sidebar filters and order of the sections
- `sections/`: the parts of the story (intro, data quality, overview, deep dives, conclusions)
- `utils/`: loading data, cleaning and charts
- `notebooks/exploration.ipynb`: first exploration of the data

## 5. Limits

- Only **recorded** facts: the numbers depend on how many victims file a complaint.
- Facts are counted where they happen, so places with many tourists or workers (like Paris) have high rates.
- The fixed fines for drug use (AFD) only exist since 2020, so they are removed from the "change since 2016" charts.