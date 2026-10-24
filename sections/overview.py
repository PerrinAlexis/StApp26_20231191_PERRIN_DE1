import streamlit as st

from utils.prep import national_by_year
from utils import viz


def show(d, indicateur, years, rate_label):
    st.header("2. Overview: the national trend")
    st.write("Indicator:", indicateur, "- years", years[0], "to", years[1])

    g = national_by_year(d)
    if len(g) == 0:
        st.warning("No data for these filters.")
        return

    first = g.iloc[0]
    last = g.iloc[-1]
    evol = (last["nombre"] - first["nombre"]) / first["nombre"] * 100

    last_year = d[d["annee"] == last["annee"]].sort_values("taux_calcule", ascending=False)
    worst = last_year.iloc[0]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Recorded facts in " + str(int(last["annee"])), int(last["nombre"]))
    c2.metric("Rate in " + str(int(last["annee"])), round(last["taux"], 2), help=rate_label)
    c3.metric("Change since " + str(int(first["annee"])), str(round(evol, 1)) + " %")
    c4.metric("Highest rate in " + str(int(last["annee"])), worst["dep_name"])

    fig = viz.line_national(g, rate_label, indicateur + ": rate per year")
    st.plotly_chart(fig)
    st.caption("Line chart of the rate per year. The grey band is 2020, the year of the Covid lockdowns.")

    if evol > 0:
        st.info("Between " + str(int(first["annee"])) + " and " + str(int(last["annee"]))
                + ", the number of recorded facts increased by " + str(round(evol, 1)) + " %.")
    else:
        st.info("Between " + str(int(first["annee"])) + " and " + str(int(last["annee"]))
                + ", the number of recorded facts decreased by " + str(round(-evol, 1)) + " %.")