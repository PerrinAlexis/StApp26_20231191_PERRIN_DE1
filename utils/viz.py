import plotly.express as px

COLOR = "#1f4e79"


def line_national(g, y_label, title):
    fig = px.line(g, x="annee", y="taux", markers=True, title=title,
                  labels={"annee": "Year", "taux": y_label})
    fig.update_traces(line_color=COLOR)
    # grey band for the Covid year
    fig.add_vrect(x0=2019.5, x1=2020.5, fillcolor="grey", opacity=0.2, line_width=0,
                  annotation_text="Covid lockdowns", annotation_position="top left")
    return fig


def map_departments(d, geojson, y_label, title):
    fig = px.choropleth(d, geojson=geojson, locations="dep", featureidkey="properties.code",
                        color="taux", color_continuous_scale="YlOrRd", hover_name="dep_name",
                        hover_data={"nombre": True}, title=title,
                        labels={"taux": y_label, "nombre": "Number of facts", "dep": "Code"})
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(height=600)
    return fig


def bar_ranking(d, y_label, title):
    fig = px.bar(d, x="taux", y="dep_label", orientation="h", title=title,
                 labels={"taux": y_label, "dep_label": "Department"})
    fig.update_traces(marker_color=COLOR)
    fig.update_yaxes(autorange="reversed")  # first one on top
    return fig


def small_multiples(d, y_label, title):
    fig = px.line(d, x="annee", y="taux_calcule", facet_col="dep_label", facet_col_wrap=3,
                  markers=True, title=title,
                  labels={"annee": "Year", "taux_calcule": y_label, "dep_label": ""})
    fig.update_traces(line_color=COLOR)
    return fig


def bar_evolution(g, year_start, year_end):
    g = g.reset_index()
    g["direction"] = "Decrease"
    g.loc[g["evolution"] > 0, "direction"] = "Increase"
    fig = px.bar(g, x="evolution", y="indicateur", orientation="h", color="direction",
                 color_discrete_map={"Increase": "#c0392b", "Decrease": "#2e86c1"},
                 title="Change in the number of recorded facts, " + str(year_start) + " vs " + str(year_end),
                 labels={"evolution": "Change (%)", "indicateur": "", "direction": ""})
    fig.update_layout(height=550)
    return fig
