import pandas as pd
from matplotlib import pyplot as plt
import plotly.express as px

#df = pd.read_csv("./migr_refug_corpus.csv", usecols=['source','retweet_count'])
#group = df.groupby("source")["retweet_count"].count()
#print(group)
#plt.plot(df.source, df.retweet_count)
#plt.show()
#df1 = df = pd.read_csv("./migr_refug_corpus.csv", usecols=['author_id','created_at'])
#fig = px.line(df1, x = 'created_at', y = 'author_id', title='creation')
#fig.show()

df2 = pd.read_csv("./migr_refug_corpus.csv", usecols=['created_at','lang'])
df2['created_at'] = pd.to_datetime(df2['created_at'])
italy= df2.loc[df2['lang']=='en'] #language italian
left = italy['created_at'].astype(str).str[:10] #first 10 characters in a column, just the date
italy['created_at'] = left   #replacing column contents 
group1 = italy.pivot_table(columns=['created_at'], aggfunc='size') #counts numbers of tweets made on each date

print(group1)

plt.plot(group1)
plt.gca().axes.get_xaxis().set_visible(True)
plt.xlabel("Date of creation")
plt.ylabel("No. of tweets")
plt.show()


df3 = pd.read_csv("./migr_refug_corpus.csv", usecols=['author_id','lang'])
italy_user= df3.loc[df3['lang']=='it'] #language italian
group2 = italy_user.pivot_table(columns=['author_id'], aggfunc='size') #counts numbers of tweets made by each user
print(group2)
