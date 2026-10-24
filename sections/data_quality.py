import streamlit as st

from utils.prep import quality_report


def show(raw, df):
    st.header("1. Data quality")
    st.write("Before trusting the charts, here are the checks I did on the file.")

    missing, checks = quality_report(raw, df)
    st.dataframe(checks, hide_index=True)
    st.write("Missing values in the whole file:", int(raw.isnull().sum().sum()))

    st.markdown("""
**Cleaning**
- Column names in lower case and renamed.
- Department codes kept as text ("01", "2A", "971") so they match the map.
- No duplicated rows and no missing values were found, so no row had to be removed.

**Limits**
- These are only *recorded* facts, it depends on how many victims file a complaint.
- Facts are counted where they happen, so places with many tourists or workers (like Paris) have high rates.
- The population used for the rates is from one INSEE year, so some rates are approximate.
- Some indicators did not exist at the start (ex: fixed fines for drug use, created in 2020),
  so they are removed from the "change since 2016" charts because we can't divide by 0.
""")

    with st.expander("See the cleaned data"):
        st.dataframe(df.head(50))