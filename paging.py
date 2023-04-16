# Author : Sphesihle Madonsela
# Date 17 April 2022
# CSC3002F OS Assigment 1
# https://nicomedes.assistedcoding.eu/#/app/os/page_replacement
# Link to test the page faults
# copy the output pages remove the square brakets. paste it to the abouve website for testing

from collections import deque
import random
import sys

from typing import List, Dict, Tuple

def main()-> None:

    # the frame size from 1 to 7
    size : int = int(sys.argv[1])


    ref_size:List[int] = [j for j in range(8,65,8)]
    # select the page size at random from 8 to 64

    pages:List[int] = [random.randint(0,9) for _ in range(ref_size[random.randint(0,len(ref_size)-1)])] # array with random numbers

    print(f'N = {len(pages)} pages')
    print(f'pages : {pages}')
    print("FIFO",FIFO(size,pages),'page faults')
    print('LRU',LRU(size,pages),'page faults')
    print('OPT',OPT(size,pages),'page faults')

def FIFO(size:int,pages:List[int])->int:

    q : deque  = deque() # the queue is empty here
    main_mem : List[str] = ['' for _ in range(size)] # '' acts as place-holder

    faults : int  = 0

    # Implementing the FIFO
    for index, page in enumerate(pages):
        for slot in range(len(main_mem)):

            # if there's an empty frame keep on inserting until fool and cout the faults
            if main_mem[slot] == '' and page  not in main_mem:
                # Main_mem has some free slots
                main_mem[slot] = page
                q.append(page)
                faults += 1
            # here handle the page fault when the main_mem is full
            elif (page not in main_mem and index>=size) and '' not in main_mem:
                
                # pop left for deleting the first
                value_to_remove : str = q.popleft()
                
                # Replace the value data in the previous value's index position 
                main_mem[main_mem.index(value_to_remove)] = page
            
                q.append(page)
                faults += 1
                break
    return faults

def LRU(size : int , pages : list)->int:

    hash_table : Dict[int , int] = dict()#  {page:count}

    main_mem : List[str] = ['' for _ in range(size)] # '' acts as place-holder

    count : int = 0 # acts as our time
    faults : int = 0

    # enamerate returns a tuple (the index,the value)
    for index, page in enumerate(pages):
        for slot in range(len(main_mem)):


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

                    # A hash table of those values in memory
                    in_mem_dict : Dict[int,int] = { i : hash_table[i] for i in main_mem }

                    # tuple with sorted value, sort by value-frequency(not by key) hence pair[1]
                    sorted_in_mem_tuple : Tuple[int,int] = sorted(in_mem_dict.items(),key = lambda pair : pair[1])

                    # Sorted hash table
                    sorted_in_mem_hash : Dict[int,int] = dict(sorted_in_mem_tuple)

                    # Get the key of the item with less frequency, since sort it will at index 0
                    value_to_replace : int = list(sorted_in_mem_hash.keys())[0]

                    # Get the index of that item memory replace the date with a new page
                    main_mem[main_mem.index(value_to_replace)] = page
                    # update the faults
                    faults += 1

                break
    return faults

def OPT(size : int ,pages : List[int])->int:

    main_mem : List[int] = ['' for _ in range(size)] # '' acts as place-holder
    faults :int = 0

    # Implementing the OPT
    for index, page in enumerate(pages):
        for slot in range(len(main_mem)):

            # while there's an empty frame keep on inserting until fool and cout the faults
            if main_mem[slot] == '' and page not in main_mem:
                # Main_mem has some free slots
                main_mem[slot] = page
                faults += 1
            # here handle the page fault when the main_mem is full
            elif (page not in main_mem and index>=size) and '' not in main_mem:

                for idx,pg in enumerate(main_mem):
                    arr : List[int] = pages[index:] # the subset of the bigger data
                    # if a page not used at all in the fucture, just replace it
                    if pg not in arr:
                        if page not in main_mem:
                            main_mem[main_mem.index(pg)] = page
                        break

                    # else find the max index of the page that's gonna be used later and replace it
                    else:
                        # check if no the item is on the pages subset and pass(do nothing) if not
                        try:
                            # assume idx=0 is least used in future, then iterate through main memory change it, if it's less
                            # to check if there's an iterm that's least used than that at zero
                            # Least used will have a a big mx value
                            if idx == 0:

                                mx : int = arr.index(main_mem[idx])# assume this is max

                                for i in range(1,len(main_mem)):
                                    if mx < arr.index(main_mem[i]):
                                        mx = arr.index(main_mem[i])
                                # check for duplicates
                                if page not in main_mem:
                                    main_mem[main_mem.index(arr[mx])] =  page

                                pass
                            # Assume is at the last index and go backwards to compare, to find the max, change it if it's less
                            elif idx == len(main_mem) - 1 :
                                mx : int = arr.index(main_mem[idx]) # assume this is max
                                for i in range(idx,-1,-1):
                                    if mx < arr.index(main_mem[i]):
                                        mx = arr.index(main_mem[i])

                                # check for duplicates
                                if page not in main_mem:
                                    main_mem[main_mem.index(arr[mx])] =  page

                                pass
                            # It can be anywhere between 0 and size - 1, find the max
                            elif idx > 0 and idx < len(main_mem) -1:

                                mx : int  = arr.index(main_mem[idx])

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
                            # value not used in later 
                            pass
                faults += 1
                pass

    return faults

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage : python3 pages.py [number of pages] ')
    else:
        main()
