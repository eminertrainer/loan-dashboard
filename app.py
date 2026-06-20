
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Loan Approval Dashboard', layout='wide')

@st.cache_data

def load_data():
    return pd.read_csv('loanapprovaldata.csv')

_df = load_data()

st.title('🏦 Loan Approval Analytics Dashboard')

# Filters
st.sidebar.header('Filters')
gender = st.sidebar.multiselect('Gender', sorted(_df['Gender'].dropna().unique()))
area = st.sidebar.multiselect('Property Area', sorted(_df['Property_Area'].dropna().unique()))
edu = st.sidebar.multiselect('Education', sorted(_df['Education'].dropna().unique()))

df = _df.copy()
if gender:
    df = df[df['Gender'].isin(gender)]
if area:
    df = df[df['Property_Area'].isin(area)]
if edu:
    df = df[df['Education'].isin(edu)]

approved = (df['Loan_Status'] == 'Y').sum()
rejected = (df['Loan_Status'] == 'N').sum()
rate = approved / len(df) * 100 if len(df) else 0
avg_loan = pd.to_numeric(df['LoanAmount'], errors='coerce').mean()

c1,c2,c3,c4 = st.columns(4)
c1.metric('Applications', len(df))
c2.metric('Approved', approved)
c3.metric('Rejected', rejected)
c4.metric('Approval Rate', f'{rate:.1f}%')

st.divider()

col1,col2 = st.columns(2)
with col1:
    fig = px.pie(df, names='Loan_Status', title='Loan Status Distribution')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    area_status = df.groupby(['Property_Area','Loan_Status']).size().reset_index(name='Count')
    fig = px.bar(area_status, x='Property_Area', y='Count', color='Loan_Status', barmode='group', title='Approval by Property Area')
    st.plotly_chart(fig, use_container_width=True)

col3,col4 = st.columns(2)
with col3:
    credit = df.groupby(['Credit_History','Loan_Status']).size().reset_index(name='Count')
    fig = px.bar(credit, x='Credit_History', y='Count', color='Loan_Status', title='Credit History Impact')
    st.plotly_chart(fig, use_container_width=True)

with col4:
    fig = px.scatter(df, x='ApplicantIncome', y='LoanAmount', color='Loan_Status', title='Income vs Loan Amount')
    st.plotly_chart(fig, use_container_width=True)

st.subheader('Dataset Preview')
st.dataframe(df.head(50), use_container_width=True)
