import nltk
from nltk.corpus import stopwords


def convertResultToToknizeFormat(topicList):
    """
    docstring
    """
    all_stopwords = stopwords.words('english')
    all_stopwords.append('[')
    all_stopwords.append(',')
    all_stopwords.append(']')
    all_stopwords.append('``')
    all_stopwords.append("''")
    all_stopwords.append('?')
    all_stopwords.append('(')
    all_stopwords.append(')')
    all_stopwords.append(':')
    all_stopwords.append('I')
    all_stopwords.append('.')
    all_stopwords.append('-')
    all_stopwords.append("`")
    all_stopwords.append("*")
    all_stopwords.append("\\")
    all_stopwords.append("...")
    all_stopwords.append("\\n")
    all_stopwords.append("#")
    all_stopwords.append("!")
    all_stopwords.append("|")
    all_stopwords.append("&")
    text_tokens = nltk.word_tokenize(topicList)
    tokens_without_sw = [
        word for word in text_tokens if not word in all_stopwords]
    return tokens_without_sw