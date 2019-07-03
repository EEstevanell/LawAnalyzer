import json

def get_new_articles(json_file)->dict:
    fd = open(json_file,"r")
    articles = json.load(fd)["new"]
    fd.close()
    return articles

def get_paragraphs(article)->list:
    return article["value"]

def get_old_articles(json_file)->dict:
    fd = open(json_file,"r")
    articles = json.load(fd)["old"]
    fd.close()
    return articles