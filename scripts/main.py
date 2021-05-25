# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 00:27:20 2020

@author: jairp

DRIVER SCRIPT 
"""

##############################################################################
### 1. Import ### 
##############################################################################

import cvparser

##############################################################################
### 2. Driver script ### 
##############################################################################

if __name__ == "__main__": 
    
    # Provide paths to the documents to be parsed 
    PATH1 = '../data_raw/collegestudent.docx' ## Sample 1
    PATH2 = '../data_raw/Hair_Parra_CV_English.docx' ## Sample 2 
    
    ## Example 1: Random standup CV
    
    # Object initialization 
    cv_obj1 = cvparser.CV_parser(path=PATH1)

    # individual parsing functions calling
    cand_name1 = cv_obj1.fetch_candidate_name() 
    cand_phones1 = cv_obj1.fetch_phone_numbers() 
    cand_emails1 = cv_obj1.fetch_emails() 
    cand_educ1 = cv_obj1.fetch_education()  
    cand_skills1 = cv_obj1.fetch_skills() 
    
    # saving the parsed objects 
    cand_df1 = cv_obj1.to_dataframe(savedir='../data_clean/', 
                                    filename='fetched_collegestudent',
                                    defaultsave=False) 
    cand_df1 = cv_obj1.to_json(savedir='../data_clean/', 
                               filename='fetched_collegestudent', 
                               defaultsave=False) 
    
    
    ## 2. Example 2: my own CV sample
    
    # object initalization 
    cv_obj2 = cvparser.CV_parser(path=PATH2) 

    # individual parsing functions calling
    cand_name2 = cv_obj2.fetch_candidate_name() 
    cand_phones2 = cv_obj2.fetch_phone_numbers() 
    cand_emails2 = cv_obj2.fetch_emails() 
    cand_educ2 = cv_obj2.fetch_education()  
    cand_skills2 = cv_obj2.fetch_skills() 
    
    # save the parsed objects to csv or json 
    cand_df2 = cv_obj2.to_dataframe(savedir='../data_clean/', 
                                    filename='fetched_Hair_Parra_CV_English',
                                    defaultsave=False) 
    cand_df2 = cv_obj2.to_json(savedir='../data_clean/', 
                               filename='fetched_Hair_Parra_CV_English', 
                               defaultsave=False) 
        


