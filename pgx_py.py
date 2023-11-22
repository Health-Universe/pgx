import streamlit as st
import requests
import json

# Define static parameters
cpic_api_url = "https://api.cpicpgx.org/v1/"
drug_api_url = cpic_api_url + "drug"
guideline_api_url = cpic_api_url + "guideline"

def get_guidelineid_from_drug(json_data):
    try:
        data_list = json_data
        guideline_id = data_list[0].get("guidelineid") if data_list and isinstance(data_list, list) and len(data_list) > 0 else None
        return guideline_id
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {e}")
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def get_drug_data(drug):
    url = f"{drug_api_url}?name=eq.{drug}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None

def get_guideline(guideline_id):
    url = f"{guideline_api_url}?id=eq.{guideline_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None

def get_guideline_for_specific_drug(drug):
    drug_data = get_drug_data(drug)
    guideline_id = get_guidelineid_from_drug(drug_data)
    guideline_data = get_guideline(guideline_id)

    if guideline_data:
        st.subheader("Retrieved Guideline Data:")
        st.json(guideline_data)
    else:
        st.error("Error retrieving guideline data.")

def main():
    st.title("Guideline Viewer")

    drug = st.selectbox("Select a drug:", ['codeine', 'abacavir', 'simvastatin'])

    if st.button("Fetch Guideline"):
        get_guideline_for_specific_drug(drug)

if __name__ == "__main__":
    main()
