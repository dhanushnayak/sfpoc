import streamlit as st
from .RT_Component import RT_Info_St_Component
from .User_Component import User_Info_St_Component
from .SidebarComponent import SidebarComp
from .Forecast_Component import Forecast_St_Component

class Dashboard_build(RT_Info_St_Component,User_Info_St_Component,SidebarComp,Forecast_St_Component):
    def __init__(self,mall_rt,user_rt,fore_rt) -> None:
        #super(RT_Info_St_Component,self).__init__(mall_rt)
        #super(User_Info_St_Component,self).__init__(user_rt)
        self.mall_rt = RT_Info_St_Component.__init__(self,mall_rt)
        self.user_rt = User_Info_St_Component.__init__(self,user_rt)
        self.sidebar_rt = SidebarComp.__init__(self)
        self.forecast_rt = Forecast_St_Component.__init__(self,fore_rt)


    def build(self):

        self.page_sidebar(malls=self.rt.get_mall_name(),category=self.rt.get_categories())
        
        self.rt_dashboard_template(based_on=self.based_on,
                                   category_of_matrix=self.category_of_matrix,
                                   mode_of_matrix=self.mode_of_matrix,wise_on=self.wise_on)
        
        self.user_dashboard(based_on=self.based_on,
                                   category_of_matrix=self.category_of_matrix,
                                   mode_of_matrix=self.mode_of_matrix)
        

        self.forecast_plot(malls=self.get_malls(),category=self.get_categories(),based_on=self.based_on,premium=self.forecast_premium)
