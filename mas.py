# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 16:52:15 2017

@author: jerem
"""

import pymysql
import pymysql.cursors

xml = open("test.xml", "w")
xml.write("<instance> \n <presentation name=\"sampleProblem\" maxConstraintArity=\"2\" maximize=\"false\" format=\"XCSP 2.1_FRODO\" /> "")
xml.write("")
xml.close()