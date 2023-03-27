#importing necessary libraries
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer

def add_user_module(modules, userFields, userKeywords):
    dataframeFields = ""
    dataFrameKeywords = ""

    for x in userFields:
        dataframeFields = dataframeFields +  f"{{'name': '{x}'}}, "

    for x in userKeywords:
        dataFrameKeywords = dataFrameKeywords +  f"{{'name': '{x}'}}, "

    userModule = pd.DataFrame({"Module Name":["userModule"],
                        "Fields":[f"[{dataframeFields}]"],
                        "Keywords":[f"[{dataFrameKeywords}]"],
                        "Lecturer":["{' '}"]})

    modules = modules.append(userModule, verify_integrity= False,ignore_index=True)

    return modules

def initlialiseDatbase():
  modules = pd.read_csv('dataset\modulesMovieStyle2.csv')

  #importing necessary columns
  modules = modules[['Module Name', 'Fields', 'Keywords', 'Lecturer']]
  
  return modules

def moduleSimilarity(modules):
  #changing the 3 columns into python objects ( list of dictionaries here)
  modules['Fields'] = modules['Fields'].apply(literal_eval)
  modules['Lecturer'] = modules['Lecturer'].apply(literal_eval)
  modules['Keywords'] = modules['Keywords'].apply(literal_eval)

  #grabbing the names of all the fields and keywords attached to each module
  modules['Fields'] = modules['Fields'].apply(lambda x: [i['name'].lower() for i in x])
  modules['Keywords'] = modules['Keywords'].apply(lambda x: [i['name'].lower() for i in x])

  #taking maximum 3 fields/lecturers/keywords for each module
  modules['Fields'] = modules['Fields'].apply(lambda x: x[:3] if len(x)>3 else x)
  modules['Lecturer'] = modules['Lecturer'].apply(lambda x: x[:3] if len(x)>3 else x)
  modules['Keywords'] = modules['Keywords'].apply(lambda x: x[:3] if len(x)>3 else x)

  #removing spaces
  modules['Lecturer'] = modules['Lecturer'].apply(lambda x: [i.replace(' ','') for i in x])
  modules['Keywords'] = modules['Keywords'].apply(lambda x: [i.replace(' ','') for i in x])
  modules['Fields'] = modules['Fields'].apply(lambda x: [i.replace(' ','') for i in x])

  #Combine module data to create the metadata
  modules['metadata'] = modules.apply(lambda x : ' '.join(x['Fields']) + ' ' + ' '.join(x['Lecturer']) + ' ' + ' '.join(x['Keywords']), axis = 1)

  count_vec = CountVectorizer(stop_words='english')
  count_vec_matrix = count_vec.fit_transform(modules['metadata'])

  cosine_sim_matrix = cosine_similarity(count_vec_matrix, count_vec_matrix)
  #euclidean_dis_matrix = euclidean_distances(count_vec_matrix, count_vec_matrix)

  #module index mapping
  mapping = pd.Series(modules.index,index = modules['Module Name'])

  return mapping, cosine_sim_matrix
  #return mapping, euclidean_dis_matrix

#recommender function to recommend modules based on their metadata
def recommend_module_based_on_metadata(module_input, fields, keywords):
  
  modules = initlialiseDatbase()

  modules = add_user_module(modules, fields, keywords)
 
  mapping, cosine_sim_matrix = moduleSimilarity(modules)
  #mapping, euclidean_dis_matrix = moduleSimilarity(modules)

  module_index = mapping[module_input]
  #get similarity values with other modules
  similarity_score = list(enumerate(cosine_sim_matrix[module_index]))
  #similarity_score = list(enumerate(euclidean_dis_matrix[module_index]))
  
  #Set Reverse to False for Euclidean Distance
  similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
  # Get the scores of the 2 most similar modules.
  similarity_score = similarity_score[1:5]
  module_indices = [i[0] for i in similarity_score]
  recommendedmodules = []

  for x in range(len(module_indices)):
    recommendedmodules.append(modules['Module Name'].iloc[module_indices[x]])

  return (recommendedmodules)
