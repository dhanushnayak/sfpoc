import pandas as pd
from sfpro.config.Configuration import Configure

class Transform:
    def  __init__(self,df:pd.DataFrame,table_name:str) -> None:
        self.df = df
        self.table_name = table_name
    
    def convert_colums_type(self):
        self._params = Configure().get_datatype_columns(process='COVERT_COLUMNS',table_name=self.table_name)
        for i in self.df.columns:
            if i in self._params:
                if self._params[i]=='int':
                    self.df[i] = self.df[i].astype('int')
                if self._params[i]=='str':
                    self.df[i] = self.df[i].astype('str')
                if self._params[i]=='float':
                    self.df[i] = self.df[i].astype('float')
                if self._params[i]=='date':
                    self.df[i] = pd.to_datetime(self.df[i])
        return self.df


