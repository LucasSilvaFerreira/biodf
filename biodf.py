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

