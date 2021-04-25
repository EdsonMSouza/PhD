from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
import os

import sqlite3
import contextlib

def parsear(xmlTree, arq):
    # script vars
    author_id = 0
    author_eid = ''
    author_name = ''
    affl_source = ''
    document_count = 0
    cited_by_count = 0
    citation_count = 0
    h_index = 0
    coauthor_count = 0

    asjc = []
    freq = []

    classification_type = ''
    journal_history_issn = []
    affl_id = []
    affl_afdispname = []
    affl_country = ''
    affl_acronym = ''
    affl_state = ''
    affl_city = ''

    affl_history_id = []
    affl_history_country_count = ''

    xml_code = ''
    xml_status = ''

    # open connection with SQLite
    file = 'parse_authors_xml.db'
    conn = sqlite3.connect(file)
    cursor = conn.cursor()

    cont = 0
    for coredata in xmlTree.findAll('author-retrieval-response'):

        # data for author
        try:
            author_id = coredata.find('dc:identifier').string[10:]
        except:
            author_id = 0

        try:
            author_eid = coredata.find('eid').string
        except:
            author_eid = 0
        
        try:
            document_count = coredata.find('document-count').string
        except:
            document_count = 0

        try:
            cited_by_count = coredata.find('cited-by-count').string
        except:
            cited_by_count = 0
        
        try:
            citation_count = coredata.find('citation-count').string
        except:
            citation_count = 0
        
        try:
            coauthor_count = coredata.find('coauthor-count').string
        except:
            coauthor_count = 0

        try:
            h_index = coredata.find('h-index').string
        except:
            h_index = 0

        # subject areas
        tmp = []
        try:
            for areas in coredata.find_all('subject-area'):
                try:
                    tmp = tmp + [ areas.get('code') ]
                except:
                    tmp = tmp + [ 0 ]
            asjc = asjc + [ ';'.join(tmp) ]
        except:
            asjc = asjc + [ '' ]

        if len(coredata.find_all('author-profile')) > 0:
            for author_profile in coredata.find_all('author-profile'):
                # author source
                try:
                    affl_source = author_profile.find('preferred-name').get('source')
                except:
                    affl_source = ''

                # author name
                try:
                    author_name = author_profile.find('preferred-name').find('indexed-name').string
                except:
                    author_name = ''

                if author_profile != None:
                    for c_classification in [author_profile]:
                        if len(c_classification.find_all('classifications')) > 0:
                            for type in c_classification.find_all('classifications'):
                                
                                # classification type
                                try:
                                    classification_type = type.get('type')
                                except:
                                    classification_type = ''

                                # classification frequency - should be use with asj [[]] (ASJ)
                                tmp = []
                                for frequency in c_classification.find_all('classification'):
                                    tmp = tmp + [ frequency.get('frequency') ]
                            freq = freq + [ ';'.join(tmp) ]
                        else:
                            classification_type = ''
                            freq = freq + [ '' ]

                    # journal history    
                    if len(author_profile.find_all('journal-history')) > 0:
                        for journal in [author_profile.find_all('journal-history')]:
                            tmp = []
                            for journal in coredata.find_all('journal'):      
                                for word in journal.find_all('sourcetitle'):
                                    for word in journal.find_all('sourcetitle-abbrev'):
                                        for word in journal.find_all('issn'):
                                            try:
                                                tmp = tmp + [ word.string ]
                                            except:
                                                tmp = tmp + [ '' ]
                            journal_history_issn = journal_history_issn + [ ';'.join(tmp) ]
                    else:
                        journal_history_issn = journal_history_issn + [ 0 ]
                        
                    # affiliation current
                    if len(author_profile.find_all('affiliation-current')) > 0:
                        for affiliation_current in author_profile.find_all('affiliation-current'):
                            if len(affiliation_current.find_all('affiliation')) > 0:
                                tmp0 = []
                                tmp1 = []
                                for affiliation in affiliation_current.find_all('affiliation'):
                                    try:
                                        tmp0 = tmp0 + [ affiliation.get('affiliation-id') ]
                                    except:
                                        tmp0 = tmp0 + [ '' ]
                                  
                                    try:
                                        tmp1 = tmp1 + [ affiliation.find('afdispname').string ]
                                    except:
                                        tmp1 = tmp1 + [ '' ]
                                
                                affl_id = affl_id + [ ';'.join(tmp0) ]
                                affl_afdispname = affl_afdispname + [ '; '.join(tmp1) ]
                                
                            else:
                                affl_id = affl_id + [ 0 ]
                                affl_afdispname = affl_afdispname + [ '' ]
                            
                            # address
                            if len(affiliation.find_all('address')) > 0:
                                for address in affiliation.find_all('address'):
                                    try:
                                        affl_country = address.find('country').string
                                    except:
                                        affl_country = ''
                                    
                                    try:
                                        affl_acronym = address.get('country').upper()
                                    except:
                                        affl_acronym = ''
                                        
                                    try:
                                        affl_city = address.find('city').string.upper()
                                    except:
                                        affl_city = ''

                                    try:
                                        affl_state = address.find('state').string.upper()
                                    except:
                                        affl_state = ''
                            else:
                                affl_acronym = ''
                                affl_country = ''
                                affl_city = ''
                                affl_state = ''
                    else:
                        affl_id = ['']
                        affl_afdispname = ['']
                        affl_acronym = ''
                        affl_country = ''
                        affl_city = ''
                        affl_state = ''

                    # affiliation history
                    tmp0 = []
                    tmp1= []
                    if len(author_profile.find_all('affiliation-history')) > 0:
                        for affiliation_history in author_profile.find_all('affiliation-history'):
                            if len(affiliation_history.find_all('affiliation')) > 0:
                                for journal in affiliation_history.find_all('affiliation'):
                                    tmp0 = tmp0 + [journal.get('affiliation-id')]
                                    try:
                                        tmp1 = tmp1 + [journal.find('address').get('country').upper()]
                                    except:
                                        tmp1 = tmp1 + [ '' ]

                                affl_history_id = affl_history_id + [ ';'.join(tmp0) ]
                                affl_history_country_count = len({x:';'.join(tmp1).count(x) for x in set(tmp1)})
                            else:
                                affl_history_id = 0
                                affl_history_country_count = 0
                    else:
                        affl_history_id = ['']
                        affl_history_country_count = 0
            
                    # affiliation history end    
                else:
                    affl_id = ['']
                    affl_afdispname = ['']
                    affl_source = ''
                    author_name = ''
                    classification_type = ''
                    freq = ['']
                    journal_history_issn = ['']
                    affl_acronym = ''
                    affl_country = ''
                    affl_city = ''
                    affl_state = ''
                    affl_history_id = ['']
                    affl_history_country_count = 0
            #print()
        else:
            affl_source = 0
            author_name = ''
            freq = ['']
            classification_type = ''
            journal_history_issn = ['']
            affl_id = [ '' ]
            affl_afdispname = ['']
            affl_country = ''
            affl_acronym = ''
            affl_state = ''
            affl_city = ''
            affl_history_id = ['']
            affl_history_country_count = 0
            #print("Caiu aqui")

    #print(str(cont).zfill(6), '  Read:', arq)
    try:
        sql = """INSERT INTO xml_authors (
                        area,
                        author_id, 
                        author_eid, 
                        author_name, 
                        affl_source, 
                        document_count, 
                        cited_by_count, 
                        citation_count,
                        h_index, 
                        coauthor_count, 
                        asjc, 
                        asjc_frequency,
                        classification_type,
                        journal_history_issn,
                        affl_id,
                        affl_name,
                        affl_country,
                        affl_acronym,
                        affl_state,
                        affl_city,
                        affl_history_id,
                        affl_history_country_count
                    ) VALUES (
                        ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
                    )"""

        values = (  "Computer Science",
                    author_id, 
                    author_eid, 
                    author_name, 
                    affl_source, 
                    document_count, 
                    cited_by_count, 
                    citation_count,
                    h_index, 
                    coauthor_count, 
                    asjc[0], 
                    freq[0],
                    classification_type,
                    journal_history_issn[0],
                    affl_id[0],
                    affl_afdispname[0],
                    affl_country,
                    affl_acronym,
                    affl_state,
                    affl_city,
                    affl_history_id[0],
                    affl_history_country_count
                    )
                #print(values)
        cursor.execute(sql, values)
        conn.commit()
    except:
        sql = """INSERT INTO xml_authors (area, author_id) VALUES (?,?)"""
        values = ('PARSER ERROR', arq)
        
        print("PARSER ERROR")
        cursor.execute(sql, (values))
        conn.commit()

    # clean vector variables
    asjc = []
    freq = []
    journal_history_issn = []
    affl_afdispname = []
    affl_history_id = []
    affl_id = []
    cursor.close()
    conn.close()