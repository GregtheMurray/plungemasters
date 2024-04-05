import streamlit as st
import pandas as pd
import numpy as np
import matplotlib
url = 'https://docs.google.com/spreadsheets/d/1VKIpC91WmA7jIms8AMakdqYSvz4QKerIcYThkF9rzok/export?format=csv&id=1VKIpC91WmA7jIms8AMakdqYSvz4QKerIcYThkF9rzok&gid=448313398'




@st.cache_data
def get_data(url):
    df = pd.read_csv(url)
    return df

rd_min = 63
rd_max = 81



rds = ['R1','R2','R3','R4',
    'R1.1','R2.1','R3.1','R4.1','R1.2',
    'R2.2','R3.2','R4.2','R1.3','R2.3',
    'R3.3','R4.3','R1.4','R2.4','R3.4',
    'R4.4','R1.5','R2.5','R3.5','R4.5']
#old conditional formatting
# def cell_color_rd(rd_val):
#     par =72
#     if rd_val == par:
#         color = '#edede9'
#     elif rd_val < par:
#         color = '#2a9d8f'
#     else:
#         color = '#f4a261'
#     return 'background-color: %s' % color



hcol1,hcol2 = st.columns([.2,.8])
with hcol1:
    st.image('https://upload.wikimedia.org/wikipedia/commons/c/c5/Masters_Tournament.svg')
with hcol2:
    st.title('Masters Leaderboard')


df = get_data(url)
df['row_num'] = df.reset_index().index
df['Name'] = df['Name'].str.strip()
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

    st.subheader('Entries')
    entries = df[['Rank', 'Entry','Total',]]  
    st.dataframe(entries,hide_index=True)
   
    entries_d = pd.DataFrame(np.vstack([g1,g2,g3,g4,g5,g6]), columns=g1.columns)

    entries_d.rename(columns={'Golfer 1':'Golfer'},inplace=True)
    entries_d.sort_values(by=['row_num','Tot'],inplace=True)
   
   
    st.subheader('Entry Details')

    entries_d = entries_d.reset_index()
    entries_d = entries_d.drop(columns=['index','row_num','Name'])
    # st.dataframe(entries_d,hide_index=True)

    
    # Entry 1
    d0 = entries_d.query("Entry == '{}'".format(entries['Entry'].iloc[0]))
    d0.drop(columns=['Entry','Rank'], inplace = True)
    st.write('**' + entries['Entry'].iloc[0] + '** | Rank: **' + entries['Rank'].iloc[0] + '** | Total: **' + str(entries['Total'].iloc[0]) + '**')
    d0 = d0.style.background_gradient(cmap='coolwarm',subset=rds[:4],vmin = rd_min, vmax=rd_max).highlight_null('white')
    st.dataframe(d0,hide_index=True)

    try:
    # Entry 2
        d1 = entries_d.query("Entry == '{}'".format(entries['Entry'].iloc[1]))
        d1.drop(columns=['Entry','Rank'], inplace = True)
        st.write('**' + entries['Entry'].iloc[1] + '** | Rank: **' + entries['Rank'].iloc[1] + '** | Total: **' + str(entries['Total'].iloc[1]) + '**')
        d1 = d1.style.background_gradient(cmap='coolwarm',subset=rds[:4],vmin = rd_min, vmax=rd_max).highlight_null('white')
        st.dataframe(d1,hide_index=True)
    except: 
        pass 

    try:
    # Entry 3
        d2 = entries_d.query("Entry == '{}'".format(entries['Entry'].iloc[2]))
        d2.drop(columns=['Entry','Rank'], inplace = True)
        st.write('**' + entries['Entry'].iloc[2] + '** | Rank: **' + entries['Rank'].iloc[2] + '** | Total: **' + str(entries['Total'].iloc[2]) + '**')
        d2 = d2.style.background_gradient(cmap='coolwarm',subset=rds[:4],vmin = rd_min, vmax=rd_max).highlight_null('white')
        st.dataframe(d2,hide_index=True)
    except: 
        pass 

    try:
    # Entry 4
        d3 = entries_d.query("Entry == '{}'".format(entries['Entry'].iloc[3]))
        d3.drop(columns=['Entry','Rank'], inplace = True)
        st.write('**' + entries['Entry'].iloc[3] + '** | Rank: **' + entries['Rank'].iloc[3] + '** | Total: **' + str(entries['Total'].iloc[3]) + '**')
        d3 = d3.style.background_gradient(cmap='coolwarm',subset=rds[:4],vmin = rd_min, vmax=rd_max).highlight_null('white')
        st.dataframe(d3,hide_index=True)
    except: 
        pass 

    try:
    # Entry 5
        d4 = entries_d.query("Entry == '{}'".format(entries['Entry'].iloc[4]))
        d4.drop(columns=['Entry','Rank'], inplace = True)
        st.write('**' + entries['Entry'].iloc[4] + '** | Rank: **' + entries['Rank'].iloc[4] + '** | Total: **' + str(entries['Total'].iloc[4]) + '**')
        d4 = d4.style.background_gradient(cmap='coolwarm',subset=rds[:4],vmin = rd_min, vmax=rd_max).highlight_null('white')
        st.dataframe(d4,hide_index=True)
    except: 
        pass 


else:

    df.drop(columns=['row_num'], inplace=True)
    df_style = df.style\
            .background_gradient(cmap='coolwarm',subset=rds,vmin = 63,vmax=81)\
            .highlight_null('white')

    st.subheader('Standings')
    
    st.dataframe(df_style, hide_index=True)





