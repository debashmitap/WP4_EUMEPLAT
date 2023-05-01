import gensim
import pandas as pd
import os
# Load the regular expression library
import re
from wordcloud import WordCloud

from gensim.utils import simple_preprocess
import nltk
from nltk.corpus import stopwords
import gensim.corpora as corpora

import pyLDAvis.gensim_models as gensimvis
import pickle 
import pyLDAvis

def remove_stopwords(texts, language):
    stop_words = stopwords.words(language)
    stop_words.extend(['from', 'subject', 're', 'edu', 'use','https','rt','piu'])
    print(stop_words)

    return [[word for word in simple_preprocess(str(doc)) 
            if word not in stop_words] for doc in texts]


if __name__ == "__main__":


    tweets = pd.read_csv("./all-weeks-countries.csv", usecols=['text','lang'])
    print(tweets.head())


    # Remove punctuation
    tweets['text_processed'] = \
    tweets['text'].map(lambda x: re.sub(r'http[s]?:\/\/[\w\d/._-]+', '', x).strip())

    # Convert the titles to lowercase
    tweets['text_processed'] = \
    tweets['text_processed'].map(lambda x: x.lower())

    # Print out the first rows of tweets
    print(tweets['text_processed'].head())

    # Join the different processed titles together.
    long_string = ','.join(list(tweets['text_processed'].values))

    # Create a WordCloud object
    wordcloud = WordCloud(background_color="white", max_words=1000, contour_width=3, contour_color='steelblue')

    # Generate a word cloud
    wordcloud.generate(long_string)

    # Visualize the word cloud
    wordcloud.to_image().show()

    # nltk.download('stopwords')

    def sent_to_words(sentences):
        for sentence in sentences:
            # deacc=True removes punctuations
            yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))

    data = tweets.text_processed.values.tolist()
    data_words = list(sent_to_words(data))

    # remove stop words
    data_words = remove_stopwords(data_words, 'english')
    data_words = remove_stopwords(data_words, 'french')
    data_words = remove_stopwords(data_words, 'italian')
    data_words = remove_stopwords(data_words, 'german')

    # Generate a word cloud after removing stop words
    long_list = [','.join(element) for element in data_words]
    long_string = ','.join(long_list)
    wordcloud.generate(long_string)
    # Visualize the word cloud
    wordcloud.to_image().show()

    print('========= DATA WORDS SAMPLE =========')
    print(data_words[:1][0][:30])
    # Create Dictionary
    id2word = corpora.Dictionary(data_words)

    # Create Corpus
    texts = data_words

    # Term Document Frequency
    corpus = [id2word.doc2bow(text) for text in texts]

    # View
    print(corpus[:1][0][:30])

    # number of topics
    num_topics = 5

    # Build LDA model
    lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                        id2word=id2word,
                                        num_topics=num_topics)

    # Print the Keyword in the 10 topics
    print(lda_model.print_topics())
    doc_lda = lda_model[corpus]

    # Visualize the topics
    # pyLDAvis.enable_notebook()

    LDAvis_data_filepath = os.path.join('./results/ldavis_prepared_'+str(num_topics))

    # # this is a bit time consuming - make the if statement True
    # # if you want to execute visualization prep yourself
    if 1 == 1:
        LDAvis_prepared = gensimvis.prepare(lda_model, corpus, id2word)
        with open(LDAvis_data_filepath, 'wb') as f:
            pickle.dump(LDAvis_prepared, f)

    # load the pre-prepared pyLDAvis data from disk
    with open(LDAvis_data_filepath, 'rb') as f:
        LDAvis_prepared = pickle.load(f)

    pyLDAvis.save_html(LDAvis_prepared, './results/ldavis_prepared_'+ str(num_topics) +'.html')

    LDAvis_prepared