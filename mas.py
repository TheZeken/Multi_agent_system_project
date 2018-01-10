# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 16:52:15 2017

@author: jerem
"""

import pymysql
import pymysql.cursors

import pymysql
import pymysql.cursors

# Connect to the database.
conn = pymysql.connect(db='mas', user='root', passwd='', host='localhost')

get_nb_var = "SELECT count(*) FROM `variable`"
get_var = "SELECT * FROM `variable`"
get_nb_dom = "SELECT count(DISTINCT `dom_nb`) FROM `domain`"
get_val_dom = "SELECT `val_dom` FROM `domain` WHERE `dom_nb`= %s"
get_nb_val_dom = "SELECT count(*) FROM `domain` WHERE `dom_nb`= %s"
get_nb_const = "SELECT count(*) FROM `constraints` WHERE"
get_const = "SELECT * FROM `constraints`"


                          

with conn.cursor() as cursor:
    cursor.execute(get_nb_var) #We execute our SQL request
    conn.commit()
    for row in cursor:
        nb_var = row[0]
    cursor.execute(get_nb_dom) #We execute our SQL request
    conn.commit()
    for row in cursor:
        nb_dom = row[0]    
    

xml = open("test.xml", "w")
xml.write("<instance> \n <presentation name=\"sampleProblem\" maxConstraintArity=\"2\" maximize=\"false\" format=\"XCSP 2.1_FRODO\" /> ")
xml.write( "    <agents nbAgents=\""+str(nb_var)+"\"> \n")

for i in range(0,nb_var):
    xml.write("         <agent name=\"a_"+str(i+1)+"\"/> \n")
    
xml.write("     </agents>  \n")

xml.write( "    <domains nbDomains=\""+str(nb_dom)+"\"> \n")

for i in range(0,nb_dom):
    with conn.cursor() as cursor:
            cursor.execute(get_nb_val_dom,i) #We execute our SQL request
            conn.commit()
            for row in cursor:
                nb_val_dom = row[0]
            xml.write("         <domain name=\"d_"+str(i+1)+"\" nbValues=\""+str(nb_val_dom)+"\">")
            
            cursor.execute(get_val_dom,i) #We execute our SQL request
            conn.commit()
            cpt =1
            for row in cursor:
                if cpt != nb_val_dom:
                    xml.write(str(row[0])+" ")
                    cpt+=1
                else:
                    xml.write(str(row[0]))
                    cpt+=1
    
    xml.write("</domain>  \n")
xml.write("</domains>  \n")

xml.write( "    <variables nbVariables=\""+str(nb_var)+"\"> \n")

with conn.cursor() as cursor:
    cpt=0
    cursor.execute(get_var) #We execute our SQL request
    conn.commit()
    for row in cursor:
        nb_val_dom = row[1]
        val_var = row[0]
        xml.write("         <variable name=\"v_"+str(cpt+1)+"\" domain=\"d_"+str(nb_val_dom)+"\" agent=\"a_"+str(cpt+1)+"\" /> \n")
        cpt+=1
xml.write("</variables>  \n")

xml.write("<predicates nbPredicates=\"2\"> \n")
xml.write("  <predicate name=\"EQ\"> \n ")
xml.write("      <parameters> int X1 int X2 int X3 </parameters>  \n       <expression>\n")
xml.write("         <functional> eq(sub(X1, X2),X3) </functional> \n        </expression>\n")
xml.write("  </predicate> \n ")

xml.write("  <predicate name=\"SUP\"> \n ")
xml.write("      <parameters> int X1 int X2 int X3</parameters>  \n       <expression>\n")
xml.write("         <functional> gt(sub(X1, X2),X3) </functional> \n       </expression>\n")
xml.write("  </predicate> \n ")

xml.write("</predicates> \n\n")

with conn.cursor() as cursor:
    cursor.execute(get_nb_var) #We execute our SQL request
    conn.commit()
    for row in cursor:
        nb_const = row[0]
        xml.write("<constraints nbConstraints=\""+str(nb_const)+"\"> \n")
    
    
    cursor.execute(get_const) #We execute our SQL request
    conn.commit()
    for row in cursor:
        if row[4] == "=":
            name_const = "v_"+str(row[1])+'_min_v_'+str(row[2])+'_eq'
            ref = "EQ"
            val_min = int(row[1])-int(row[2])
        else:
            name_const = "v_"+str(row[1])+'_min_v_'+str(row[2])+'_sup'
            ref = "SUP"
            val_min = int(row[1])-int(row[2])
            
        xml.write("<constraint name=\""+name_const+"\" arity=\"2\" scope=\"v_"+str(row[1])+" v_"+ str(row[2])+"\" reference=\""+ref+"\" >\n")
        xml.write("<parameters> v_"+str(row[1])+" v_"+str(row[2])+" "+str(row[5])+"</parameters> \n")
        xml.write("</constraint> \n")
    xml.write("</constraints> \n")
    xml.write("</instance>")





xml.close()