import streamlit as st
import numpy as np
import pandas as pd
#import pandas_profiling
#from streamlit_pandas_profiling import st_profile_report
from termcolor import colored
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
from snowflake.snowpark.functions import udf,sproc
from src.sfpro.utils.comman import *
from src.sfpro.pipeline.SessionBuilder import SessionCreated
from src.sfpro.pipeline.DataClean import Transform
from src.sfpro.pipeline.DataFetcher import DataFetch
from src.sfpro.config.Configuration import Configure
from src.sfpro.pipeline.Malls import Mall_info
from src.sfpro.pipeline.Users import User_info
from src.sfpro.pipeline.Forecaster import Forecast_info
from src.sfpro.components.Dashboard import Dashboard_build
from src.sfpro.components.User_Component import User_Info_St_Component

# Session Creation
#session = SessionCreated("normal").build()


########################################################################################################################

st.set_page_config(
    page_title="RT",
    page_icon='shark',
    layout='wide')

######################################################################################################################
style_data = os.path.join(os.path.dirname(__file__),'style/styles.css')
with open(style_data) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


############################################################################################################################


st.header("RT ANALYSIS")

table_names_mapper = {
    'All':"RETAIL_TRANSACTION",
     'CEVAHIR_AVM_TABLE':"CEVAHIR_AVM_TABLE",
     'EMAAR_SQUARE_MALL_TABLE':'EMAAR_SQUARE_MALL_TABLE', 
     'FORUM_ISTANBUL_TABLE':'FORUM_ISTANBUL_TABLE', 
     'ISTINYE_PARK_TABLE':'ISTINYE_PARK_TABLE', 
     'KANYON_TABLE':'KANYON_TABLE', 
     'MALL_OF_ISTANBUL_TABLE':'MALL_OF_ISTANBUL_TABLE', 
     'METROCITY_TABLE':'METROCITY_TABLE', 'METROPOL_AVM_TABLE':'METROPOL_AVM_TABLE', 
     'ZORLU_CENTER_TABLE':'ZORLU_CENTER_TABLE', 
     'VIAPORT_OUTLET_TABLE':'VIAPORT_OUTLET_TABLE',
}


################################################################################################################################
################################################################################################################################################################


session = SessionCreated('normal').build()

dft = DataFetch(session=session)
tables = ['All']
tables.extend(dft.get_all_mall_table())
with st.sidebar:
    table_name  = st.selectbox(
                           "Selected Mall",
                           tables,
                    )
    table_name = table_names_mapper[table_name]


df = dft.table(table_name=table_name)

df = Transform(df,table_name='BASIC').convert_colums_type()

mall_info  = Mall_info(df)
user_info = User_info(df)
fore_info =  Forecast_info(session=session)

dash = Dashboard_build(mall_rt=mall_info,user_rt=user_info,fore_rt=fore_info)
dash.build()
