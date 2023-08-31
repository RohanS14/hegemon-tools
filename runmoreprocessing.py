# IMPORT STATEMENTS
import sys
sys.path.append("/Users/rohan/public_html/Hegemon")
import StepMiner as smn
import HegemonUtil as hu
import re
import numpy as np
import math
import pandas as pd
import scanpy as sc
import os
import GEOparse

def getDataInfo():
    '''Get the accession ID, GPL (platform name) and filepath for the Hegemon files.'''
    path_dir = os.getcwd()
    accessionID = path_dir.split("/")[-1]
    gse = GEOparse.get_GEO(geo=str(accessionID), destdir=path_dir)
    gpl = list(gse.gpls.keys())[0]
    filepath = path_dir+"/"+str(accessionID)+'-%s'%(gpl)
    return accessionID, gpl, filepath

def make_idx(expr_name, idx_name):
    '''Build index file from expression file.'''
    print('Starting make_idx')
    expr = expr_name

    ptr = []
    ids = []
    name = []
    desc = []
    pos = 0

    with open(expr, 'rb') as f:
        for line in f:
            if pos == 0:
                pos += len(line)
            else:
                ptr.append(pos)
                pos += len(line)
                split = line.decode("utf-8").split('\t')
                ids.append(split[0])
                name.append(split[1].split(':')[0])
                desc.append(':'.join(split[1].split(':')[1:]))
        f.close()

    with open(idx_name, 'w') as f:
        f.write('ProbeID\tPtr\tName\tDescription\n')
        for i in range(len(ids)):
            f.write('{}\t{}\t{}\t{}\n'.format(ids[i], ptr[i], name[i], desc[i]))
        f.close()
    print("Done with make_idx")

def writeExprIdx(expr):
    '''Write both index and expression file from the expression file as a dataframe.'''
    accessionID, gpl, filepath = getDataInfo()
    expr_name = "%s-expr.txt" % filepath
    idx_name = "%s-idx.txt" % filepath
    print("Starting expr")
    expr.to_csv(expr_name, header=True, index=False,sep='\t')
    print("Done writing expr")
    make_idx(expr_name, idx_name)
    
def printConf(dbid, name, key =''):
    '''Print the information needed to add the dataset to explore.conf (configuration file).'''
    accessionID, gpl, filepath = getDataInfo()
    print("[%s]" % dbid)
    print("name = %s" % name)
    print("expr = %s-expr.txt" % filepath)
    print("index = %s-idx.txt" % filepath)
    print("survival = %s-survival.txt" % filepath)
    print("indexHeader = %s-ih.txt" % filepath)
    print("info = %s-info.txt" % filepath)
    print("key = %s" % key)
    print("source = %s" % accessionID)
    
def writeConf(dbid, name, key='', cf=''):
    '''Write the information to add the dataset to explore.conf (configuration file).'''
    accessionID, gpl, filepath = getDataInfo()
    with open(cf, 'a') as f:
        f.write("\n[%s]\n" % dbid)
        f.write("name = %s\n" % name)
        f.write("expr = %s-expr.txt\n" % filepath)
        f.write("index = %s-idx.txt\n" % filepath)
        f.write("survival = %s-survival.txt\n" % filepath)
        f.write("indexHeader = %s-ih.txt\n" % filepath)
        f.write("info = %s-info.txt\n" % filepath)
        f.write("key = %s\n" % key)
        f.write("source = %s\n" % accessionID)

def main():
    while True:
        dbid = str(input("Database ID "))
        name = str(input("Dataset Name "))
        key = str(input("key "))
        cf = str(input("Configuration file (default /Users/rohan) "))
        if cf == "":
            cf = "/Users/rohan/public_html/Hegemon/explore.conf"
        printConf(dbid, name, key)
        x = str(input("Write to file? y/n "))
        if (x == "y"):
            break
    writeConf(dbid, name, key, cf)

if __name__ == "__main__":
    main()
