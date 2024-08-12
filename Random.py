
import pandas as pd
import streamlit as st
import numpy as np
from time import sleep

def form_groups_from_excel(df):
    # Combine the first and last names into a full name
    df['Full Name'] = df['First Name'] + ' ' + df['Last Name']

    # Separate names based on the score
    high_score_names = df[df['Score'] >= 3.5]['Full Name'].tolist()
    low_score_names = df[df['Score'] < 3.5]['Full Name'].tolist()

    # Shuffle the lists to randomize the groups
    np.random.shuffle(high_score_names)
    np.random.shuffle(low_score_names)


# If high_score_names has an odd number of names, move one to low_score_names
    if len(high_score_names) % 2 != 0:
        low_score_names.append(high_score_names.pop())



    # Function to create groups
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

    # Create groups for high and low scores separately
    high_score_groups = create_groups(high_score_names)
    low_score_groups = create_groups(low_score_names)

    return high_score_groups + low_score_groups

# Streamlit app
st.image("https://github.com/Guileort/Ramdomization-app/blob/main/Icono.png?", width=100)
new_title = '<p style="font-family:sans-serif; color:red; font-size: 32px;">APLICACION PARA LA ALEATORIZACION DE GRUPOS</p>'
st.markdown(new_title, unsafe_allow_html=True)

st.write("Cargue un archivo Excel con columnas tituladas:  'First Name', 'Last Name', and 'Score'.")

# File uploader
uploaded_file = st.file_uploader("Seleccione un archivo de excel", type=["xlsx"])

if uploaded_file is not None:
    # Read the uploaded file into a DataFrame
    df = pd.read_excel(uploaded_file)
    
    # Form the groups
    groups = form_groups_from_excel(df)

    # Display the groups
    st.write("### Grupos:")
    for idx, group in enumerate(groups, start=1):
        if len(group) == 3:
            st.write(f"**Grupo {idx}:** {group[0]}, {group[1]} y {group[2]}")
        else:
            st.write(f"**Grupo {idx}:** {group[0]} y {group[1]}")
        sleep(2)    
else:
    st.write("Por favor cargar un archivo Excel")
