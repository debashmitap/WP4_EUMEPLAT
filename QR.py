import pandas as pd
from matplotlib import pyplot as plt

def reduceticks(plt, N):
    # thanks to https://stackoverflow.com/a/64819668
    # 1 tick every N
    xticks_pos, xticks_labels = plt.xticks()  # get all axis ticks
    myticks = [j for i,j in enumerate(xticks_pos) if not i%N]  # index of selected ticks
    # newlabels = [label for i,label in enumerate(xticks_labels) if not i%N]
    return myticks


df=pd.read_csv("./newsguard.csv", usecols=['twitter_id','country','owner','rating','owner'])
print(df)

df1=pd.read_csv("./migr_refug_corpus.csv", usecols=['author_id','lang','source','created_at','id'])
print(df1.head())


df2 = pd.merge(
    left=df1,
    right=df,
    left_on='author_id',
    right_on='twitter_id',
    how='left'
).drop(columns='twitter_id')
df2.to_csv("tweetsQR.csv")
print(df2.head())  

df2 = df2.drop_duplicates(subset=['id']) #removes duplicates using column id

df2['created_at'] =pd.to_datetime(df2['created_at'])   #change to date value from string
df2 = df2.sort_values(['created_at'])
df2['year_month']= df2['created_at'].dt.year.astype(str) + '_' + df2['created_at'].dt.month.astype(str) #add a column  

#france

df_fr = df2[df2['country'] == 'FR']
df_fr = df_fr[df_fr['rating'] == 'N'] #check the rating which points to reliable unreliable resources (N=unreliable, T=reliable)
print(df_fr)

df_fr = df_fr.groupby(['owner'])['owner'].count().count() #.sum() for counting the total number of tweets, .count() for counting the total number of sources
print(df_fr)

df_fr = df2[df2['country'] == 'FR']
df_fr = df_fr[df_fr['rating'] == 'T']
df12_fr1 = df_fr.groupby(['year_month'])['year_month'].count()
print(df12_fr1)

df_fr = df2[df2['country'] == 'FR']
df_fr = df_fr[df_fr['rating'] == 'N']
df12_fr2 = df_fr.groupby(['year_month'])['year_month'].count()
print(df12_fr2)

xlabels = df_fr['year_month'].unique().tolist()
xticks = range(len(xlabels))

plt.plot(df12_fr1)
plt.plot(df12_fr2, color='red')
plt.gca().axes.get_xaxis().set_visible(True)

plt.xticks(xticks, xlabels,rotation = 45)
plt.gca().set_xticks(reduceticks(plt, 3)) 

plt.title("Time series of tweets in France")
plt.xlabel("year_month")
plt.ylabel("No. of tweets")
plt.legend(["Reliable", "Questionable"], loc ="upper right")

plt.show()

#italy

df_it = df2[df2['country'] == 'IT']
df_it = df_it[df_it['rating'] == 'N'] #check the rating which points to reliable unreliable resources
print(df_it)

df_it = df_it.groupby(['owner'])['owner'].count().sum()
print(df_it)



df_it = df2[df2['country'] == 'IT']
df_it = df_it[df_it['rating'] == 'T']
df12_it1 = df_it.groupby(['year_month'])['year_month'].count()
print(df12_fr1)

df_it = df2[df2['country'] == 'IT']
df_it = df_it[df_it['rating'] == 'N']
df12_it2 = df_it.groupby(['year_month'])['year_month'].count()
print(df12_it2)

xlabels = df_it['year_month'].unique().tolist() # year_month labels
xticks = range(len(xlabels)) # a range from 0.. number of months in dataset

plt.plot(df12_it1)
plt.plot(df12_it2, color='red')
plt.gca().axes.get_xaxis().set_visible(True)
plt.xticks(xticks, xlabels,rotation = 45)
plt.gca().set_xticks(reduceticks(plt, 3))
# plt.xticks(df_it['year_month'].unique().tolist()[::3], rotation = 45)
plt.title("Time series of tweets in Italy")
plt.xlabel("year_month")
plt.ylabel("No. of tweets")
plt.legend(["Reliable", "Questionable"], loc ="upper right")
plt.show()



#germany

df_de = df2[df2['country'] == 'DE']
df_de = df_de[df_de['rating'] == 'N'] #check the rating which points to reliable unreliable resources
print(df_de)

df_de = df_de.groupby(['owner'])['owner'].count().count()
print(df_de)


df_de = df2[df2['country'] == 'DE']
df_de = df_de[df_de['rating'] == 'T']
df12_de1 = df_de.groupby(['year_month'])['year_month'].count()
print(df12_de1)

df_de = df2[df2['country'] == 'DE']
df_de = df_de[df_de['rating'] == 'N']
df12_de2 = df_de.groupby(['year_month'])['year_month'].count()
print(df12_de2)

xlabels = df_it['year_month'].unique().tolist()
xticks = range(len(xlabels))

plt.plot(df12_de1)
plt.plot(df12_de2, color='red')
plt.gca().axes.get_xaxis().set_visible(True)
plt.xticks(xticks, xlabels,rotation = 45)
plt.gca().set_xticks(reduceticks(plt, 3))
# plt.xticks(df_de['year_month'].unique().tolist()[::3],rotation = 45)
plt.title("Time series of tweets in Germany")
plt.xlabel("year_month")
plt.ylabel("No. of tweets")
plt.legend(["Reliable", "Questionable"], loc ="upper right")
plt.show()

#UK

df_uk = df2[df2['country'] == 'GB']
df_uk = df_uk[df_uk['rating'] == 'T'] #check the rating which points to reliable unreliable resources
print(df_uk)

df_uk = df_uk.groupby(['owner'])['owner'].count().count()
print(df_uk)


df_uk = df2[df2['country'] == 'GB']
df_uk = df_uk[df_uk['rating'] == 'T']
df12 = df_uk.groupby(['year_month'])['year_month'].count()
print(df12)

df_uk1 = df2[df2['country'] == 'GB']
df_uk1 = df_uk1[df_uk1['rating'] == 'N']
df12_uk = df_uk1.groupby(['year_month'])['year_month'].count()
print(df12_uk)

xlabels = df_it['year_month'].unique().tolist()
xticks = range(len(xlabels))

plt.plot(df12)
plt.plot(df12_uk, color='red')
plt.gca().axes.get_xaxis().set_visible(True)
plt.xticks(xticks, xlabels,rotation = 45)
plt.gca().set_xticks(reduceticks(plt, 3))
# plt.xticks(df_uk['year_month'].unique().tolist()[::3], rotation = 45)
plt.title("Time series of tweets in UK")
plt.xlabel("year_month")
plt.ylabel("No. of tweets")
plt.legend(["Reliable", "Questionable"], loc ="upper left")
plt.show()

