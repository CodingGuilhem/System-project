#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import compare as c

arg = sys.argv[1:]

for i in range(len(arg)) :
    if i == 0 and arg[i] != "" :
        path = [arg[i]]
    
    if i == 1 and arg[i] != "" :
        gap = int(arg[i])
    else : 
        gap = 0
    
    if i == 2 and arg[i] != "" :
        treshold = int(arg[i])
    else :
        treshold = 0.75
    
    if i >= 3 :
        print("Error : Too many arguments.")
        sys.exit()

def into_dict(dict, key, value):
    """ 
    Add the value to the key in the dictionary.
    Input : dictionary, key, value
    Output : dictionary
    """
    if key in dict:
        dict[key]+= [str(value)]
    else:
        dict[key] = {}
        dict[key] = [str(value)]
    return dict

def add_dict(dict1, dict2):
    """
    Add the values of the second dictionary to the first one.
    Input : two dictionaries
    Output : first dictionary with the second in it
    """
    for key in dict2.keys():
        if key in dict1.keys():
            dict1[key] += dict2[key]
        else:
            dict1[key] = dict2[key]
    return dict1

def explore_path (path) :
    """
    Explore the path and create a dictionary of the vcf files in the path.
    The key are the path to the vcf file, and the value are the name of the vcf file.
    Input : path to the data
    Output : dictionary of the vcf files ({path : [vcf_file_name1, vcf_file_name2, ...]})
    """
    dico_files = {}
    for file in os.listdir(path):
        full_path = os.path.join(path,file) 
        if os.path.isdir(full_path) :
            explore_path(full_path)
        else :
            fin = file.split(".")[-1]
            if fin == "vcf" :
                into_dict(dico_files, path, file)
    return dico_files 

def make_vcf_dict(path) :
    """
    Create a dictionary of the vcf files in the path.
    The key are the path to the vcf file, and the value are the name of the vcf file.
    Input : path to the data
    Output : dictionary of the vcf files    
    """ 
    
    if len(path)!=1 :
        print("Error : Variable path must be one string only")
        return 0
    
    vcf_dict = {}
    list_dir =os.listdir(path[0])
    for elements in list_dir :
        full_path = os.path.join(path[0],elements)
        if os.path.isdir(full_path) : # if the element is a directory we explore it and add the results to the dictionary
            add_dict(vcf_dict, explore_path(full_path))
        else : #else the element is a file, we look if it is a vcf file and add it to the dictionary if it is the case
            if elements.split(".")[-1] == "vcf" :
                into_dict(vcf_dict, path[0], elements) 
    return vcf_dict

def print_results (dic) :
    """
    Print the results of the comparison.
    Input : dictionary of the SNP ({variant_name : number_of_same_sequence})
    Output : Print the results in proper format
    """
    if len(dic) == 0 :
        print("No sequences found.")
    else :
        for variant in dic.keys() :
            print(variant + " : " + str(dic[variant]) + " sequences found.")

    return 0

vcf_dict = make_vcf_dict(path)
vcf_dict = c.make_dictionary(vcf_dict)# We replace the dictionary of the vcf path by the dictionary of the SNP
compare_dict = c.compare_replicates(vcf_dict,gap,treshold) # We compare the replicates
print_results(compare_dict) # We print the results