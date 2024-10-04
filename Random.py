import pandas as pd
import streamlit as st
import numpy as np
from time import sleep

def form_groups_from_excel(df):
    # Combine the first and last names into a full name
    df['Full Name'] = df['First Name'] + ' ' + df['Last Name']

    # Separate names based on the score into three categories: high, medium, low
    high_score_names = df[df['ID'] >= 3.8]['Full Name'].tolist()
    medium_score_names = df[(df['ID'] >= 3.2) & (df['ID'] < 3.8)]['Full Name'].tolist()
    low_score_names = df[df['ID'] < 3.2]['Full Name'].tolist()

    # Shuffle the lists to randomize the groups
    np.random.shuffle(high_score_names)
    np.random.shuffle(medium_score_names)
    np.random.shuffle(low_score_names)

    # If high_score_names has an odd number of names, move one to medium_score_names
    if len(high_score_names) % 2 != 0:
        medium_score_names.append(high_score_names.pop())

    # If medium_score_names has an odd number of names, move one to low_score_names
    if len(medium_score_names) % 2 != 0:
        low_score_names.append(medium_score_names.pop())

    # Function to create groups of 2 or 3
    def create_groups(names):
        groups = []
        i = 0
        while i < len(names):
            if len(names) - i == 3:
                groups.append((names[i], names[i + 1], names[i + 2]))
                i += 3
            else:
                groups.append((names[i], names[i + 1]))
                i += 2
        return groups

    # Create groups for high, medium, and low scores separately
    high_score_groups = create_groups(high_score_names)
    medium_score_groups = create_groups(medium_score_names)
    low_score_groups = create_groups(low_score_names)

    return high_score_groups + medium_score_groups + low_score_groups

# Streamlit app
### Position logo on right side
left_co, cent_co,last_co = st.columns(3)
with last_co:
    st.image("https://raw.githubusercontent.com/Guileort/Ramdomization-app/f4555721973318b15276a5276830b5400109d175/logo.svg?raw=true", width=100)

new_title = '<p style="font-family:sans-serif; color:rgb(0, 0, 139); font-size: 32px; font-weight: bold"> Aleatoreitor APP</p>'
st.markdown(new_title, unsafe_allow_html=True)

st.write("Aleatoriza tu listado en grupos de dos o tres personas, solo toma unos segundos.")

st.write("Cargue un archivo Excel con columnas tituladas: 'First Name', 'Last Name', y 'ID' ")

# Add custom CSS to change button color and font size
st.markdown("""
    <style>
    .stButton > button {
        background-color: green;
        color: white;
        font-size: 22 px;
        border-radius: 5px;
        padding: 8px 16px;
    }
    .stButton > button:hover {
        background-color: darkgreen;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Seleccione un archivo de excel", type=["xlsx"])

# Button to repeat randomization
randomize_button = st.button("Aleatorizar")

if uploaded_file is not None and randomize_button:
    # Read the uploaded file into a DataFrame
    df = pd.read_excel(uploaded_file)
    
    # Form the groups
    groups = form_groups_from_excel(df)

    # Display the groups
    st.write("### Grupos:")
    
    for idx, group in enumerate(groups, start=1):
        if len(group) == 3:
            group_text = f"**Grupo {idx}**: {group[0]}, {group[1]}, {group[2]}"
        else:
            group_text = f"**Grupo {idx}**: {group[0]:10} y {group[1]}"
        st.markdown(f"{group_text}",  unsafe_allow_html=True)
        sleep(2)
