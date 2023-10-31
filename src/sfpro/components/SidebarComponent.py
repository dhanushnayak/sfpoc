import streamlit as st
from .RT_Component import RT_Info_St_Component
from .User_Component import User_Info_St_Component

class SidebarComp:
    def __init__(self) -> None:
           pass
        

    def page_sidebar(self,malls=[],category=[]):
        with st.sidebar: 
                    
                    self.based_on  = st.selectbox(
                            'Based on ?',
                            ['price','quantity'])
        
                
                    self.category_of_matrix = st.multiselect(
                            'Category On?',
                            category,['all'])
                    
                    self.wise_on = st.select_slider(
                           "Wise On?",
                           ['Days','Weeks','Months',"Years"]
                    )
                    self.mode_of_matrix = st.selectbox(
                            'Matrix on?',
                            ['mean','max','min'])
                    
                    self.pattern_option = st.selectbox('PATTERN PLOT',options=['Accumulator','Difference']) 

                    __,col1 = st.columns([0.6,0.4])
                    with col1:
                        self.forecast_premium = st.toggle("Forecast")