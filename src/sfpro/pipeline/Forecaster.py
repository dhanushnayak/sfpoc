from snowflake.snowpark.session import Session
from .DataFetcher import DataFetch


class Forecast_info(DataFetch):
    def __init__(self,session=Session) -> None:
       self.fetcher = super().__init__(session=session)

    def forecast(self, table_name:str,category:str,based_on:str,days:int):
        table_name  = str(table_name).upper().replace(" ","_")+"_DAYWISE"
        if category!='all':category = category+'_'+str(based_on).upper()
        else: category = "TOTAL"+'_'+str(based_on).upper()
        dataframe = self.forecast_fetcher_data(table_name=table_name,category=category,days=days)
        return {"df":dataframe['data'],"category_name":category,'time_of_model':dataframe['time_of_model'],'predicts':dataframe['predicts']}
        
    def build_forecast(self, table_name:str,category:str,based_on:str,days:int):
        table_name  = str(table_name).upper().replace(" ","_")+"_DAYWISE"
        category = category+'_'+str(based_on).upper()
        status = self.build_model(table_name=table_name,category=category,days=days)
        return status
