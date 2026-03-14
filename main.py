def calcrc(buf, lbuf):
    #crc=0xFFFF
    ch = 0xFF
    cl = 0xFF

    for i in range(lbuf + 1):
        cl = cl ^ buf[i]        #we are getting remainders after XOR

        for ctrc in range(8):   #this processes byte, as every byte has 8 bits
            carryh = ch % 2     #we are checking if the lowest bit of ch is 1 or 0, if it is 1 then carryh will be 1 otherwise it will be 0
            carryl = cl % 2

            #Right shifting Mechanism
            ch = ch // 2          # // this is floor division- 7/2=3 not 3.5, which is equivalent to right shift by 1
            #high bit of cl will shift into low bit of ch
            #ch LSB is MSB of cl, so we add 128 to cl if carryh is 1
            cl = (128 * carryh) + (cl // 2)

            if carryl != 0:  #if carryl is 1, we need to XOR with the polynomial
                ch = ch ^ 0xA0
                cl = cl ^ 0x01
                #crc=crc ^ 0xA001

    return ch, cl
    #return crc


packet=input("Enter the data of 8 byte in hexadecimal (e.g., A1 03 00 00 00 0F 1D 6E): ").split()
print(f"Packet: {packet}")
packet = [int(x, 16) for x in buffer]  # Convert hexadecimal input
#buffer = [0xA1, 0x03, 0x00, 0x00, 0x00, 0x0F]  # Data in hexadecimal
data=[]
crc=[]
#splitting packet into 'data' and 'crc'
for d in range(6):
    data.append(packet[d])
ldata=len(data)-1
crc.append(packet[6])
crc.append(packet[7])
cl,ch=calcrc(data,ldata)


print(f"Packet: {packet}")
print(f"Data: {data} \n CRC: {crc}")
print(f"[CRCH: {ch:02x} , CRCL: {cl:02x}]")

#checking data integrity
if crc[0]==ch and crc[1]==cl:
    print("Data is Intact")
else:
    print("Data is varied!")
