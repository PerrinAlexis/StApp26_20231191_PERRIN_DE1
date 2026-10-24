import streamlit as st

from utils.io import load_geojson
from utils.prep import by_department, evolution_by_indicator
from utils import viz


def show(df, d, indicateur, years, rate_label):
    st.header("3. Where? Comparing departments")

    year = st.slider("Year for the map and the rankings", years[0], years[1], years[1])
    dep = by_department(d, year)
    if len(dep) == 0:
        st.warning("No data for these filters.")
        return

    # map
    fig = viz.map_departments(dep, load_geojson(), rate_label, indicateur + " in " + str(year))
    st.plotly_chart(fig)
    st.caption("Map of metropolitan France: the darker the department, the higher the rate. "
               "Overseas departments are not on the map but they are in the rankings.")

    # top 10 and bottom 10
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(viz.bar_ranking(dep.head(10), rate_label, "10 highest rates in " + str(year)))
    with col2:
        bottom = dep.sort_values("taux").head(10)
        st.plotly_chart(viz.bar_ranking(bottom, rate_label, "10 lowest rates in " + str(year)))

    st.info("In " + str(year) + ", the highest rate is in " + dep.iloc[0]["dep_name"]
            + " (" + str(round(dep.iloc[0]["taux"], 2)) + ") and the lowest is in "
            + dep.iloc[-1]["dep_name"] + " (" + str(round(dep.iloc[-1]["taux"], 2)) + ").")

    # compare some departments over time
    st.subheader("Compare departments over time")
    options = sorted(d["dep_label"].unique())
    chosen = st.multiselect("Choose departments", options, default=list(dep["dep_label"].head(3)))
    if len(chosen) > 0:
        fig = viz.small_multiples(d[d["dep_label"].isin(chosen)], rate_label, indicateur + ": rate per year")
        st.plotly_chart(fig)

    # change for every type of crime
    st.header("4. What? Which crimes are rising")
    all_years = sorted(df["annee"].unique())
    c1, c2 = st.columns(2)
    y0 = c1.selectbox("From", all_years, index=0)
    y1 = c2.selectbox("To", all_years, index=len(all_years) - 1)
    if y0 >= y1:
        st.warning("The first year must be before the second one.")
        return

    evo = evolution_by_indicator(df, y0, y1)
    st.plotly_chart(viz.bar_evolution(evo, y0, y1))
    st.caption("Change for every type of crime in all France (not affected by the filters). "
               "Red = increase, blue = decrease.")
    st.info("Biggest increase: " + evo.index[-1] + " (" + str(round(evo["evolution"].iloc[-1])) + " %). "
            + "Biggest decrease: " + evo.index[0] + " (" + str(round(evo["evolution"].iloc[0])) + " %).")