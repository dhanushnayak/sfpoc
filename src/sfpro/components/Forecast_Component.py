import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sfpro.pipeline.Forecaster import Forecast_info


class Forecast_St_Component:
    def __init__(self,rt: Forecast_info) -> None:
        self.rt2 = rt

    def forecast_plot(self,malls,category,based_on='price',premium=False):
        with st.container():
            st.subheader(f"""
                             Forecaster 
                             """,divider='rainbow')
            with st.container():
                with st.expander(label="Report"):
                    col1,col2,col3= st.columns([0.3,0.4,0.3])
                    with col1:
                        if isinstance(malls,list):
                            mall = st.selectbox("Malls",options=malls,index=None)
                        else:
                            mall = st.selectbox("Malls",options=[malls])
                    with col2:
                        categorys = st.selectbox("Category",options=category)
                    with col3:
                        days = st.slider('Days',0,14,(0,7))[1]

                    if mall is not None:
                        st.markdown(f'''
                        **Forecasting  for mall :orange[{mall}] - :blue[{categorys}] on :violet[{based_on}], for next :green[{days}]**
                        ''',)
                        data = self.rt2.forecast(table_name=mall,category=categorys,based_on=based_on,days = days)
                        with col3:
                            st.markdown(f'**{data["time_of_model"]}**')
                        fig =  px.line(data_frame=data['df'],x='INVOICE_DATE',y=data['category_name'],height=400,width=200)
                        fig2 = px.line(data_frame=data['predicts'],x='INVOICE_DATE',y="FORECAST",height=400,width=200,markers="--")
                        fig2 = go.Scatter(x=data['predicts']['INVOICE_DATE'],y=data['predicts']['FORECAST'],line = dict(color='firebrick', width=4, dash='dot'),name='Forecasts')
                        fig.add_trace(fig2)
                        st.plotly_chart(fig, use_container_width=True)
                        #st.plotly_chart(fig2, use_container_width=True)
                    else:
                        data = None
                        st.markdown("**Select the :violet[Mall] for forecasting**")
                    if premium:
                        col12,col22,col32= st.columns([0.3,0.5,0.2])
                        with col32:
                            try:
                                if data['time_of_model']=="Model not found": label_button='Build Model'
                                else: label_button = "Re-Build Model"
                            except:
                                label_button = "Build Model"
                            rebuild = st.button(label=label_button,type="primary")
                            if rebuild:
                                status = self.rt2.build_forecast(table_name=mall,category=categorys,based_on=based_on,days = days)
                                if status==True:
                                    st.success("Model built Successfully")
                                else:
                                    st.error("Model built crashed please contact the developer")
                                
                    


