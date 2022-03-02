import pandas as pd
import  matplotlib.pyplot as plt
import seaborn as sns

from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype


class BioDF(pd.DataFrame):    # adding new functions to the Dataframe class
    _metadata = ['lucas']
    lucas = 1  # This will be passed to copies

    @property
    def _constructor(self):
        return BioDF

    def my_method(self):
        return self + 1 

    def my_second_method(self, another_df):
        return self + another_df

    def show_plot(self, column_name, color='blue'):
      plt.plot(self[column_name], color=color)
      plt.show()


    def bio_is_bed(self ,chr_prefix='chr' ):
      ''' 
      Return True case the df has a BED3 configuration first column =chromossome information , second=start information, third=end information
      Parameters:
        chr_prefix : str ('chr' )
          Check if the chromossome first columns has elements with a given prefix.
      
      Return: bool 
      '''
      df = self

      
      columns_df = df.columns.values

      # if not is_string_dtype(df[columns_df[0]]):
      #   assert False, 'First column is not a string'
      #   return False

      # if not is_numeric_dtype(df[columns_df[1]]):
      #   print(df[columns_df[1]])
      #   assert False, 'Second column is not a int'
      #   return False

      # if not is_numeric_dtype(df[columns_df[2]]):
      #   assert False, 'Third column is not a int'
      #   return False

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

    
    def bio_reposition_to_bed(self, chr_col_name, start_col_name, end_col_name, check_prefix='chr'):

      ''' 
      Return a dataframe in a valid Bed3 format given the name of the chr, start and end columns.
      All the remaning elements will be shifted after the end column.
      Parameters:
        chr_col_name : str
          Chromossome column
        start_col_name : str
          Start coordinate column
        end_col_name : str
          End coordinate column
      Return: BioDataframe 
      '''


      df_columns_names = [c for c in self.columns if c not in [chr_col_name,start_col_name,end_col_name] ]

      c_extract = [chr_col_name, start_col_name, end_col_name] + df_columns_names 
      
      if  self[c_extract].bio_is_bed( chr_prefix=check_prefix):
        return self[ [chr_col_name, start_col_name, end_col_name] + df_columns_names ]
      else:
        assert False, 'This reposition is not valid, returning a empity BioDf'
        return BioDF()

# df = BioDF() # creating a simple dataframe # all the dataframe functions and attributes are still the same. but now it has new functions

# df_bed = BioDF([['chr1', 'chr1'],
#                 ['hi','hi2'],
#                 [1,1],
#                 [2, 3],
#                 ]).T


# df_bed[[0,1,2]]
#df_bed.bio_reposition_to_bed(0,2,3)
