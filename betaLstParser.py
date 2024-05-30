import numpy as np
import csv

def parseBetaBinary(filePath):

    bMasks  = np.zeros(4,dtype=np.uint64)
    bShifts = np.zeros(4,dtype=np.uint64)
    bitPos = [[ 0,13], [14,15], [16,59], [60,63]] #big endian encoding for <val,ch,time,empty>

    for n,pos in enumerate(bitPos):
        print(pos)
        bMasks[n]  = sum([2**i for i in range(pos[0],pos[1]+1)])    # mask for bitwise operation
        bShifts[n] = pos[0]                                         # shift bits to get correct value
    

    data = np.fromfile(filePath, dtype=np.dtype('>u8'))

    #lstType = np.dtype([('val', np.uint16), ('ch', np.uint8 ), ('time', np.uint64), ('empty', np.uint8 )]) # for full parsing, make sure parseIter is correct if using this
    lstType = np.dtype([('time', np.uint64), ('ch', np.uint8), ('val', np.uint16)])
    
    parseIter = ((((x&bMasks[2]) >> bShifts[2]) * 40, # 40 ns per bit
                  ((x&bMasks[1]) >> bShifts[1]) + 1,  # ch number starts from 1
                   (x&bMasks[0]) >> bShifts[0]) for x in data[:10])
    parsed = np.fromiter(parseIter,dtype=lstType)                              # parse data into parameters
    return parsed

# in UTF-8 format (human-readable)
def writeBetaLst(data,filePath):
    with open(filePath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in data: writer.writerow(row)
