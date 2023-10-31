import pandas as pd
import streamlit as st
import plotly.express as px
from sfpro.pipeline.Users import User_info

class User_Info_St_Component:
    def __init__(self,rt: User_info) -> None:
        self.rt1 = rt

    def top_customer(self,based_on,
                    category_of_matrix,
                    mode_of_matrix):
        tp = self.rt1.Top_Users(based_on=based_on,
                                category=category_of_matrix,
                                mode=mode_of_matrix)
        fig = px.bar(tp,
                    height=400, width=200,title='Top Contributors',orientation='h')
        st.plotly_chart(fig, use_container_width=True)

    def age_based(self,based_on,
                    category_of_matrix,
                    mode_of_matrix):
        ap = self.rt1.Age_Users(based_on=based_on,
                                category=category_of_matrix,
                                mode=mode_of_matrix)
        fig = px.bar(ap,
                    height=400, width=200,title='Age-Related Patterns')
        st.plotly_chart(fig, use_container_width=True)

    def gender_based(self,based_on='price',category_of_matrix=['all'],mode_of_matrix='mean'):
        ap = self.rt1.Gender_Users(based_on=based_on,
                                category=category_of_matrix,
                                mode=mode_of_matrix)
        fig = px.pie(ap, values='value',names='index',
                    height=400, width=200,hole=0.8,title='Gender-Related Patterns')
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
        st.plotly_chart(fig, use_container_width=True)
        

    def user_dashboard(self,based_on,
                            category_of_matrix,
                            mode_of_matrix):
        
        with st.container():
            st.subheader(f"""
                             User Based Analysis
                             """,divider='rainbow')
            with st.container():
                with st.expander(label="Report"):
                    c1,c2 = st.columns(2)
                    with c1:
                        with st.container():
                            self.gender_based(
                            based_on=based_on,
                            category_of_matrix=category_of_matrix,
                            mode_of_matrix=mode_of_matrix
                            )
                        
                    with c2: 
                        with st.container():
                            self.top_customer(based_on=based_on,
                                                category_of_matrix=category_of_matrix,
                                                mode_of_matrix=mode_of_matrix)
                
                    with st.container():
                            self.age_based(based_on=based_on,
                                                category_of_matrix=category_of_matrix,
                                                mode_of_matrix=mode_of_matrix)

    
