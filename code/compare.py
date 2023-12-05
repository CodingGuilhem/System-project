#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

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

def extract_info(vcf_file) :
    """
    Extract the position and the sequence of the SNP in the vcf file.
    Input : vcf file
    Output : list of the position and the sequence of the SNP
    """

    if len(vcf_file)==0 :
        print("Error : Only the vcf file must be inputed.(string)")
        return []
    
    position = []
    sequence = []
    with open(vcf_file, "r") as vcf :
        for line in vcf :
            if line[0]!="#" :
                splitted_line = line.split("\t")
                position.append(splitted_line[1])
                sequence.append(splitted_line[4])

    return [position, sequence]

    
def create_replicate_dict(vcf_file_path) :
    """
    Create a dictionary of the SNP in the vcf files.
    The key are the path to the vcf file, and the value are the position and the sequence of the SNP.
    Input : dictionary of the vcf files
    Output : dictionary of the SNP ({position : sequence})
    """
    if len(vcf_file_path) == 0 :
        print("Error : Only the dictionary of the vcf files must be inputed.")
        return 0
    
    rep_dict = {}
    info_seq = extract_info(vcf_file_path)
    seq = info_seq[1]
    pos = info_seq[0]
    for i in range(len(seq)) :
        into_dict(rep_dict, pos[i],seq[i])
    
    return rep_dict

def make_dictionary(vcf_dict) :
    """
    Create a dictionary of the SNP in the vcf dictionary.
    Input : dictionary of the vcf files({path : [vcf_file_name1, vcf_file_name2, ...]})
    Output : dictionary of the SNP ({variant_name : {vcf_file_name: {position : sequence}}})
    """
    
    if len(vcf_dict) == 0 :
        print("Error : Only the dictionary of the vcf files must be inputed.")
        return 0
    
    dictionary = {}
    for path in vcf_dict.keys() :
        for vcf_file in vcf_dict[path] :
            variant_name = vcf_file.split("-")[0]
            if variant_name not in dictionary.keys() :
                dictionary[variant_name] = {}
            
            replicate_dict = create_replicate_dict(os.path.join(path,vcf_file))
            dictionary[variant_name][vcf_file] = replicate_dict
    
    return dictionary

def extract_variant_and_replicate_name(vcf_dict) :
    """
    Extract the variant name and the replicate name from the vcf dictionary.
    Input : dictionary of the vcf files ({vcf_variant : {replicate : {position : sequence}}})
    Output : list of the variant name and the replicate name ([variant_name, replicate_name])
    """
    variant_list = []
    replicate_list = []
    for variant in vcf_dict.keys() :
        variant_list.append(variant)
        for replicate in vcf_dict[variant].keys() :
            replicate_list.append(replicate)
    
    return [variant_list, replicate_list]

def calcul_identite(seq1, seq2) :
    """
    Calculate the identity between two sequences of the same length.
    Input : two sequences
    Output : identity between the two sequences
    """
    identite = 0
    for i in range(len(seq1)) :
        if seq1[i] == seq2[i] :
            identite+=1
    
    return identite/len(seq1)

def calcul_full_identite (s1,s2) :
    """
    Calculate the identity between two sequences of different length.
    Input : two sequences
    Output : identity between the two sequences
    """
    identite = []
    if len(s1) < len(s2) :
        for i in range(len(s2)-len(s1)) :
            identite.append(calcul_identite(s1,s2[i:i+len(s1)]))    
    elif len(s2) < len(s1) :
        for i in range(len(s1)-len(s2)) :
            identite.append(calcul_identite(s2,s1[i:i+len(s2)]))
    else :
        return calcul_identite(s1,s2)

    return max(identite)

def compare_dict_two_by_two(d1,d2,gap,threshold) :
    """
    return the number of sequences that are the same between the two dictionary ( {position : sequence})
    Input : two dictionaries
    Output : number of sequences that are the same between the two dictionary
    """
    res = 0
    key_d1 = list(d1.keys())# On extrait les position pour ne pas avoir à boucler sur les deux dictionnaires en même temps
    key_d2 = list(d2.keys())
    for key in key_d1 :
        for g in range(gap+1) : 
            
            if str(int(key)+g) in key_d2 :
                for seq1 in d1[key] :
                    for seq2 in d2[str(int(key)+g)] :
                        if seq1 != "<DEL>" and seq2 != "<DEL>" and seq1 != "<INS>" and seq2 != "<INS>" and seq1 != "<DUP>" and seq2 != "<DUP>": #On ne prend pas en compte les séquences sans nucléotides 
                            identity = calcul_full_identite(seq1,seq2)
                            if identity >= threshold : #Si l'identité des deux sequences est supérieur au threshold on incrémente le compteur
                                res+=1
                
    return res

def compare_replicates(vcf_dict,gap,threshold) :
    """
    Compare the replicates of the SNP.
    Input : dictionary of the SNP ({variant_name : {vcf_file_name: {position : sequence}}})
    Output : dictionary of the differences between the replicates ({
    """
    input = extract_variant_and_replicate_name(vcf_dict)
    variant_list = input[0]
    replicate_list = input[1]

    res = {}
    for variant in variant_list :
        for replicate in range(len(replicate_list)) :
            for replicate2 in range(len(replicate_list)) :
                if  replicate_list[replicate] != replicate_list[replicate2] and replicate_list[replicate] in vcf_dict[variant].keys() and replicate_list[replicate2] in vcf_dict[variant].keys() :
                    d1 = vcf_dict[variant][replicate_list[replicate]]
                    d2 = vcf_dict[variant][replicate_list[replicate2]]
                    s = str(replicate_list[replicate]) + " vs " + str(replicate_list[replicate2])
                    res[s] = {} 
                    res[s] = compare_dict_two_by_two(d1,d2,gap,threshold)
                
    return res

                    
    return 0

