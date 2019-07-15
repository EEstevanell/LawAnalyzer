import json

def get_new_law(json_file)->dict:
    fd = open(json_file, "r")
    law = json.load(fd)["new"]
    fd.close()
    return law

def get_paragraphs(article)->list:
    return article["value"]

def get_old_law(json_file)->dict:
    fd = open(json_file,"r")
    law = json.load(fd)["old"]
    fd.close()
    return law

def get_new_law_2(json_file)->dict:
    fd = open(json_file, "r")
    law = json.load(fd)["new"]
    fd.close()
    return law

def get_old_law_2(json_file)->dict:
    fd = open(json_file,"r")
    law = json.load(fd)["old"]
    fd.close()
    return law