# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 17:12:39 2020

@author: jairp

cyparser.py: 
    This module contains all the main implementations for a CV parser, 
    encapsulated inside the class `CV_parser`. This class can be loaded and 
    imported form another class when copied into the same directory. 
"""

###############################################################################

### 1. Imports ### 

import re
import spacy 
import docx2txt
import pandas as pd
from time import time
from spacy.matcher import Matcher
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from win32com.client import Dispatch
speak = Dispatch("SAPI.SpVoice")

###############################################################################

EMAIL_REGEX = r'[\w\.-]+@[\w\.-]+'
PHONE_REGEX = r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})'
LINKS_REGEX = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
SYMBOLS = r'[?|$|.|!|,]'
SYMBOLS_ext = r'[?|$|.|!|,|\s]|(of)|(and)| '


# Education Degrees
EDUCATION = [
            'ba', 'ab', 'barts', 'baarts','bsci', 
            'bachelorarts', 'bachelorscience', 
            'bachelorcommerce', 'bachelorartsbcience', 
            'bsa','bacy','bacc','bcomm','bs','bcommerce', 
            'bacommerce', 'businessmajor', 
            'me', 'ms', 'btech', 'mtech', 
            'ssc', 'hsc', 'cbse', 'icse', 'x', 'xii'
        ]


###############################################################################

### 3. Object Implementation ### 

class CV_parser(): 
    
    def __init__(self, stringtext = '',  path='' , language='english', language_model='md'): 
        """ 
        Sets up a CV parser according to input language.
        Example languages: 'english','french','spanish'
        NOTE: Works best in English
        @attributes: 
            @ stringtext: full parsed word text 
            @ _language : parser language 
            @ word_tokenizer : nltk word tokenizer
            @ sent_tokeizer : nltk sentence tokenizer 
            @ stemmer : nltk Snowball stemmer  
            @ lemmatizer : nltk lemmatizer 
            @ stopwords :  stopwords list from input language
        @ other arguments: 
            @ path:  input PATH to try to parse
        """
        print("Initializing...")
        t0 = time() # timing 
        
        self._language = language

        if language == 'english': 
            self._language = 'english'  
            
            if language_model == 'sm': 
                self.language_model = 'en_core_web_sm' 
            elif language_model == 'lg': 
                self.language_model = 'en_core_web_lg' 
            else: 
                self.language_model = 'en_core_web_md'
                
        elif language == 'spanish':  
            self._language = 'spanish'  
            
            if language_model == 'sm': 
                self.language_model = 'es_core_news_sm' 
            else: 
                self.language_model = 'es_core_news_md' 

        elif language == 'french':
            self._language = 'french' 
            
            if language_model == 'sm': 
                self.language_model = 'fr_core_news_sm' 
            else: 
                self.language_model = 'fr_core_news_md' 
                
        else: 
            message = "Input language not recognized. " 
            message += "Please make sure to input a valid language. \n"
            message += "Valid languages are : 'english','spanish''french'"
            raise ValueError(message)
        
        self.stringtext = ""
        self.word_tokenizer = word_tokenize # Re-assign word tokenizer 
        self.sent_tokenizer = sent_tokenize # Re-assign sentence tokenizer
        self.stemmer = SnowballStemmer(language=self.language) # Initialize Snowball stemmer 
        self.lemmatizer = WordNetLemmatizer() # Re-assign lemmatizer 
        self.stopwords = set(stopwords.words(language)) # Obtain language stopwords 
        
        try: 
            # Option for when the input is already in string format
            if type(stringtext) == str and len(stringtext) > 1: 
                print("stringtext input")
                self.stringtext = stringtext 
            elif len(path) > 1: 
                print("processing file...")
                self.stringtext = docx2txt.process(path) # convert into string and assign
            else: 
                raise ValueError("Invalid Input")
                
        except Exception as e: 
            print("ERROR: Something went wrong")
            e.with_traceback() 
            
            
        # SpaCy objects 
        print("Fitting text to spaCY NLP model...")
        self.nlp = spacy.load(self.language_model) # instantiate model 
        self.doc = self.nlp(self.stringtext) # fitted object in spacy nlp 
        self.matcher = Matcher(self.nlp.vocab) # to match NER 
            
        t1 = time() 
        print("Done in {} seconds.".format(t1-t0))
            
        
    @property 
    def language(self): 
        return self._language 
    
    
    def self_print(self): 
        print(self.stringtext) 
        
    
    def self_tokenize(self): 
        return self.word_tokenizer(self.stringtext)
    
            
    def fetch_candidate_name(self): 
        """ 
        Fetches candidate name from input text
        """
        
        possible_names = [] 
        
        nlp_text = self.doc # := nlp(self.stringtext) 
        
        # Pattern for proper names
        pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
        self.matcher.add('NAME', None, pattern) 
        matches = self.matcher(nlp_text) 
        
        possible_names = []
        # fetch the matches 
        for match_id, start, end in matches: 
            span = nlp_text[start:end] 
            possible_names += [span.text]
            if len(possible_names) >= 2: 
                break
                    
        # Extract candidates 
        doc_entities = self.doc.ents 
        
        # Subset to person type entities 
        doc_persons = filter(lambda x: x.label_ == 'PERSON', doc_entities) 
        doc_persons = filter(lambda x: len(x.text.strip().split()) >= 2, doc_persons)
        doc_persons = map(lambda x: x.text.strip(), doc_persons)
        doc_persons = list(doc_persons)
        
        # Assume the first Person entity with more than two tokens is the candidate's name 
        if len(doc_persons) > 0: 
            return possible_names + [doc_persons[0]]
        
        return "NOT FOUND"
        
    def fetch_emails(self):
        return re.findall(EMAIL_REGEX, self.stringtext)
        
    
    def fetch_phone_numbers(self): 
        return re.findall(PHONE_REGEX, self.stringtext) 
    
    
    def fetch_links(self): 
        return re.findall(LINKS_REGEX, self.stringtext)
    
    def fetch_education(self): 
        """
        Fetch education like tokens from the applicant's CV
        """
        # Sentence tokenize text
        nlp_text = [sent.string.strip() for sent in self.doc.sents]
        
        edu ={} 
        # Extract education degree 
        for idx, text in enumerate(nlp_text): 
            
            # split the text, obtain bigrams, and cat both
            text_unigrams = text.split()         
            text_bigrams = [tup[0] + tup[1] for tup in list(ngrams(text_unigrams,2))]
            all_grams = text_unigrams + text_bigrams
            
            for tok in all_grams: 
                # Replace special symbols and lowercase                
                re_tok = re.sub(SYMBOLS_ext,'',tok.lower().strip())
                if re_tok in EDUCATION and re_tok not in self.stopwords: 
                    edu[tok] = text + nlp_text[idx + 1] 
                    
        # Extract year 
        education = [] 
        for key in edu.keys(): 
            year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
            if year: 
                education.append((key, ''.join(year[0])))
            else: 
                education.append(key) 
                
        return education 
    
    
    def fetch_skills(self): 
        """ 
        Look for skillset matches based on a reference skills file
        """
        
        noun_chunks = self.doc.noun_chunks
        nlp_text = self.doc
    
        # removing stop words and implementing word tokenization
        tokens = [token.text for token in nlp_text if not token.is_stop]
        
        data = pd.read_csv("skills.csv")  # reading the csv file
        skills = list(data.columns.values) # extract values into a lis
        skillset = []  # store final skills here
        
        # check for one-grams (example: python)
        for token in tokens:
            if token.lower() in skills:
                skillset.append(token)
        
        # check for bi-grams and tri-grams (example: machine learning)
        for token in noun_chunks:
            token = token.text.lower().strip()
            if token in skills:
                skillset.append(token)
        
        return [i.capitalize() for i in set([i.lower() for i in skillset])]
    
    
    def to_dataframe(self, savepath='', defaultsave=False): 
        """ 
        Extracts all available attributes and creates a dataframe
        """
        
        # Fetch all information 
        cand_name = self.fetch_candidate_name() 
        cand_phones = self.fetch_phone_numbers() 
        cand_emails = self.fetch_emails()
        cand_educ = self.fetch_education() 
        cand_skills = self.fetch_skills()
        
        # Create dictionary object
        cand_data = {'name':cand_name, 'phones':cand_phones,'emails':cand_emails, 
                     'education':cand_educ ,'cand_skills':cand_skills, 
                     'raw_resume':self.stringtext }
        
        # COnvert to pandas dataframe
        df = pd.DataFrame(cand_data.items(), columns=['Field','Content'])
        print(df)
        
        # save file if prompted
        if len(savepath) >2: 
            df.to_csv(savepath) 
        elif defaultsave: 
            df.to_csv()            
        
        return df
    
    
    def mistery_function(self): 
        print("\U0001f600") 
        print("Thank you for trying my code!") 
        speak.speak("Thank you for trying my code!") 
        speak.speak("Wink, wink~")
        
        
        
        
        
        
        
        
        
        
        
        

