import pandas as pd

class RT_info:
    def __init__(self,df:pd.DataFrame):
        self.df = df
        self.categories = ['all']
        self.malls = ['all']

    def get_all_data(self,mall='all',wise_on='D',mode_of_matrix='mean'):
          if mall=='all':df = self.df
          else: df = self.df[self.df['SHOPPING_MALL']==mall]
          total_transaction = len(df)
          total_price = df['PRICE'].sum()
          pdfs = df.groupby("CATEGORY")['PRICE'].sum().sort_values(ascending=False)
          qdfs = df.groupby("CATEGORY")['QUANTITY'].sum().sort_values(ascending=False)
          #df = df.set_index("INVOICE_PRICE")
          df['INVOICE_DATE'] = pd.to_datetime(df['INVOICE_DATE'])
          df = df.set_index("INVOICE_DATE")
          pdf = df['PRICE']
          qdf = df['QUANTITY']
          if mode_of_matrix=='mean': 
                pdf = pdf.resample(wise_on).mean()
                qdf = qdf.resample(wise_on).mean()
          if mode_of_matrix=='max': 
                    pdf = pdf.resample(wise_on).max()
                    qdf = qdf.resample(wise_on).max()
          if mode_of_matrix=='min': 
                    pdf = pdf.resample(wise_on).min()
                    qdf = qdf.resample(wise_on).min()

          qdf = qdf.fillna(0)
          pdf = pdf.fillna(0)
       
          try:
                inp =  round((pdf.tail(-2).iloc[1] - pdf.tail(-2).iloc[0])/pdf.tail(-2).iloc[0],2)*100
                qnp = round((qdf.tail(-2).iloc[1] - qdf.tail(-2).iloc[0])/qdf.tail(-2).iloc[0],2)*100
          except:
                inp,qnp = 0,0
                
          return {"total_price":round(total_price,1),"total_transaction": total_transaction,'pdfs':pdfs,'qdfs':qdfs,"incp":round(inp,1),"qncp":round(qnp,1)}

    def get_pl_matrix(self,wise='D',mode_of_matrix='mean'):
        qdf = self.df
        qdf['INVOICE_DATE'] = pd.to_datetime(qdf['INVOICE_DATE'])
        if mode_of_matrix=='mean': 
                #qdf = qdf.mean().unstack().reset_index().set_index("INVOICE_DATE")
                qdf = qdf.resample(wise).mean()
        if mode_of_matrix=='max': 
                #qdf = qdf.max().unstack().reset_index().set_index("INVOICE_DATE")
                qdf = qdf.resample(wise).max()
        if mode_of_matrix=='min': 
                #qdf = qdf.min().unstack().reset_index().set_index("INVOICE_DATE")
                qdf = qdf.resample(wise).min()
        return qdf
          
    def get_categories(self):
        self.categories.extend(list(self.df['CATEGORY'].unique()))
        return self.categories
    
    def preprocess_price_quantity(self,qdf,based_on='price',mode_of_matrix='mean',wise_on='D',pattern='Accumulator'):
        qdf['INVOICE_DATE'] = pd.to_datetime(qdf['INVOICE_DATE'])
        qdf = qdf.groupby(['INVOICE_DATE','CATEGORY'])[str(based_on).upper()]
        if mode_of_matrix=='mean': 
                qdf = qdf.mean().unstack().reset_index().set_index("INVOICE_DATE")
                qdf = qdf.resample(wise_on).mean()
        if mode_of_matrix=='max': 
                qdf = qdf.max().unstack().reset_index().set_index("INVOICE_DATE")
                qdf = qdf.resample(wise_on).max()
        if mode_of_matrix=='min': 
                qdf = qdf.min().unstack().reset_index().set_index("INVOICE_DATE")
                qdf = qdf.resample(wise_on).min()
        if pattern=='Difference': qdf=qdf-qdf.shift(1)
        qdf = qdf.fillna(0)
        return qdf
    
    def Price_df(self,category=['all'],mode='mean',wise_on='D',pattern_option='Accumulator'):
        category1 = category
        if 'all' in category1 and len(category1)==1: category1 = self.get_categories()
        elif len(category1)>1 and 'all' in category1: category1.remove('all')  
        else: category1 = category  
        pdf = self.df[self.df['CATEGORY'].isin(category1)]
        pdf = self.preprocess_price_quantity(pdf,based_on='price',mode_of_matrix=mode,wise_on=wise_on,pattern=pattern_option)
        del category1
        return pdf
    

    
    def Quantity_df(self,category='all',mode='mean',wise_on='D',pattern_option='Accumulator'):
        category1 = category
        if 'all' in category1 and len(category1)==1: category1 = self.get_categories()
        elif len(category1)>1 and 'all' in category1: category1.remove('all')
        else: category1 = category   
        qdf = self.df[self.df['CATEGORY'].isin(category1)]
        qdf = self.preprocess_price_quantity(qdf,based_on='quantity',mode_of_matrix=mode,wise_on=wise_on,pattern=pattern_option)
        del category1
        return qdf
    
    def Matrix_df(self,category='all',based_on='price',mode_of_matrix='mean',wise_on='D',pattern='Accumulator',group_on='mall'):
        def calculate_matrix(df):
             df = round((df.iloc[1]-df.iloc[0])/df.iloc[0],3) * 100
             return df
        category1 = category
        if 'all' in category1 and len(category1)==1: category1 = self.get_categories()
        elif len(category1)>1 and 'all' in category1: category1.remove('all')
        else: category1 = category   
        qdf = self.df[self.df['CATEGORY'].isin(category1)]

        qdf['INVOICE_DATE'] = pd.to_datetime(qdf['INVOICE_DATE'])

        if group_on=='mall': qdf = qdf.groupby(['INVOICE_DATE','SHOPPING_MALL'])[str(based_on).upper()]
        if group_on=='category': qdf = qdf.groupby(['INVOICE_DATE','CATEGORY'])[str(based_on).upper()]

        if mode_of_matrix=='mean': 
                qdf = qdf.mean().unstack().reset_index().set_index("INVOICE_DATE")
                qdf = qdf.resample(wise_on).mean()
        if mode_of_matrix=='max': 
                qdf = qdf.max().unstack().reset_index().set_index("INVOICE_DATE")
                qdf = qdf.resample(wise_on).max()
        if mode_of_matrix=='min': 
                qdf = qdf.min().unstack().reset_index().set_index("INVOICE_DATE")
                qdf = qdf.resample(wise_on).min()
        if pattern=='Difference': qdf=qdf-qdf.shift(1)

        qdf = qdf.fillna(0)

        del category1
        try: qdf = qdf.tail(2).apply(calculate_matrix)
        except: qdf = 0
        return qdf
    

        