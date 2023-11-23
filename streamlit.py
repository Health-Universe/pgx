# -*- coding: utf-8 -*-
"""streamlit.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qVJh-h0cNk9JjpilOsCOCa3RkUhFU6Sz
"""

import streamlit as st
import requests
import json

# Define static parameters

# CPIC API URLs
cpic_api_url = "https://api.cpicpgx.org/v1/"
drug_api_url = cpic_api_url + "drug"
guideline_api_url = cpic_api_url + "guideline"
recommendation_view_api_url = cpic_api_url + "recommendation_view"

# Functions that collect information from the user

def get_ethnicity():
    choices = ['Latino', 'American', 'European', 'Oceanian', 'East Asian',
               'Near Eastern', 'Central/South Asian', 'Sub-Saharan African',
               'African American/Afro-Caribbean', 'Other', 'Mixed Ethnicity',
               'Unknown']
    ethnicity = st.selectbox("Select Ethnicity", choices)
    return ethnicity

def get_drug():
    choices = ['codeine', 'abacavir', 'simvastatin']
    drug = st.selectbox("Select Drug", choices)
    return drug

def get_lookup_keys_for_query(drug):
    lookup_keys_values = get_lookup_keys_for_drug(drug)

    if lookup_keys_values:
        st.write(f"Available lookup keys for {drug}:")
        lookup_key = st.selectbox("Select a lookup key", list(lookup_keys_values.keys()))

        lookup_values = lookup_keys_values[lookup_key]
        st.write(f"Available lookup values for {lookup_key}: {', '.join(lookup_values)}")

        lookup_value = st.selectbox(f"Select a lookup value for {lookup_key}", list(lookup_values))

        return lookup_key, lookup_value

    st.error("Failed to retrieve lookup keys.")
    return None

def get_lookup_keys_for_drug(drug):
    url = f"{recommendation_view_api_url}?drugname=eq.{drug}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            lookup_keys_values = {}

            for recommendation in data:
                lookup_key_values = recommendation.get("lookupkey", {})
                for key, value in lookup_key_values.items():
                    if key not in lookup_keys_values:
                        lookup_keys_values[key] = set()
                    lookup_keys_values[key].add(value)

            return lookup_keys_values

        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None

def get_recommendation_for_specific_drug(drug, gene, phenotype):
    url = f"{recommendation_view_api_url}?drugname=eq.{drug}&lookupkey=cs.{{%22{gene}%22:%20%22{phenotype}%22}}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            st.write("CPIC Recommendations:")
            st.write(response.json())

        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None

if __name__ == "__main__":
    st.title("CPIC Recommendation Viewer")

    # Call the ethnicity function
    # ethnicity = get_ethnicity()
    drug = get_drug()
    gene, phenotype = get_lookup_keys_for_query(drug)

    if gene and phenotype:
        st.write("Selected Lookup Key:", gene)
        st.write("Selected Lookup Value:", phenotype)

        # Get recommendations for specific drug
        get_recommendation_for_specific_drug(drug, gene, phenotype)