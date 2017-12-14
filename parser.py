# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 14:35:13 2017

@author: jerem
"""
import pymysql
import pymysql.cursors

directory = "C:\\Users\\jerem\\Desktop\\M2\\multi_agent\\FullRLFAP\\CELAR\\scen01\\"

# Connect to the database.
conn = pymysql.connect(db='mas', user='root', passwd='', host='localhost')

sql_insert_var = "INSERT INTO `variable` (`var_nb`,`domain_nb`) VALUES (%s, %s)"
sql_insert_dom = "INSERT INTO `domain` (`dom_nb`,`card`,`val_dom`) VALUES (%s, %s, %s)"
sql_insert_ctr = "INSERT INTO `constraints` (`var_nb1`,`var_nb2`,`const_type`,`op_const`,`nb_k`) VALUES (%s, %s, %s, %s, %s)"
#%%
var = open(directory+"var.txt", "r")
for line in var: 
    with conn.cursor() as cursor:
        cursor.execute(sql_insert_var,(int(line[0:line.index(' ',3)]),int(line[6:7]))) #We execute our SQL request
        conn.commit()  
#%%
dom = open(directory+"dom.txt", "r")
for line in dom:
    card = int(line[5:7])
    x = 7
    y = 11
    #print(line[9:11])
    for i in range(0,card):
        with conn.cursor() as cursor:
            cursor.execute(sql_insert_dom,(int(line[2:3]),card,int(line[x:y]))) #We execute our SQL request
            conn.commit()  
        int(line[x:y])
        x += 4
        y += 4
#%%
var = open(directory+"ctr.txt", "r")
for line in var:
    op = line[10:11]
    with conn.cursor() as cursor:
        cursor.execute(sql_insert_ctr,(int(line[0:3]),int(line[4:7]),line[8:9],line[10:11],int(line[12:15]))) #We execute our SQL request
        conn.commit()  