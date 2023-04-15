
# Author : Sphesihle Madonsela 
# Date 17 April 2022
# CSC3002F OS Assigment 1
# https://nicomedes.assistedcoding.eu/#/app/os/page_replacement
# Link to test the page faults 
# copy the output pages remove the square brakets. paste it to the abouve website for testing

from collections import deque
import random
import sys

def main():
    
    # the frame size from 1 to 7
    size = int(sys.argv[1])

    
    ref_size = [j for j in range(8,65,8)]  
    # select the page size at random from 8 to 64
    
    pages = [random.randint(0,9) for i in range(ref_size[random.randint(0,len(ref_size)-1)])] # array with random numbers
    
    print(f'N = {len(pages)} pages')
    print(f'pages : {pages}')
    print("FIFO",FIFO(size,pages),'page faults')
    print('LRU',LRU(size,pages),'page faults')
    print('OPT',OPT(size,pages),'page faults')
    
# helper fuction for LRU mathod
def lru_min(dictionary,ram,key):
    
    min = dictionary[ram[0]]
    for pg in ram:
        if dictionary[pg] < min :
            min  = dictionary[pg]
    
    for i in dictionary.keys():
        if dictionary[i] == min:
            key = i
            break  
    return key 

def FIFO(size,pages):
    
    q  = deque() # the queue is empty here
    main_mem = ['' for i in range(size)] # '' acts as place-holder 
    
    faults = 0
   
    # Implementing the FIFO 
    for index, page in enumerate(pages):
        for slot in range(len(main_mem)):
    
            # while there's an empty frame keep on inserting until fool and cout the faults 
            if main_mem[slot] == '' and page  not in main_mem:
                # Main_mem has some free slots  
                main_mem[slot] = page
                q.append(page)
                faults +=1
            # here handle the page fault when the main_mem is full 
            elif (page not in main_mem and index>=size) and '' not in main_mem:
                try:
                    # pop left for deleting the first 
                    main_mem[main_mem.index(q.popleft())] = page
                except IndexError:
                    # Queue is sow empty can't delete"
                    pass
                q.append(page)
                faults +=1
                break
                          
    return faults

def LRU(size,pages):
    hash_table = {}#  {page:count}
    main_mem = ['' for i in range(size)] # '' acts as place-holder 
        
    count = 0 # acts as our time
    faults = 0
    
    # enamerate returns a tuple (the index,the value) 
    for index, page in enumerate(pages):
        for slot in range(len(main_mem)):
        
            # while there's an empty frame keep on inserting until fool and cout the faults 
            
            # Main_mem has some free slots and insert when not found   
            if main_mem[slot] == '' and page not in main_mem:

                count += 1
                main_mem[slot] = page
                hash_table[page] = count
                faults += 1
               
              
                break
                
           # if there's hit but the main_mem is not full apdate the timer for that value
            elif page in main_mem and ''  in main_mem:
                count += 1
                hash_table[page] = count
                break
                
            # here the main_mam will be full
            elif index>=size and '' not in main_mem:
                
                count +=1
                hash_table[page] = count
                if page not in main_mem:       
                    key = lru_min(hash_table,main_mem,page)  
                    # replace
                    main_mem[main_mem.index(key)] = page
                    faults += 1
                   
                break
    return faults

def OPT(size,pages):

    main_mem = ['' for _ in range(size)] # '' acts as place-holder 
    faults = 0
        
    # Implementing the OPT 
    for index, page in enumerate(pages):
        for slot in range(len(main_mem)):
            
            # while there's an empty frame keep on inserting until fool and cout the faults 
            while main_mem[slot] == '' and page not in main_mem:
                # Main_mem has some free slots  
                main_mem[slot] = page
                faults +=1
            # here handle the page fault when the main_mem is full 
            if (page not in main_mem and index>=size) and '' not in main_mem:
            
                for idx,pg in enumerate(main_mem):
                    arr = pages[index:] # the subset of the bigger data
                    # if a page not used at all in the fucture, just replace it 
                    if pg not in arr:
                        if page not in main_mem:
                            main_mem[main_mem.index(pg)] = page
                        break
                    
                    # else find the max index of the page that's gonna be used later and replace it 
                    else:
                        # check if no the item is on the pages subset and pass(do nothing) if not 
                        try:
                            # assume the max-lenght to at zero, then iterate through main memory change it if it's less
                            if idx == 0:
                                mx = arr.index(main_mem[idx])# assume this is max
                                
                                for i in range(1,len(main_mem)):
                                    if mx < arr.index(main_mem[i]):
                                        mx = arr.index(main_mem[i])
                                # check for duplicates 
                                if page not in main_mem:
                                    main_mem[main_mem.index(arr[mx])] =  page
                                
                                pass
                            # Assume is at the last index and go backwards to compare, to find the max, change it if it's less
                            elif idx == len(main_mem) -1 :
                                mx = arr.index(main_mem[idx]) # assume this is max
                                for i in range(idx,-1,-1):
                                    if mx < arr.index(main_mem[i]):
                                        mx = arr.index(main_mem[i])
                                
                                # check for duplicates
                                if page not in main_mem:
                                    main_mem[main_mem.index(arr[mx])] =  page
                                
                                pass
                            # It can be anywhere between 0 and size - 1, find the max 
                            elif idx > 0 and idx < len(main_mem) -1:
                                
                                mx = arr.index(main_mem[idx])
                                
                                # search going forward 
                                for i in range(idx+1,len(main_mem)):
                                    if mx < arr.index(main_mem[i]):
                                        mx = arr.index(main_mem[i])
                                
                                # seach going backwards    
                                for j in range(idx-1,-1,-1):
                                    if mx < arr.index(main_mem[j]):
                                        mx = arr.index(main_mem[j])
                                        
                                # replace make sure no duplicates
                                if page not in main_mem:
                                    main_mem[main_mem.index(arr[mx])] =  page
                                
                               
                                pass
                        except ValueError:
                            # just do nothing 
                            pass
                faults += 1     
                pass
                                
    return faults

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage : python3.py [number of pages] ')
    else:
        main()
