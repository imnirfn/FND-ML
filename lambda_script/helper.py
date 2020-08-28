import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

def process_text(text, length=False, stem=False):
    
    try:
    
        stop_words = set(stopwords.words('english'))
    
    except:
        
        nltk.download('stopwords')
        
        stop_words = set(stopwords.words('english'))
    if stem:    
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(word.lower()) for word in text.split() if (word.isalpha()) and (word not in stop_words)]
    else:
        tokens = [word.lower() for word in text.split() if (word.isalpha()) and (word not in stop_words)]

    cleaned_text = ' '.join(tokens)

    if length:
        length_of_text = len(tokens)
        return cleaned_text,length_of_text
    else:
        return cleaned_text
