import pandas as pd
import re
from biothings_client import get_client

# Author: Rohan Subramanian
# Description: Methods to handle gene names, IDs, aliases and symbols during data processing and analysis

# Specify locations of genome annotation tables
fpath = "/booleanfs2/sahoo/Data/SeqData/genome/"

GENOME_ANNOTATIONS = {
    "Homo sapiens":"Homo_sapiens.GRCh38.99.chr_patch_hapl_scaff.txt",
    "Mus musculus":"Mus_musculus.GRCm38.94.txt",
    "Rattus norvegicus":"Rattus_norvegicus.Rnor_5.0.79.txt",
    "Arabidopsis thaliana":"Arabidopsis_thaliana.TAIR10.22.txt",
    "Chlorocebus sabaeus":"Chlorocebus_sabaeus.ChlSab1.1.100.txt",
    "Danio rerio":"Danio_rerio.GRCz11.104.chr_patch_hapl_scaff.txt",
    "Mustela putorius":"Mustela_putorius_furo.MusPutFur1.0.99.txt",
    "Papio anubis":"Papio_anubis.Panu_3.0.98.txt"
}

# Use BioThings API to interchange between gene names, IDs, aliases and symbols
# Works on any system, slower
# Further documentation: https://biothings-clientpy.readthedocs.io/en/latest/index.html

def getAlias(gene, species="human"):
    '''Get alias names given gene name, by default in human database'''
    try:
        gene_client = get_client('gene')
        data = gene_client.query(gene, fields='alias', species=species)
        return data['hits'][0]['alias']
    except:
        print("No results")

def genetoEnsembl(gene, species="human"):
    '''Convert gene name to Ensembl ID'''
    try:
        gene_client = get_client('gene')
        data = gene_client.query(gene, fields='ensembl', species=species)
        return data['hits'][0]['ensembl']['gene']
    except:
        print("No results")
        
def ensembltoGene(ID, species="human"):
    '''Convert Ensembl ID to gene name'''
    try:
        gene_client = get_client('gene')
        data = gene_client.query(ID, fields='symbol', species=species)
        return data['hits'][0]['symbol']
    except:
        print("No results")
        
# Use data stored on Hegemon server to rapidly interchange between Ensembl ID and gene symbol

def getAnnotationTable(species):
    '''Get dataframe of genome annotation table given scientific name'''
    filename = fpath+GENOME_ANNOTATIONS[species]
    return pd.DataFrame(pd.read_csv(filename, sep = '\t', header=None)) 

def getAnnotationDict(species):
    '''Get dataframe of genome annotation table given scientific name'''
    filename = fpath+GENOME_ANNOTATIONS[species]
    fp = open(filename, "r")
    hsdict = {}
    for line in fp:
        line = line.strip();
        ll = re.split("\t", line);
        hsdict[ll[0]] = ll[1]
    fp.close()
    return hsdict

def mergeExpr(expr, species):
    '''Convert ProbeID column of expr file from ensemblID to gene symbol, given scientific name'''
    ensembl_df = getAnnotationTable(species)
    ensembl_df.columns = ["ProbeID", "Name"]
    ensembl_df.merge(expr, how="right",on="ProbeID")