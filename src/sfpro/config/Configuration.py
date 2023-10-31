from sfpro.constants import CONFIG_FILE_PATH,DATABASE_FILE_PATH,TRANSFORM_FILE_PATH
from sfpro.utils.comman import read_yaml


class Configure:
    def __init__(self):
        self.config = CONFIG_FILE_PATH
        self.schema_config = DATABASE_FILE_PATH
        self.transform_config = TRANSFORM_FILE_PATH

    def get_params(self,user='superuser'):
        self._params = read_yaml(self.config)
        if user == 'normal':
            self.params =  self._params['SNOWFLAKE_USER']
        if user == "superuser":
            self.params =  self._params['SNOWFLAKE_SUPER_USER']
        return self.params
    
    def get_database(self,database='poc_db'):
        self._params  = read_yaml(self.schema_config)
        if database == "poc_db":
            self.get_database = self._params['POC_DB']
            return self._params
        
    def get_warehouse(self,warehouse_name='poc_wh'):
        self._params =  read_yaml(self.config)
        if warehouse_name == 'poc_wh':
            self.wh = self._params['warehouse']['poc_wh']
            return self.wh
        
    def get_datatype_columns(self,process='COVERT_COLUMNS',table_name='RETAIL_TRANSACTION'):
        self._params =  read_yaml(self.transform_config)
        if process=='COVERT_COLUMNS':
            self.trans = self._params['COVERT_COLUMNS'][table_name]
            return self.trans
            
