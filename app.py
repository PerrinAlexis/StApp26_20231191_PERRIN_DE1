import os

import streamlit as st

from utils.io import load_data, get_dep_names, LICENSE_TEXT
from utils.prep import clean_data, filter_data
from sections import intro, overview, deep_dives, data_quality, conclusions

st.set_page_config(page_title="Crime in France", layout="wide")

# load and clean the data
raw = load_data()
df = clean_data(raw, get_dep_names())

# sidebar
st.sidebar.title("Filters")
indicators = sorted(df["indicateur"].unique())
indicateur = st.sidebar.selectbox("Type of crime", indicators)

ymin = int(df["annee"].min())
ymax = int(df["annee"].max())
years = st.sidebar.slider("Years", ymin, ymax, (ymin, ymax))

regions = st.sidebar.multiselect("Regions (empty = all France)", sorted(df["region"].dropna().unique()))
include_dom = st.sidebar.checkbox("Include overseas departments", value=True)
st.sidebar.caption(LICENSE_TEXT)

# about me
st.sidebar.markdown("---")
if os.path.exists("assets/efrei_logo.png"):
    st.sidebar.image("assets/efrei_logo.png", width=150)
st.sidebar.markdown("""
**Full name :** Alexis PERRIN
**Program :**
**Year :** 2026
**Email :** alexis.perrin@efrei.net
**LinkedIn :** [alexis-perrin](https://www.linkedin.com/in/alexis-perrin-03752b292)
**GitHub :** [PerrinAlexis](https://github.com/PerrinAlexis)

**Course :** Data Analysis & Visualization
**Project proposed by :** Prof. Mano Mathew
**Email :** mano.mathew@efrei.fr
""")

if indicateur == "Cambriolages de logement":
    rate_label = "Rate per 1,000 dwellings"
else:
    rate_label = "Rate per 1,000 inhabitants"

d = filter_data(df, indicateur, years, regions, include_dom)

# the story
intro.show(df)
data_quality.show(raw, df)
overview.show(d, indicateur, years, rate_label)
deep_dives.show(df, d, indicateur, years, rate_label)
conclusions.show(df)