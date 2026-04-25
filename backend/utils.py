import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')

def clean_text(text):
    text = text.lower()
    
    tokens = word_tokenize(text)
    
    tokens = [
        word for word in tokens
        if word not in stopwords.words('english')
        and word not in string.punctuation
    ]
    
    return " ".join(tokens)

import re

def extract_experience(text):
    text = text.lower()
    
    # Match patterns like "2 years", "3+ years"
    matches = re.findall(r'(\d+)\+?\s*years?', text)
    
    if matches:
        return max([int(x) for x in matches])
    
    return 0