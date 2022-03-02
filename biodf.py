import pandas as pd
import  matplotlib.pyplot as plt
import seaborn as sns


class BioDF(pd.DataFrame):    # adding new functions to the Dataframe class
    _metadata = ['lucas']
    lucas = 1  # This will be passed to copies

    @property
    def _constructor(self):
        return SubclassedDataFrame

    def my_method(self):
        return self + 1 

    def my_second_method(self, another_df):
        return self + another_df

    def show_plot(self, column_name, color='blue'):
      plt.plot(self[column_name], color=color)
      plt.show()
        
        
    def is_bed(self ,chr_prefix='chr' ):
      ''' 
      Return True case the df has a BED3 configuration first column =chromossome information , second=start information, third=end information
      Parameters:
        chr_prefix : str ('chr' )
          Check if the chromossome first columns has elements with a given prefix.
      
      Return: bool 
      '''
      df = self
      columns_df = df.columns.values
      col_chr_check = set( df[columns_df[0]].apply(lambda x :  x.lower().startswith(chr_prefix.lower())   )  )
      chr_detected = False
      if len(col_chr_check) == 1 and col_chr_check == set([True]):
        chr_detected= True
      else:
        assert chr_detected == True, f"The {chr_prefix} prefix was not found in all the  first column elements"
        return False

      end_and_start_check = (df[columns_df[2]] > df[columns_df[1]]).unique()
      if end_and_start_check.tolist() == [True]:
        return True
      else:
        assert end_and_start_check.tolist() == [True], f" All the elements in the third column should be higher than the second column"
        return False

