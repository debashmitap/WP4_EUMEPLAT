from latent_ideology_class import latent_ideology as li
import pandas as pd


# df=pd.read_csv("./migration_all_retweeters_data.csv", usecols=['retweeter_author_id','retweeted_id'])
# print(df.head())

# another_csv=pd.read_csv("./migr_refug_corpus.csv", usecols=['id','lang','source','possibly_sensitive'])
# print(another_csv.head())

#for left merge

# df = pd.merge(
#     left=df,
#     right=another_csv,
#     left_on='retweeted_id',
#     right_on='id',
#     how='left'
# ).drop(columns='id')
# df.to_csv("updated.csv")
# print(df.head())    

df=pd.read_csv("./updated.csv")
df = df[df['lang'] == 'it']
print(df)

df = df[:50000]

#we call the method with our example matrix

li_matrix = li(df)

#Lets apply the method!
df1, df2 = li_matrix.apply_method(n=5, targets='retweeter_author_id', sources='retweeted_id')
df1.to_csv('df1.csv')
df2.to_csv('df2.csv')


#We can print the results
print(df1,'\n',df2)

adj_mat = li_matrix.make_adjacency(n=5, targets='retweeter_author_id', sources='retweeted_id')
print(adj_mat)


A = adj_mat.to_numpy() #to numpy matrix
scores_targets = li_matrix.calculate_scores(A)
print(scores_targets)

B = A.T #transposed matrix
scores_sources = li_matrix.calculate_scores(B)
print(scores_sources)

df1a, df2a = li_matrix.apply_simplified_method(adj_mat)
print(df1a, '\n', df2a)


df6=pd.read_csv("./df1.csv", usecols=['target','score'])
print(df.head())

another_csv=pd.read_csv("./updated.csv", usecols=['retweeter_author_id','lang','source','possibly_sensitive'])
print(another_csv.head())


df6 = pd.merge(
    left=df6,
    right=another_csv,
    left_on='target',
    right_on='retweeter_author_id',
    how='left'
).drop(columns='retweeter_author_id')
df6.to_csv("italy.csv")
print(df6.head())   