import streamlit as st
import pandas as pd
import numpy as np
from  matplotlib.colors import LinearSegmentedColormap

#set colormap for gradients
cmap=LinearSegmentedColormap.from_list('rg',["#ff006e", "w", "#0a9396"], N=256) 

@st.cache_data
def get_data(url):
    df = pd.read_csv(url)
    return df

def format_entry(df,df_detail,entry_num):
    try:
        out = df_detail.query("Entry == '{}'".format(df['Entry'].iloc[entry_num]))
        out.drop(columns=['Entry','Rank','Total'], inplace = True)
        st.write('**' + df['Entry'].iloc[entry_num] + '** | Rank: **' + df['Rank'].iloc[entry_num]\
                + '** | Total: **' + str(df['Total'].iloc[entry_num]) + '**')
        out = out.style.background_gradient(cmap=cmap,subset=rds[:4],vmin = rd_min, vmax=rd_max).highlight_null('white')
        st.dataframe(out,hide_index=True)
    except:
        pass

#Set Page config
def page_config_default():
    st.set_page_config(layout='wide',initial_sidebar_state='collapsed',page_icon="⛳") 
                       
page_config_default()                     

#Disable table hovers
st.markdown(
                """
                <style>
                [data-testid="stElementToolbar"] {
                    display: none;
                }
                </style>
                """,
                unsafe_allow_html=True
            ) 


url = 'https://docs.google.com/spreadsheets/d/1VKIpC91WmA7jIms8AMakdqYSvz4QKerIcYThkF9rzok/export?format=csv&id=1VKIpC91WmA7jIms8AMakdqYSvz4QKerIcYThkF9rzok&gid=448313398'

rd_min = 63
rd_max = 81

rds = ['R1','R2','R3','R4',
    'R1.1','R2.1','R3.1','R4.1','R1.2',
    'R2.2','R3.2','R4.2','R1.3','R2.3',
    'R3.3','R4.3','R1.4','R2.4','R3.4',
    'R4.4','R1.5','R2.5','R3.5','R4.5']






### Page Start ###
with st.sidebar:
    st.write('**Options**')
    with st.container(border=True):
        det_rad = st.radio('Standing Detail Level',options=['Scores','Golfers','Rounds'], captions=['Entry Scores', '\+ Golfer Scores', '\+ Golfer Round Scores'])


hcol1,hcol2 = st.columns([.2,.8])
with hcol1:
    st.image('https://upload.wikimedia.org/wikipedia/commons/c/c5/Masters_Tournament.svg')
with hcol2:
    st.title('Masters Leaderboard')


df = get_data(url)
df['row_num'] = df.reset_index().index
df['Name'].str.strip()

names = sorted(list(df['Name'].unique()))
names.insert(0,'Entrant Name')
name_sbx = st.selectbox('Select an Entrant', names, placeholder='Entrant Name',)


#Create Entry Details 
g1 = df[['Rank','Entry','Name','Golfer 1','R1','R2','R3','R4', 'Tot','row_num','Total']]
g2 = df[['Rank','Entry','Name','Golfer 2','R1.1','R2.1','R3.1','R4.1','Tot.1','row_num','Total']]
g3 = df[['Rank','Entry','Name','Golfer 3','R1.2','R2.2','R3.2','R4.2','Tot.2','row_num','Total']]
g4 = df[['Rank','Entry','Name','Golfer 4','R1.3','R2.3','R3.3','R4.3','Tot.3','row_num','Total']]
g5 = df[['Rank','Entry','Name','Golfer 5','R1.4','R2.4','R3.4','R4.4','Tot.4','row_num','Total']]
g6 = df[['Rank','Entry','Name','Golfer 6','R1.5','R2.5','R3.5','R4.5','Tot.5','row_num','Total']]

entries_d = pd.DataFrame(np.vstack([g1,g2,g3,g4,g5,g6]), columns=g1.columns)
entries_d.rename(columns={'Golfer 1':'Golfer'},inplace=True)
entries_d.sort_values(by=['row_num','Tot',],inplace=True)

#Check for golfer list similarity
# entries_d.sort_values(by=['row_num','Golfer',],inplace=True)

# entries_test = entries_d.groupby(['Rank','Entry','Total'])['Golfer'].apply(list).reset_index()
# entries_string = entries_d.groupby(['Rank','Entry','Total'])['Golfer'].apply(','.join).reset_index()

# count_list = entries_string.groupby(['Golfer'])['Total'].count().reset_index()
# count_list


if name_sbx != 'Entrant Name':
    entries = df.query("Name == '{}'".format(name_sbx))
    details = entries_d.query("Name == '{}'".format(name_sbx))


    st.subheader('Entries')
    entries = entries[['Rank', 'Entry','Total',]]  
    st.dataframe(entries,hide_index=True)
   
    st.subheader('Entry Details')

    # entry detail data prep
    details = details.reset_index()
    details = details.drop(columns=['index','row_num','Name'])

    # display entries
    for i in range(4):
        format_entry(entries, details,i)


else:
    st.subheader(':trophy: Standings')
    df.drop(columns=['row_num'], inplace=True)

    if det_rad == 'Scores': 
        df_style = df[['Rank','Entry','Total']]
    elif det_rad == 'Golfers':
        df_style = df[['Rank','Entry','Total','Golfer 1','Tot',
                       'Golfer 2','Tot.1','Golfer 3','Tot.2',
                       'Golfer 4','Tot.3','Golfer 5','Tot.4',
                       'Golfer 6','Tot.5']]
    else:
        df_style = df.style\
            .background_gradient(cmap=cmap,subset=rds,vmin = rd_min,vmax=rd_max)\
            .highlight_null('white')

        
        
    st.dataframe(df_style, hide_index=True)