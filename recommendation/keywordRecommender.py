

#importing necessary libraries
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer

def add_user_module(modules, userFields, userKeywords):
    # # full implementation
    dataframeFields = ""
    dataFrameKeywords = ""

    print(f"this is the user keyords {userKeywords}")
    #print(userKeywords)
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

#add_user_module(fields, keywords)

def testing(modules):
  #changing the 4 columns into python objects ( list of dictionaries here)
  modules['Fields'] = modules['Fields'].apply(literal_eval)
  modules['Lecturer'] = modules['Lecturer'].apply(literal_eval)
  modules['Keywords'] = modules['Keywords'].apply(literal_eval)
  #grabbing the names of all the genres attached to each movie
  modules['Fields'] = modules['Fields'].apply(lambda x: [i['name'].lower() for i in x])
  #grabbing the name of the director from all the crew members
  #we will only use directors from the creqw column for our purpose
  #movies[‘crew’] = movies[‘crew’].apply(lambda x: [i[‘name’].lower() for i in x if i[‘job’]==’Director’])
  #grabbing the cast and keywords from the list of dictionaries of those columns
  #modules['Lecturer'] = modules['Lecturer'].apply(lambda x: [i['Module Name'].lower() for i in x])
  modules['Keywords'] = modules['Keywords'].apply(lambda x: [i['name'].lower() for i in x])
  #taking maximum 3 cast/genre/keywords for each movie
  modules['Fields'] = modules['Fields'].apply(lambda x: x[:3] if len(x)>3 else x)
  modules['Lecturer'] = modules['Lecturer'].apply(lambda x: x[:3] if len(x)>3 else x)
  modules['Keywords'] = modules['Keywords'].apply(lambda x: x[:3] if len(x)>3 else x)

  #removing spaces
  modules['Lecturer'] = modules['Lecturer'].apply(lambda x: [i.replace(' ','') for i in x])
  modules['Keywords'] = modules['Keywords'].apply(lambda x: [i.replace(' ','') for i in x])
  modules['Fields'] = modules['Fields'].apply(lambda x: [i.replace(' ','') for i in x])

  modules['metadata'] = modules.apply(lambda x : ' '.join(x['Fields']) + ' ' + ' '.join(x['Lecturer']) + ' ' + ' '.join(x['Keywords']), axis = 1)

  count_vec = CountVectorizer(stop_words='english')
  count_vec_matrix = count_vec.fit_transform(modules['metadata'])
  cosine_sim_matrix = cosine_similarity(count_vec_matrix, count_vec_matrix)
  #module index mapping
  mapping = pd.Series(modules.index,index = modules['Module Name'])

  return mapping, cosine_sim_matrix


#clean movie_id function
# def clean_id(modules, x):
#   #converting everything into integer
#   modules['Module Name'] = modules['Module Name'].astype('int')
#   modules['Keywords'] = modules['Keywords'].astype('int')
#   modules['Fields'] = modules['Fields'].astype('int')
#   modules['Lecturer'] = modules['Lecturer'].astype('int')
#   return modules

#recommender function to recommend movies based on metadata
def recommend_module_based_on_metadata(module_input, fields, keywords):
  
  modules = initlialiseDatbase()

  modules = add_user_module(modules, fields, keywords)

  print(modules.Keywords)

  print(fields)
  print(keywords)
 
  mapping, cosine_sim_matrix = testing(modules)

  module_index = mapping[module_input]
  #get similarity values with other movies
  similarity_score = list(enumerate(cosine_sim_matrix[module_index]))
  similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
  # Get the scores of the 2 most similar movies. Ignore the first movie.
  similarity_score = similarity_score[1:2]
  module_indices = [i[0] for i in similarity_score]
  return (modules['Module Name'].iloc[module_indices[0]])

# recommend_module_based_on_metadata('userModule')