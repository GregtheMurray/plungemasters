import streamlit as st
import pandas as pd
import numpy as np
import datetime
from  matplotlib.colors import LinearSegmentedColormap

#set colormap for gradients
cmap=LinearSegmentedColormap.from_list('rg',["#ff006e", "w", "#0a9396"], N=256) 

def roundDownDateTime(dt):
    delta_min = dt.minute % 5
    return datetime.datetime(dt.year, dt.month, dt.day,
                             dt.hour, dt.minute - delta_min)


@st.cache_data
def get_data(url,timestamp):
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
        mtext = """:gray[*Tiebreaker 1 (Champ Score): {}  |  Tiebreaker 2 (Low Am Score): {}*]""".format(str(df['T1'].iloc[entry_num]),
                                                                                                  str(df['T2'].iloc[entry_num]))
        st.markdown(mtext)
        st.markdown('##')
    except : 
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

hcol1,hcol2 = st.columns([.2,.8])
with hcol1:
    st.image('https://upload.wikimedia.org/wikipedia/commons/c/c5/Masters_Tournament.svg')
with hcol2:
    st.title('Masters Leaderboard')


df = get_data(url,roundDownDateTime(pd.Timestamp.now()))
df['row_num'] = df.reset_index().index
df['Entry'] = df['Entry'].str.strip(' ')
df['Entry'] = df['Entry'].str.replace("'",'')

# Data Prep
 
#Create Entry Details 
g1 = df[['Rank','Entry','Name','Pos', 'Golfer 1','Today','Thru','Score','R1','R2','R3','R4', 'Tot','row_num','Total']]
g2 = df[['Rank','Entry','Name','Pos.1','Golfer 2','Today.1','Thru.1','Score.1','R1.1','R2.1','R3.1','R4.1','Tot.1','row_num','Total']]
g3 = df[['Rank','Entry','Name','Pos.2','Golfer 3','Today.2','Thru.2','Score.2','R1.2','R2.2','R3.2','R4.2','Tot.2','row_num','Total']]
g4 = df[['Rank','Entry','Name','Pos.3','Golfer 4','Today.3','Thru.3','Score.3','R1.3','R2.3','R3.3','R4.3','Tot.3','row_num','Total']]
g5 = df[['Rank','Entry','Name','Pos.4','Golfer 5','Today.4','Thru.4','Score.4','R1.4','R2.4','R3.4','R4.4','Tot.4','row_num','Total']]
g6 = df[['Rank','Entry','Name','Pos.5','Golfer 6','Today.5','Thru.5','Score.5','R1.5','R2.5','R3.5','R4.5','Tot.5','row_num','Total']]

#clean up 
entries_d = pd.DataFrame(np.vstack([g1,g2,g3,g4,g5,g6]), columns=g1.columns)
entries_d.rename(columns={'Golfer 1':'Golfer'},inplace=True)
entries_d.sort_values(by=['row_num','Tot',],inplace=True)

# group Golfers in to lists per entry
entry_golfer_list = entries_d.groupby(['Rank','Entry','Total','row_num'])['Golfer'].apply(list).reset_index()


tab1, tab2 = st.tabs(['Leaderboard','Similar Entries'])


with tab1:
    names = sorted(list(df['Name'].unique()))
    names.insert(0,'All Entries (Defualt)')
    name_sbx = st.selectbox('Select an Entrant', names, placeholder='All Entries (Defualt)',)

    if name_sbx != 'All Entries (Defualt)':
        entries = df.query("Name == '{}'".format(name_sbx))
        details = entries_d.query("Name == '{}'".format(name_sbx))


        st.subheader('Entries')
        entries = entries[['Rank', 'Entry','Total','T1','T2']]  
        show_entries = entries[['Rank', 'Entry','Total',]]  
        st.dataframe(show_entries,hide_index=True)
    
        st.subheader('Entry Details')

        # entry detail data prep
        details = details.reset_index()
        details = details.drop(columns=['index','row_num','Name'])

        # display entries
        for i in range(4):
            format_entry(entries, details,i)


    else:
        # Data Detail options
        with st.expander('Data Display Options'):
            with st.container(border=True):
                det_rad = st.radio('Standing Detail Level',
                                options=['Scores','Golfers','Rounds'],
                                captions=['Entry Scores', f'+ Golfer Scores', f'+ Golfer Round Scores'])
        # Standings
        st.subheader(':trophy: Standings')
        df.drop(columns=['row_num'], inplace=True)

        if det_rad == 'Scores': 
            df_style = df[['Rank','Entry','Total','T1','T2']]
        elif det_rad == 'Golfers':
            df_style = df[['Rank','Entry','Total','Golfer 1','Score',
                        'Golfer 2','Score.1','Golfer 3','Score.2',
                        'Golfer 4','Score.3','Golfer 5','Score.4',
                        'Golfer 6','Score.5','T1','T2']]
        else:
            df.drop(columns=['Name'], inplace=True)
            df_style = df.style\
                .background_gradient(cmap=cmap,subset=rds,vmin = rd_min,vmax=rd_max)\
                .highlight_null('white')

            
            
        st.dataframe(df_style, hide_index=True)

with tab2:
    entry_list = sorted(list(entry_golfer_list['Entry']))
    sbx_entry = st.selectbox('Choose an Entry',entry_list, placeholder='Entry Name')
    
    if sbx_entry != 'Entry Name':
        sel_entry = entry_golfer_list.query("Entry == '{}'".format(sbx_entry))
        compare_entries = entry_golfer_list.query("Entry != '{}'".format(sbx_entry))
        sim_df = pd.DataFrame()
        for idx, row in compare_entries.iterrows():

            entry_list = set(sel_entry['Golfer'].iloc[0])
            compare_list = set(row['Golfer'])
            common = list(entry_list & compare_list)
            different = compare_list - entry_list
            row['count_sim'] = len(common)
            row['common'] = sorted(common)
            row['different'] = sorted(different)

            row = pd.DataFrame(row).transpose()

            sim_df = pd.concat([sim_df,row], ignore_index=True)

    
        
        golfer_str =''
        for n, golfer in enumerate(sorted(sel_entry['Golfer'].iloc[0])):
            if n == 5:
                golfer_str += golfer
            else:
                golfer_str += golfer+ ', '
        with st.container(border=True):
            st.write('''Entry: **{}** | Rank: **{}** | Total: **{}**  
                    Golfers:  
                    {}'''.format(sel_entry['Entry'].iloc[0],
                                        sel_entry['Rank'].iloc[0],
                                        sel_entry['Total'].iloc[0],
                                        golfer_str ))
            
        g_sim = sim_df.groupby(['count_sim'])['row_num'].count().reset_index()

        g_sim['title'] = g_sim['count_sim'].astype(str) + ' Golfer(s)'
        g_sim = pd.pivot_table(g_sim,values=['row_num'],columns=['title'])
        g_sim = g_sim[g_sim.columns[::-1]]
        g_sim = g_sim.style.background_gradient(axis=1)\
                           .format(precision=0)
        
        
        
        
        st.write('**Entry Counts by # of Similar Golfers :golfer:**')
        st.dataframe(g_sim,hide_index=True)
        # st.bar_chart(g_sim,)

        with st.expander('See Entry Similarity Details'):
            sim_df.sort_values(['count_sim','row_num'],ascending =[False,True],inplace=True)
            sim_display = sim_df[['Rank','Entry','Total','count_sim','common','different']]
            st.dataframe(sim_display,hide_index=True)