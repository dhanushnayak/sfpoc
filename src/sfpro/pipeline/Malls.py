import pandas as pd
from .RT import RT_info

class Mall_info(RT_info):
    def __init__(self,df,name=['all']) -> None:
        self.name = name
        if len(name)>1 and 'all' in name: name.remove('all')
        elif len(name)==1 and 'all' in name: 
            name = list(df['SHOPPING_MALL'].unique())
            self.name =  'all'
        self.df = df[df['SHOPPING_MALL'].isin(name)]
        super().__init__(self.df)

    def get_mall_name(self):
        if self.name == 'all': return list(self.df['SHOPPING_MALL'].unique())
        else: return self.name

    def Compare_analysis(self,based_on,mode='mean'):
        if self.name == 'all':
            tmp = self.df.groupby(['SHOPPING_MALL'])[str(based_on).upper()]
            if mode=='mean': tmp = tmp.mean()
            if mode=='min': tmp =  tmp.min()
            if mode=='max': tmp =  tmp.max()
            return tmp
        else:
            tmp = self.df.groupby(['CATEGORY'])[str(based_on).upper()]
            if mode=='mean': tmp = tmp.mean()
            if mode=='min': tmp =  tmp.min()
            if mode=='max': tmp =  tmp.max()
            return tmp





