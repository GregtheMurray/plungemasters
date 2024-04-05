import streamlit as st
import pandas as pd
import numpy as np

url = 'https://docs.google.com/spreadsheets/d/1VKIpC91WmA7jIms8AMakdqYSvz4QKerIcYThkF9rzok/export?format=csv&id=1VKIpC91WmA7jIms8AMakdqYSvz4QKerIcYThkF9rzok&gid=448313398'




@st.cache_data
def get_data(url):
    df = pd.read_csv(url)
    return df

 

def cell_color_rd(rd_val):
    par =72
    if rd_val == par:
        color = '#edede9'
    elif rd_val < par:
        color = '#2a9d8f'
    else:
        color = '#f4a261'
    return 'background-color: %s' % color



hcol1,hcol2 = st.columns([.2,.8])
with hcol1:
    st.image('https://upload.wikimedia.org/wikipedia/commons/c/c5/Masters_Tournament.svg')
with hcol2:
    st.title('Masters Leaderboard')


df = get_data(url)
df['row_num'] = df.reset_index().index

names = sorted(list(df['Name'].unique()))
names.insert(0,'Entrant Name')
name_sbx = st.selectbox('Select an Entrant', names, placeholder='Entrant Name',)







if name_sbx != 'Entrant Name':
    df = df.query("Name == '{}'".format(name_sbx))

    g1 = df[['Rank','Entry','Name','Golfer 1','R1','R2','R3','R4', 'Tot','row_num']]
    g2 = df[['Rank','Entry','Name','Golfer 2','R1.1','R2.1','R3.1','R4.1','Tot.1','row_num']]
    g3 = df[['Rank','Entry','Name','Golfer 3','R1.2','R2.2','R3.2','R4.2','Tot.2','row_num']]
    g4 = df[['Rank','Entry','Name','Golfer 4','R1.3','R2.3','R3.3','R4.3','Tot.3','row_num']]
    g5 = df[['Rank','Entry','Name','Golfer 5','R1.4','R2.4','R3.4','R4.4','Tot.4','row_num']]
    g6 = df[['Rank','Entry','Name','Golfer 6','R1.5','R2.5','R3.5','R4.5','Tot.5','row_num']]

    entries = pd.DataFrame(np.vstack([g1,g2,g3,g4,g5,g6]), columns=g1.columns)

    entries.rename(columns={'Golfer 1':'Golfer'},inplace=True)
    entries.sort_values(by=['row_num','Tot'],inplace=True)
    st.subheader('Entries')
    entries = entries.reset_index()
    entries = entries.drop(columns=['index','row_num','Name'])
    st.dataframe(entries,hide_index=True)

else:


    rds = ['R1','R2','R3','R4',
        'R1.1','R2.1','R3.1','R4.1','R1.2',
        'R2.2','R3.2','R4.2','R1.3','R2.3',
        'R3.3','R4.3','R1.4','R2.4','R3.4',
        'R4.4','R1.5','R2.5','R3.5','R4.5']

    df_style = df.style\
        .applymap(cell_color_rd,subset=rds,)\
        .highlight_null('white')
    st.subheader('Standings')
    df_style





