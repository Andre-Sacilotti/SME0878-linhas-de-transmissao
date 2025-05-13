import streamlit as st
import pandas as pd
import altair as alt

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('processed_data/risco_cluster.csv')
    return df

df = load_data()

st.title('Risco Cluster Dashboard')

clusters = sorted(df['cluster_geo'].unique())
categories = sorted(df['Denominação_categoria'].unique())

selected_cluster = st.sidebar.selectbox('Select Cluster', ['All'] + [str(c) for c in clusters])
selected_category = st.sidebar.selectbox('Select Category', ['All'] + categories)

filtered_df = df.copy()
if selected_cluster != 'All':
    filtered_df = filtered_df[filtered_df['cluster_geo'] == float(selected_cluster)]
if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['Denominação_categoria'] == selected_category]

st.subheader('Filtered Data')
st.dataframe(filtered_df)

st.subheader('Summary Statistics')
st.write(f"Total Inspections: {filtered_df['total_inspecoes'].sum()}")
st.write(f"Total Problems: {filtered_df['n_problemas'].sum()}")
st.write(f"Average Risk Proportion: {filtered_df['prop_risco_cluster'].mean():.2f}")

st.subheader('Risk Proportion by Category')
bar_chart = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X('Denominação_categoria', sort='-y'),
    y='prop_risco_cluster',
    color='prop_risco_cluster',
    tooltip=['Denominação_categoria', 'prop_risco_cluster']
).properties(width=700)
st.altair_chart(bar_chart, use_container_width=True)

st.subheader('Problems by Category')
bar_chart2 = alt.Chart(filtered_df).mark_bar().encode(
    x=alt.X('Denominação_categoria', sort='-y'),
    y='n_problemas',
    color='n_problemas',
    tooltip=['Denominação_categoria', 'n_problemas']
).properties(width=700)
st.altair_chart(bar_chart2, use_container_width=True)
