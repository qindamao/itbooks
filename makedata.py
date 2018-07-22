#! /usr/bin/env.python
# -*-coding: utf-8 -*-
# __author__ = "qindamao"
# Date: 2018/7/13

from dbs.makedatadb import makedatadb
def tagstofile():
    db = makedatadb()
    tagset = set()
    for row in db.get_all_tags():
        if row == '':
            continue
        tagset = tagset.union(set(row.split(',')))
    taglist = list(map(lambda x:x+'\n',tagset))
    with open('data/tags.txt', 'a', encoding='utf-8') as f:
        f.writelines(taglist)

def booknamestofile():
    db = makedatadb()
    booknames = db.get_all_booknames()
    booklist = list(map(lambda x:x+'\n',booknames))
    with open('data/booknames.txt', 'a', encoding='utf-8') as f:
        f.writelines(booklist)

def __readdatas(filpath):
    datas = {}
    with open(filpath,'r',encoding='utf-8') as f:
        datas = f.readlines()
    return [item.split(',')[0] for item  in datas]

def deletedirtydata():
    booknames = __readdatas('data/booknames.txt')
    cleanout = __readdatas('data/cleanout.txt')
    bookset = set(booknames)
    cleanoutset = set(cleanout)
    db = makedatadb()
    diff = bookset.difference(cleanoutset)
    for data in list(diff):
        db.delete_the_dirty(data)
if __name__ == '__main__':
    #booknamestofile()
    deletedirtydata()


