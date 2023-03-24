#importing necessary libraries
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

#putting module data on 'modules' dataframe
modules = pd.read_csv('dataset\modulesMovieStyle2.csv')

tfidf = TfidfVectorizer(stop_words='english')
modules['Description'] = modules['Description'].fillna('')
#Construct the required TF-IDF matrix by applying the fit_transform method on the overview feature
overview_matrix = tfidf.fit_transform(modules['Description'])
#Output the shape of tfidf_matrix
overview_matrix.shape

similarity_matrix = linear_kernel(overview_matrix,overview_matrix)

#module index mapping
mapping = pd.Series(modules.index,index = modules['Module Name'])

def recommend_module_based_on_description(module_input):
  module_index = mapping[module_input]
  #get similarity values with other movdules
  #similarity_score is the list of index and similarity matrix
  similarity_score = list(enumerate(similarity_matrix[module_index]))
  #sort in descending order the similarity score of module inputted with all the other module
  similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
  # Get the scores of the 1 most similar movies. Ignore the first movie.
  similarity_score = similarity_score[1:2]
  #return module names using the mapping series
  module_indices = [i[0] for i in similarity_score]

  return (modules['Module Name'].iloc[module_indices[0]])
