'''FEREYDOUN (Fast and flexible, Elastic, built-in collision Resolution, Expandable and downsize-friendly, Yielding, built-in seamless Dynamic resize, Open ended, Uniform, Normal distributed) hash table'''
'''This is not the actual implementation of "FEREYDOUN hash table" and it only serves as a proof of concept.'''

__author__      = "Fereydoun Farrahi Moghaddam"

import hashlib
from math import ceil
from copy import copy, deepcopy
from random import randint


class ACTION:                                                                                                                               # Hash table possible actions.
    SEARCH = 1                                                                                                                              # Returns the value of key if existed after try_i_m tries. Will move the key/value pair if there is an empty cell with less amount of misses. Hash table will be shrunk if possible. 
    INSERT = 2                                                                                                                              # Inserts key/value at the first empty cell that finds. if it goes beyond the Hash table size, it will exapand the Hash table.     
    UPDATE = 3                                                                                                                              # Updates the value of key if existed after try_i_m tries.
    DELETE = 4                                                                                                                              # Deletes the key/value pair if existed after try_i_m tries. Hash table will be shrunk if possible. 



ht_s_i = 10                                                                                                                                 # Hash table initial size
ht_s_e = 1.1                                                                                                                                # Hash table initial size expansion/shrink factor    
empty_cell = {"key":None,"value":None}                                  
ht = []
for i in range(ht_s_i):                                                                                                                     # Hash table
    ht.append(deepcopy(empty_cell))                   

def hash1(key):                                                                                                                             # A general purpose hashing algorithm
    return long(hashlib.md5(key).hexdigest(),16)                                                                                            # md5 is just an example 

def dyn_s(try_i):                                                                                                                           # Calculates the dynamic size of Hash table based on number of misses
    return long(ceil(ht_s_i*(ht_s_e**(try_i-1))))

def ht_pos(key, try_i):                                                                                                                     # Calculates the key/value pair position
    return long(hash1(key)%dyn_s(try_i))

def ht_expnd(pos):                                                                                                                          # Expands the Hash table
    global ht
    for i in range(pos+1-len(ht)):
        ht.append(deepcopy(empty_cell))         

def ht_shrnk():                                                                                                                             # Downsize the Hash table
    global ht
    for i in range(len(ht)-1, ht_s_i-2, -1):
        if ht[i]["key"]!=None:
            break

    ht=ht[:i+1]

def ht_srch(key, action=ACTION.SEARCH, value=None, try_i_m=1000):                                                                           # Performs ACTIONS on Hashtable

    emptycell_1st_pos = None
    found = False

    for try_i in range(1, try_i_m+2):                                                                                                       # i-th try equals to (i-1) misses
        key_pos = ht_pos(key, try_i)
        if key_pos < len(ht):
            if ht[key_pos]["key"]==None and emptycell_1st_pos==None:
                emptycell_1st_pos = key_pos
                if action==ACTION.INSERT:
                    break
            if ht[key_pos]["key"]==key:
                found = True
                break
        else:                                                                                                                               #if it goes outside the current ht size
            if action==ACTION.INSERT:
                ht_expnd(key_pos)

                break
    
    if action==ACTION.INSERT:
        if emptycell_1st_pos!=None:
            ht[emptycell_1st_pos]["key"] = key
            ht[emptycell_1st_pos]["value"] = value
            return [key, value, emptycell_1st_pos, try_i-1, len(ht)]
        else:
            ht[key_pos]["key"] = key
            ht[key_pos]["value"] = value
            return [key, value, key_pos, try_i-1, len(ht)]
        
    if action==ACTION.UPDATE:
        if found:
            ht[key_pos]["value"] = value
            return [key, value, key_pos, try_i-1, len(ht)]
        else:
            return [key, value, None, try_i-1, len(ht)]
        
    
    if found:
        value = ht[key_pos]["value"]
        moved = False
        if action==ACTION.DELETE:
            ht[key_pos]["key"] = None
            ht[key_pos]["value"] = None
        else:
            
            if emptycell_1st_pos!=None:
                moved = True

                ht[emptycell_1st_pos]["key"]=ht[key_pos]["key"]
                ht[emptycell_1st_pos]["value"]=ht[key_pos]["value"]
                ht[key_pos]["key"]=None
                ht[key_pos]["value"]=None
        if key_pos==len(ht)-1 and (moved or action==ACTION.DELETE):
            ht_shrnk()    

        if moved:
            return [key, value, emptycell_1st_pos, try_i-1, len(ht)]
        else:
            return [key, value, key_pos, try_i-1, len(ht)]
    else:
        return [key, None, None, try_i-1, len(ht)]
    
    
    






# Some tests



for i in range(400):
    ht_srch(key=str(i), action=ACTION.INSERT, value="Value1")
    print i, len(ht), ",",

print ht_srch(key="1", action=ACTION.UPDATE, value="1")
print ht_srch(key="1000", action=ACTION.UPDATE, value="1000")

print ht_srch(key="1")
print ht_srch(key="5")
print ht_srch(key="15")


for i in range(25):
    print ht_srch(key=str(i), action=ACTION.DELETE),
    print ht_srch(key="15"),
    print ht_srch(key="18"),


for i in range(390):
    ht_srch(key=str(i), action=ACTION.DELETE)
    ht_srch(key=ht[-1]["key"])
    print 400-i, len(ht), ",",

















