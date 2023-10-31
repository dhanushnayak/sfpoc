import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from sfpro.pipeline.Malls import Mall_info
from .utils.utils import *

class RT_Info_St_Component:
    def __init__(self,rt: Mall_info) -> None:
        self.rt = rt
        self.pattern_option =  'Accumulator'
        self.viewc_value = "D"
        self.wise_mapper = {"Days":"D",'Months':"M","Years":"Y",'Weeks':"W"}

    def get_malls(self):
        return self.rt.get_mall_name()
    
    def get_categories(self):
        return self.rt.get_categories()

    def compare_plot(self,based_on='price',category=['all'],mode='mean'):
        with st.container():
            dfp =  self.rt.Compare_analysis(based_on=based_on,mode=mode)
            fig = px.pie(dfp, values=dfp.name,names=dfp.index,
                        height=400, width=200,hole=0.8,title=f"{str(based_on).capitalize()}-focused shopping center overview")
            fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
            st.plotly_chart(fig, use_container_width=True)

    def plot_diagram(self,based_on,category_of_matrix,mode_of_matrix,wise_on,pattern_option):
                if based_on=='price':
                    kl = self.rt.Price_df(category=category_of_matrix,
                                        mode=mode_of_matrix,
                                        wise_on = wise_on,
                                        pattern_option=pattern_option)
                if based_on=='quantity':
                    kl = self.rt.Quantity_df(category=category_of_matrix,
                                            mode=mode_of_matrix,
                                            wise_on = wise_on,
                                            pattern_option=pattern_option)
                fig =  px.area(kl,height=400,width=200)
                st.plotly_chart(fig, use_container_width=True)

    def matrix_plot_mall_category(self,based_on,category_of_matrix,mode_of_matrix,wise_on,pattern_option):
        
        with st.container():
            st.subheader(f"""
                             P&L Chart 
                             """,divider='rainbow')
            with st.container():
                with st.expander("Report"):
                    clm1,clm2 = st.columns(2)
                    with clm1:
                        kl1 = self.rt.Matrix_df(category=category_of_matrix,
                                                    based_on=based_on,
                                                    mode_of_matrix=mode_of_matrix,
                                                    wise_on=wise_on,
                                                    pattern=pattern_option,
                                                    group_on='mall'
                                                    )
                        try:
                            if len(kl1)>0:
                                kl1 = kl1.reset_index()
                                kl1 = kl1.rename(columns={0:'value'})
                                kl1['status'] = np.where(kl1['value']>0,'gain','loss')
                                fig = px.bar(kl1,x='SHOPPING_MALL',y='value',color='status', color_discrete_map={
                                'loss': 'red',
                                'gain': 'green'
                            },title=f"{wise_on}-wise {based_on} PL of shopping center")
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.markdown("** NO DATA FOUND **")
                        except:
                            pass
                    with clm2:
                        kl2 = self.rt.Matrix_df(category=category_of_matrix,
                                                    based_on=based_on,
                                                    mode_of_matrix=mode_of_matrix,
                                                    wise_on=wise_on,
                                                    pattern=pattern_option,
                                                    group_on='category'
                                                    )
                        try:
                            if len(kl2)>0:
                                kl2 = kl2.reset_index()
                                kl2 = kl2.rename(columns={0:'value'})
                                kl2['status'] = np.where(kl2['value']>0,'gain','loss')
                                fig = px.bar(kl2,x='CATEGORY',y='value',color='status', color_discrete_map={
                                'loss': 'red',
                                'gain': 'green'
                            },title=f"{wise_on}-wise {based_on} PL on category")
                                st.plotly_chart(fig, use_container_width=True)
                            else:
                                st.markdown("** NO DATA FOUND **")
                        except:
                            pass
                 
    def get_matrix_all(self,mall='all',based_on='price',wise_on='D'):
        rtk = self.rt.get_all_data(mall=mall,wise_on=wise_on)
        with st.container():
            col1, col2 = st.columns(2)
            col1.metric(label=' Gross Income',value=f"₹{rtk['total_price']}",delta=f" {rtk['incp']} %")
            col2.metric(label=' Integral Transaction ',value=f"{rtk['total_transaction']}",delta=f" {rtk['qncp']} %")
        
        with st.container():
                try:
                    if based_on=='price':rdk = rtk['pdfs']
                    if based_on=='quantity':rdk = rtk['qdfs']
                    fig =  px.bar(rdk,height=400,width=400,title=f"Category Based - {str(based_on).capitalize()} Accumulated ")
                    st.plotly_chart(fig, use_container_width=True)
                except:
                    st.markdown("** No Enough Data Found ** ")

        

    def price_quantity_plot(self,based_on,category_of_matrix,mode_of_matrix,wise_on):
        with st.container():
            self.plot_diagram(
                      based_on=based_on,
                      category_of_matrix=category_of_matrix,
                      mode_of_matrix=mode_of_matrix,
                      wise_on=wise_on,
                      pattern_option=self.pattern_option
                 )
            
            

    def rt_dashboard_template(self,based_on,category_of_matrix,mode_of_matrix,wise_on):
        with st.container():
            st.subheader(f"""
                             Shopping Center Overview
                             """,divider='rainbow')
            with st.container():
                with st.expander("Report"):
                    ccon1,ccon2 = st.columns([0.4,0.6])
                    with ccon1:
                        self.compare_plot(based_on=based_on,
                                                mode=mode_of_matrix)
                        
                    with ccon2: 
                        self.get_matrix_all(mall='all',
                                            based_on=based_on,
                                            wise_on=self.wise_mapper[wise_on])

                    self.price_quantity_plot(based_on=based_on,
                                                        category_of_matrix=category_of_matrix,
                                                        mode_of_matrix=mode_of_matrix,wise_on=self.wise_mapper[wise_on])
                
            self.matrix_plot_mall_category(based_on=based_on,
                             category_of_matrix=category_of_matrix,
                             mode_of_matrix=mode_of_matrix,
                             wise_on=self.wise_mapper[wise_on],
                             pattern_option=self.pattern_option
                             )