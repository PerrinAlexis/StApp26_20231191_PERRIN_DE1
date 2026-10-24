import glob
import json

import pandas as pd
import streamlit as st

DATASET_PAGE = "https://www.data.gouv.fr/datasets/bases-statistiques-communale-departementale-et-regionale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales"

LICENSE_TEXT = (
    "Source : SSMSI - Ministère de l'Intérieur, base départementale de la délinquance "
    "enregistrée par la police et la gendarmerie nationales (data.gouv.fr). "
    "Licence Ouverte / Open Licence 2.0 (Etalab)."
)


@st.cache_data
def load_data():
    path = glob.glob("data/donnee-dep*.csv")[0]
    df = pd.read_csv(path, sep=";", decimal=",", dtype={"Code_departement": str, "Code_region": str})
    return df


@st.cache_data
def load_geojson():
    with open("data/departements.geojson", encoding="utf-8") as f:
        return json.load(f)


@st.cache_data
def get_dep_names():
    geo = load_geojson()
    names = {}
    for feat in geo["features"]:
        names[feat["properties"]["code"]] = feat["properties"]["nom"]
    names["971"] = "Guadeloupe"
    names["972"] = "Martinique"
    names["973"] = "Guyane"
    names["974"] = "La Réunion"
    names["976"] = "Mayotte"
    return names
