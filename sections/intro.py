import streamlit as st

from utils.io import DATASET_PAGE, LICENSE_TEXT


def show(df):
    st.title("Is France becoming more dangerous?")
    st.markdown("#### What the police and gendarmerie data says, department by department (2016 - %d)"
                % df["annee"].max())

    st.markdown(
        """
Crime and insecurity are one of the main concerns of French people, and the topic comes back in every
election. But the debate is often based on feelings or on one news story. In this app I try to answer
the question with the official figures of the Ministry of the Interior.

**Who is this for?** Citizens and local elected officials who want to know how their department compares
to the rest of the country.

**Questions I want to answer:**
1. How has recorded crime evolved since 2016, and what was the effect of Covid?
2. Which types of crime are increasing and which are decreasing?
3. Which departments are the most and the least affected, once we take population into account?
"""
    )

    with st.expander("About the data and how to read it", expanded=False):
        st.markdown(
            f"""
- **Dataset:** departmental base of crimes and offences recorded by the police and gendarmerie
  (SSMSI, Ministry of the Interior), one row per department, year and indicator.
  [Link to the dataset]({DATASET_PAGE})
- **Rates** are given per 1,000 inhabitants (per 1,000 dwellings for burglaries), so departments of
  different size can be compared.
- **Important:** these are *recorded* facts, not all the crimes that really happen. If more victims
  file a complaint (for example after an awareness campaign), the number goes up even if the real
  number of crimes did not change.
- Indicators have different units (victims, offences, vehicles...) so they are never added together.

{LICENSE_TEXT}
"""
        )
