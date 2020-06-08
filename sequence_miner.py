# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 10:17:19 2020

@author: Jean-Francois

Traminer
"""

#Créer un objet séquence
import pandas as pd
import numpy as np

df = pd.DataFrame({"id":[1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 4], "time": [1, 3, 6, 1, 3, 9, 2, 6, 8, 4, 5, 7, 8], "event":["1", "2", "2", "2", "3", "3", "1", "2", "3", "1", "2", "3", "3"]})
print(df.head(5))

df = pd.read_excel("sequence.xlsx")

class Sequence:
    

    
    def __init__(self, df, id_col, time_col, event_col):
        self.df = df
        self.id_col = id_col
        self.time_col = time_col
        self.event_col = event_col
        self.event_alphabet = list(self.df[event_col].unique())
        self.id_alphabet = list(self.df[id_col].unique())
        self.length = len(self.df)
        
    def fill_sequence_gap(self):
        lst_df = []
        lst_event = []
        for id_current in self.id_alphabet:
            sub_df = self.df[self.df[self.id_col] == id_current]
            sub_df.drop_duplicates(inplace = True)
            min_time = sub_df[self.time_col].min()
            max_time = sub_df[self.time_col].max()
            # expand subdf by reindexing
            sub_df.set_index(self.time_col, inplace = True)
            new_range = pd.Index(list(range(min_time, max_time+1)), name = "time")
            sub_df = sub_df.reindex(new_range).ffill(axis = 0) 
            sub_df[self.time_col] = sub_df.index
            
            
            lst_df.append(sub_df)
            lst_event.append(sub_df[self.event_col].to_list())
        self.seq_long =  pd.concat(lst_df)
        self.seq_long.index.name = None
        self.seq_lst =  lst_event
        self.seq_pivot1 = self.seq_long.pivot(index = self.id_col, columns = self.time_col, values = self.event_col).T
        self.seq_pivot2 = self.seq_long.pivot_table(index = self.time_col, columns = self.event_col, aggfunc="count")
    
    

    def stats_state_sequence(self):
        pass
        
    def stats_id_sequence(self):
        pass
        
    def plot_state_timeline(self):
        self.seq_pivot2.plot.bar(stacked=True, legend = True)
        
    def plot_transition_timeline(self):
        pass

s1 = Sequence(df, "id", "time", "event")
s1.fill_sequence_gap()
print("\ndataframe:\n", s1.df)
print("\event lists:\n", s1.seq_lst)
s1.plot_state_timeline()

# s1["event"].astype(str)
# pivoted = seq.pivot(index = "id", columns = "time", values = "event")
# pivoted_T = seq.pivot(index = "id", columns = "time", values = "event").T
# valpT = pivoted_T.values.tolist()




