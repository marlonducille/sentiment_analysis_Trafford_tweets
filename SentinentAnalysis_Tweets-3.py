
#https://www.analyticsvidhya.com/blog/2018/02/the-different-methods-deal-text-data-predictive-python/
from nltk.corpus import movie_reviews
from nltk.classify import NaiveBayesClassifier
from sklearn.naive_bayes import GaussianNB
from collections import defaultdict
import nltk.classify.util
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from collections import Counter

#https://datascienceplus.com/brexit-tweets-sentiment-analysis-in-python/
#https://www.nltk.org/book/ch02.html
#https://twitter-sentiment-csv.herokuapp.com/
#https://towardsdatascience.com/latent-semantic-analysis-sentiment-classification-with-python-5f657346f6a3

#C:\Users\Karen\Anaconda3\Scripts

def word_features(words):
    features = defaultdict(lambda: False)
    for word in words:
        features[word] = True
    return features

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
      all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def extract_features(document):
    word_features = get_word_features(get_words_in_tweets(tweets_process))
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features


dataset = pd.read_csv('tweet_about_trafford_all2.csv', error_bad_lines=False)
stop = stopwords.words('english')

tweets = []
tweets_text = ''

for i in range(0, 122):
    tweet = tuple([dataset.Tweet[i], dataset.Sentiment[i]])
    dataset.Tweet[i] = dataset.Tweet[i].replace('[^\w\s]','')
    dataset.Tweet[i] = dataset.Tweet[i].replace('https','')
    dataset.Tweet[i] = dataset.Tweet[i].replace('co','')
    dataset.Tweet[i] = dataset.Tweet[i].replace('RT','')
    dataset.Tweet[i] = dataset.Tweet[i].replace('re','')   
    dataset.Tweet[i]  = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",dataset.Tweet[i]).split())
    tweets_text = tweets_text + dataset.Tweet[i]
    tweets.append(tweet)


tweets_process = []
for (words, sentiment) in tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    tweets_process.append((words_filtered, sentiment))



training_set = nltk.classify.apply_features(extract_features, tweets_process)
classifier = nltk.NaiveBayesClassifier.train(training_set)


new_tweet = 'Nation being asset stripped through #Tory council funds cuts.  To fund the wealthy and corporate tax cuts.'
print(classifier.classify(extract_features(new_tweet.split())))



from wordcloud import WordCloud
import matplotlib.pyplot as plt

wordcloud = WordCloud(
    background_color='black',
    max_words=25,
    width=4000,
    height=3000
).generate(tweets_text)


plt.imshow(wordcloud)
plt.axis('off')
plt.show()

# other visualisation
with open('council_tax_tweet.csv', 'r', encoding = 'utf8') as counciltaxfile:
        # Pandas to read the “Sentiment” column,
        df_counciltax = pd.read_csv(counciltaxfile, error_bad_lines=False)
        sent_tweet = df_counciltax["sentiment"]

        #use Counter to count how many times each sentiment appears and save each as a variable
        counter = Counter(sent_tweet)
        positive = counter['positive']
        negative = counter['negative']
        neutral = counter['neutral']


## declare the variables for the pie chart, using the Counter variables for “sizes”
labels = 'Positive', 'Negative', 'Neutral'
sizes = [positive, negative, neutral]
colors = ['green', 'red', 'black']
text = "council tax"

## use matplotlib to plot the chart
plt.pie(sizes, labels = labels, colors = colors, shadow = True, startangle = 90)
plt.title("Sentiment Tweets about Trafford")
plt.show()

