# CV_parser
A parser for word and pdf resumes

## Instructions 
1) Go to the `/scripts` directory and run the  `main.py` file for immediate results. 
2) The `data_raw` folder contains two sample CV's to be parsed. 
3) The `data_clean` folder contains the fetched information from the raw input CV's using the `main` script in the `/scripts` directory.
4) Inside the `/scripts` directory, the `cvparser.py` module contains all the main implementaions, which aare called by the `main.py` on the two CVs inside the `data_raw` directory. 

## Information 
- Author: Hair Albeiro Parra Barrera 
- Date: 2020-03-09

## Sources: 
- https://github.com/bjherger/ResumeParser/blob/master/bin/main.py 
- https://spacy.io/usage/processing-pipelines 
- https://medium.com/@divalicious.priya/information-extraction-from-cv-acec216c3f48 
- https://github.com/divapriya/Language_Processing/blob/master/resumeParser.py
- https://www.omkarpathak.in/2018/12/18/writing-your-own-resume-parser/ 

### Demo (main.py) 

```python

import cvparser

if __name__ == "__main__": 
    
    # Read word documents
    PATH1 = '../data_raw/collegestudent.docx' ## Sample 1
    PATH2 = '../data_raw/Hair_Parra_CV_English.docx' ## Sample 2
    
    
    # Sample 1 parsing
    cv_obj1 = cvparser.CV_parser(path=PATH1)

    cand_name1 = cv_obj1.fetch_candidate_name() 
    cand_phones1 = cv_obj1.fetch_phone_numbers() 
    cand_emails1 = cv_obj1.fetch_emails()
    cand_educ1 = cv_obj1.fetch_education() 
    cand_skills1 = cv_obj1.fetch_skills()
    cand_df1 = cv_obj1.to_dataframe(savepath = '../data_clean/fetched_collegestudent.csv')
        
    
    # Sample 2 parsing
    cv_obj2 = cvparser.CV_parser(path=PATH2)

    cand_name2 = cv_obj2.fetch_candidate_name() 
    cand_phones2 = cv_obj2.fetch_phone_numbers() 
    cand_emails2 = cv_obj2.fetch_emails()
    cand_educ2 = cv_obj2.fetch_education() 
    cand_skills2 = cv_obj2.fetch_skills()
    cand_df2 = cv_obj2.to_dataframe(savepath = '../data_clean/fetched_Hair_Parra_CV_English.csv')


```
**Output:** 

```
Initializing...
processing file...
Fitting text to spaCY NLP model...
Done in 25.215816974639893 seconds.
         Field                                            Content
0         name     [Susan Forsythe, LinkedIn URL, Susan Forsythe]
1       phones                                     [555.555.5555]
2       emails                                [sf@somedomain.com]
3    education                                    [BusinessMajor]
4  cand_skills                                                 []
5   raw_resume  Susan Forsythe\n\nSometown, AZ 55555  |  555.5...
Initializing...
processing file...
Fitting text to spaCY NLP model...
Done in 22.538394451141357 seconds.
         Field                                            Content
0         name  [Hair Albeiro, Albeiro Parra, Lexicoder Lemmat...
1       phones                           [514-586-8551, 014-2016]
2       emails     [jair.parra@outlook.com, hair.parra@gmail.com]
3    education                                     [(B.A., 2020)]
4  cand_skills  [R/rstudio, Ml, Sql, Mysql, Nlp, Natural langu...
5   raw_resume  Hair Albeiro Parra Barrera\n\nMontreal, Quebec...
```
