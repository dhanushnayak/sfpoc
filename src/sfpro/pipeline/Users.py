import pandas as pd
from .RT import RT_info

class User_info(RT_info):
    def __init__(self,df,name=['all']) -> None:
        self.name = name
        if len(name)>1 and 'all' in name: name.remove('all')
        elif len(name)==1 and 'all' in name: 
            name = list(df['SHOPPING_MALL'].unique())
            self.name =  'all'
        self.df = df[df['SHOPPING_MALL'].isin(name)]
        super().__init__(self.df)

    def Top_Users(self,based_on,category,mode='mean',top=10):
        if 'all' in category and len(category)==1: category = self.get_categories()
        if len(category)>1 and 'all' in category: category.remove('all')
        tmp = self.df[self.df['CATEGORY'].isin(category)].groupby(['CUSTOMER_ID','CATEGORY'])[str(based_on).upper()]
        if mode=='mean': tmp = tmp.mean().unstack()
        if mode=='min': tmp =  tmp.min().unstack()
        if mode=='max': tmp =  tmp.max().unstack()
        tmp =  tmp.fillna(0)
        tmp['tol'] = tmp.sum(axis=1)
        tmp = tmp.sort_values(by='tol',ascending=False)[:top]
        tmp = tmp.loc[:,~tmp.columns.isin(['tol'])]
        return tmp
    
    def Age_Users(self,based_on,category,mode='mean'):
        if 'all' in category and len(category)==1: category = self.get_categories()
        if len(category)>1 and 'all' in category: category.remove('all')   
        tmp = self.df[self.df['CATEGORY'].isin(category)].groupby(['AGE','CATEGORY'])[str(based_on).upper()]
        if mode=='mean': tmp = tmp.mean().unstack()
        if mode=='min': tmp =  tmp.min().unstack()
        if mode=='max': tmp =  tmp.max().unstack()
        return tmp#.sort_values(ascending=False)
    
    def Gender_Users(self,based_on,category,mode='mean'):
        if 'all' in category and len(category)==1: category = self.get_categories()
        if len(category)>1 and 'all' in category: category.remove('all') 
        tmp = self.df[self.df['CATEGORY'].isin(category)].groupby(['GENDER','CATEGORY'])[str(based_on).upper()]
        if mode=='mean': tmp = tmp.mean().unstack()
        if mode=='min': tmp =  tmp.min().unstack()
        if mode=='max': tmp =  tmp.max().unstack()
        tmp = tmp.unstack().reset_index()
        tmp['index']=tmp['GENDER']+'-'+tmp['CATEGORY']
        tmp = tmp.rename(columns={0:'value'})
        return tmp

    





