import pandas as pd
import  matplotlib.pyplot as plt
import seaborn as sns
import pybedtools
import json
import subprocess
import os
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

#!pip install pybedtools
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

    def filter_columns(self, substring='', inplace=False):
      '''return the columns names filtered for a substring
      substring: str:
        this will return all columns names mathing the following substrings
      intplace: bool | False
        returns the df with the filtered columns
      '''

      columns_detected = [x for  x  in self.columns if substring in x]
      if inplace:
        return self[columns_detected]
      else:
        return columns_detected

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
      try: 
        df[columns_df[1]].apply(int)
      except:
          assert False == True, f"The column 1 (start)  can't be converted in a number"
          return False
      try: 
        df[columns_df[2]].apply(int)
      except:
          assert False == True, f"The column 2 (end)  can't be converted in a number"
          return False

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

    
    # def bio_reposition_to_bed(self, chr_col_name, start_col_name, end_col_name, check_prefix='chr'):

    #   ''' 
    #   Return a dataframe in a valid Bed3 format given the name of the chr, start and end columns.
    #   All the remaning elements will be shifted after the end column.
    #   Parameters:
    #     chr_col_name : str
    #       Chromossome column
    #     start_col_name : str
    #       Start coordinate column
    #     end_col_name : str
    #       End coordinate column
    #   Return: BioDataframe 
    #   '''

    #   df_columns_names = [c for c in self.columns if c not in [chr_col_name,start_col_name,end_col_name] ]

    #   c_extract = [chr_col_name, start_col_name, end_col_name] + df_columns_names 
      
    #   if  self[c_extract].bio_is_bed( chr_prefix=check_prefix):
    #     return self[ [chr_col_name, start_col_name, end_col_name] + df_columns_names ]
    #   else:
    #     assert False, 'This reposition is not valid, returning a empty BioDf'
    #     return BioDF()


    # def download_genome(self, genome='hg19', force=False):
    #   print ('Need to add new genomes and accept path files')
    #   if genome == 'hg19':
    #     link=' wget http://hgdownload.cse.ucsc.edu/goldenpath/hg19/bigZips/hg19.fa.gz; gzip -d hg19.fa.gz'
    #     out_file= 'hg19.fa'
    #   #add more genomes here


    #   if force == True or not os.path.exists(out_file):
    #       pass
    #   else:
    #       return (out_file)

    #   print ('Downloading',genome,link)
    #   os.system(link)
    #   return out_file



    
    # def bio_get_fasta(self, genome='hg19', force_download=False ):
    #   file_fasta = self.download_genome(genome=genome, force = force_download)
    #   print (file_fasta)
    #   assert self.bio_is_bed() == True, 'Cant get a fasta in a not bed formated df'
    #   extract_seq = pybedtools.BedTool.from_dataframe(self)
    #   a = extract_seq.sequence(fi=file_fasta, bedOut=True)
    #   df = self
    #   df['SEQUENCE'] = open(a.seqfn).read().split('\n')[:-1]
    #   return df

# df = BioDF() # creating a simple dataframe # all the dataframe functions and attributes are still the same. but now it has new functions

# df_bed = BioDF([['chr1', 'chr1'],
#                 ['hi','hi2'],
#                 [100000 ,100020 ],
#                  [100010 ,100030 ],
#                 ]).T


# df_bed[[0,1,2]]
#df_bed = df_bed.bio_reposition_to_bed(0,2,3)
#df_bed.bio_get_fasta()
