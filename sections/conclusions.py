import streamlit as st

from utils.prep import evolution_by_indicator


def show(df):
    st.header("5. Conclusions")

    y0 = df["annee"].min()
    y1 = df["annee"].max()
    evo = evolution_by_indicator(df, y0, y1)
    n_up = (evo["evolution"] > 0).sum()
    n_down = (evo["evolution"] < 0).sum()

    st.markdown("**What we learned**")
    st.write("- Between", y0, "and", y1, ",", n_up, "types of crime increased and", n_down,
             "decreased. So France is not simply more or less dangerous, it depends on the type of crime.")
    st.write("- 2020 is a special year because of the lockdowns.")
    st.write("- The differences between departments are big, even when we use rates.")

    st.markdown("**Implications**")
    st.write("- We should always compare departments with rates and not with raw numbers.")
    st.write("- More recorded facts can also mean that more victims file a complaint, "
             "so an increase is not always bad news.")

    st.markdown("**Next steps**")
    st.write("- Use the communal base of the same dataset to go to the city level.")
    st.write("- Add other data (unemployment, density) to try to explain the differences.")
