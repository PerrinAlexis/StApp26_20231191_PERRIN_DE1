import pandas as pd
import streamlit as st

# names of the regions 
REGIONS = {
    "11": "Île-de-France", "24": "Centre-Val de Loire", "27": "Bourgogne-Franche-Comté",
    "28": "Normandie", "32": "Hauts-de-France", "44": "Grand Est", "52": "Pays de la Loire",
    "53": "Bretagne", "75": "Nouvelle-Aquitaine", "76": "Occitanie", "84": "Auvergne-Rhône-Alpes",
    "93": "Provence-Alpes-Côte d'Azur", "94": "Corse",
    "01": "Guadeloupe", "02": "Martinique", "03": "Guyane", "04": "La Réunion", "06": "Mayotte",
}


@st.cache_data
def clean_data(raw, dep_names):
    df = raw.copy()
    df.columns = [c.lower() for c in df.columns]
    df = df.rename(columns={"code_departement": "dep", "code_region": "reg",
                            "insee_pop": "pop", "insee_log": "log"})

    df = df.drop_duplicates()
    df = df.dropna(subset=["nombre"])

    df["region"] = df["reg"].map(REGIONS)
    df["dep_name"] = df["dep"].map(dep_names)
    df["dep_label"] = df["dep"] + " - " + df["dep_name"]
    df["outre_mer"] = df["dep"].str.len() == 3

    
    df["denominateur"] = df["pop"]
    cambriolage = df["indicateur"] == "Cambriolages de logement"
    df.loc[cambriolage, "denominateur"] = df.loc[cambriolage, "log"]


    df["taux_calcule"] = df["nombre"] / df["denominateur"] * 1000
    return df


def filter_data(df, indicateur, years, regions, include_dom):
    d = df[df["indicateur"] == indicateur]
    d = d[(d["annee"] >= years[0]) & (d["annee"] <= years[1])]
    if len(regions) > 0:
        d = d[d["region"].isin(regions)]
    if include_dom == False:
        d = d[d["outre_mer"] == False]
    return d


def national_by_year(d):

    g = d.groupby("annee")[["nombre", "denominateur"]].sum().reset_index()
    g["taux"] = g["nombre"] / g["denominateur"] * 1000
    return g


def by_department(d, year):
    g = d[d["annee"] == year].copy()
    g["taux"] = g["taux_calcule"]
    return g.sort_values("taux", ascending=False)


def evolution_by_indicator(df, year_start, year_end):
    g = df[df["annee"].isin([year_start, year_end])]
    g = g.groupby(["indicateur", "annee"])["nombre"].sum().unstack()
    g.columns = ["start", "end"]
    g = g[g["start"] > 0]  # we can't compute a change if the first value is 0 (ex: AFD created in 2020)
    g["evolution"] = (g["end"] - g["start"]) / g["start"] * 100
    return g.sort_values("evolution")


def quality_report(raw, df):
    missing = raw.isnull().mean() * 100
    missing = missing.round(2).reset_index()
    missing.columns = ["column", "missing_%"]

    checks = pd.DataFrame({
        "check": ["Rows in the file", "Duplicated rows", "Same department/year/indicator twice",
                  "Rows without number", "Negative numbers", "Departments", "Indicators", "Years"],
        "result": [len(raw), raw.duplicated().sum(),
                   df.duplicated(subset=["dep", "annee", "indicateur"]).sum(),
                   raw["nombre"].isnull().sum(), (df["nombre"] < 0).sum(),
                   df["dep"].nunique(), df["indicateur"].nunique(),
                   str(df["annee"].min()) + " - " + str(df["annee"].max())],
    })
    checks["result"] = checks["result"].astype(str)
    return missing, checks