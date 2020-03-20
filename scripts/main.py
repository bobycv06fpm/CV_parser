# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 00:27:20 2020

@author: jairp

DRIVER SCRIPT 
"""

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
    


