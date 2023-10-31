import streamlit as st
import pandas as pd
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
from ..utils.comman import collection_to_list

class DataFetch:
    def __init__(self,session:Session) -> None:
        self.session = session

    def get_all_mall_table(self):
        @st.cache_data
        def get_tables():
            return collection_to_list(self.session.sql("select table_name from information_schema.tables where table_name like '%_TABLE';").collect())
        return get_tables()

    def table(self,table_name:str):
        @st.cache_data
        def get_data(table):
            return self.session.sql(f"SELECT * FROM {table}").to_pandas()
        
        return get_data(table=table_name)

    def build_model(self,table_name:str,category:str,days:int):
        data  = self.session.call('train_model_and_save',table_name,category,days)
        if data:
            model_name =  f'predict_xgb_{str(table_name).lower()}_{str(category).lower()}.joblib'
            res = self.session.sql(f"list @ML_MODELS pattern = '.*{model_name}'").collect()
            if len(res)>0: return True
            else: return False
        else:
            return False

    def forecast_fetcher_data(self,table_name:str,category:str,days:int):
        def collection_to_list(rows:list=None) -> list:
            return [list(i.as_dict().values())[0] for i in rows]
        @st.cache_data
        def get_data_fore(table,category,days):
            query_last = f"SELECT INVOICE_DATE FROM {table};"
            resq = collection_to_list(self.session.sql(query_last).collect())[-1]
            future_dates = pd.date_range(start=pd.to_datetime(resq) + pd.Timedelta(days=1), periods=days)
            if category!='all':
                #data = self.session.sql(f'SELECT "{str(category)}" FROM {str(table).strip()}').to_pandas()
                data = self.session.table(table).select(col("INVOICE_DATE"),col(f'"{category}"')).to_pandas()
                predicts = eval(self.session.call("predict_model",table,category,days))
                predicts_df = pd.DataFrame({"INVOICE_DATE":future_dates,"FORECAST":predicts})
                model_name =  f'predict_xgb_{str(table_name).lower()}_{str(category).lower()}.joblib'
                res = self.session.sql(f"list @ML_MODELS pattern = '.*{model_name}'").collect()
                if len(res)>0:
                    time_of_model = "Model created on "+str(res[0]['last_modified'])
                else:
                    time_of_model = "Model not found"
            else:
                data  = self.session.table(table).to_pandas()
                predicts = [0]*days
                predicts_df = pd.DataFrame({"INVOICE_DATE":future_dates,"FORECAST":predicts})
                time_of_model = "Model not found"
            data['INVOICE_DATE'] = pd.to_datetime(data['INVOICE_DATE'])
            return {"data":data,'predicts':predicts_df,"time_of_model":time_of_model}
        
        data_r =  get_data_fore(table_name,category=category,days=days)
        return data_r