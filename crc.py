# an exploration of CRC calculation following along with 
# https://en.wikipedia.org/wiki/Computation_of_cyclic_redundancy_checks
# and
# http://www.ross.net/crc/download/crc_v3.txt

import math

# Here is a first draft of some pseudocode for computing an n-bit CRC. It uses a contrived composite 
# data type for polynomials, where x is not an integer variable, but a constructor generating a Polynomial 
# object that can be added, multiplied and exponentiated. To xor two polynomials is to add them, modulo 
# two; that is, to exclusive OR the coefficients of each matching term from both polynomials.

class polynomial:
    def __init__ (self, data, bits=0, order='big'):
        data = bytearray(data)
        self.data = data
        self.order = order
        self.bits = bits
        if(bits==0):
            self.bits = 8*len(data)

    def __xor__(self, o):
        size = min(self.bits, o.bits)
        retval = polynomial(bytearray(math.ceil(size/8)), bits=size)
        for bit in range(size):
            retval.set_bit(bit, self.get_bit(bit) ^ o.get_bit(bit))
            # print( str(self.get_bit(bit)) + ' ^ ' + str(o.get_bit(bit)) + ' = ' + str(retval.get_bit(bit)) )
        return retval

    def __lshift__(self, num):
        new_bits = self.bits + num
        high_bit_index = self.get_highest_bit_index()
        if( (high_bit_index + num) > (self.get_max_bit_index()) ):
            bytes_to_add = math.ceil(((high_bit_index + num) - (self.get_max_bit_index()))/8)
            self.add_high_bytes(bytes_to_add)
            self.bits = new_bits

        print('NEED TO WORK ON LSHIFT OPERATOR!')

        # reach_back_bytes = math.ceil(num/8)
        # print('reach back bytes: '+str(reach_back_bytes))
        # for b in range(len(self.data)):
        #     ind = self.get_byte_index_by_byte(b)                    # account for endianness
        #     reach_back_ind = self.get_byte_index_by_byte(b-reach_back_bytes)

        #     # print(ind)
        #     print(reach_back_ind)

        #     # tempH = (self.data[ind] << num)                         # shift the current byte (when num is small this may retain some bits)
        #     # tempL = 0                                               # shift in zeroes from infinity
        #     # if(ind>=reach_back_bytes):                              # if there are lower bytes...
        #     #     tempL = (self.data[ind-reach_back_bytes] << num)    # we want to capture carry bits

        #     # print('tempH: '+str(hex(tempH))+', tempL: '+str(hex(tempL)))
            
        #     # # self.data[ind] = (tempH | tempL)                        # store the new data


        #     # 
        #     # print('shifting over data in byte: '+str(b)+', temp = '+str(hex(temp)))
        #     # self.data[b] = temp
            

        # # self.bits += num
        # # # shift over data by num bits

        return self

    # def __rshift__(self, num):
    #     # shift over data by num bits

    def set_bit(self, bit, val):
        if( bit >= self.bits ):
            return 0
            
        byte = self.get_byte_index_by_bit(bit)
        temp = self.data[byte]
        temp &= ~(0x01 << (bit%8))
        if(val):
            temp |= (0x01 << (bit%8))
        
        self.data[byte] = temp
    
    def get_bit(self, bit):
        if( bit >= self.bits ):
            return 0

        byte = self.get_byte_index_by_bit(bit)
        if(self.data[byte] & (0x01 << (bit%8))):
            return 1
        return 0
    
    def get_byte_index_by_bit(self, bit):
        if( bit >= self.bits ):
            return 0

        if(self.order=='big'):
            return ( math.ceil(self.bits/8) - 1 - math.floor(bit/8) )
        return math.floor(bit/8)
    
    def get_byte_index_by_byte(self, b):
        if(self.order=='big'):
            return (len(self.data)-1-b)
        else:
            return b

    def add_high_bytes(self, num):
        self.bits += 8*num
        if(self.order=='big'):
            temp = bytearray(num)
            temp.extend(self.data)
            self.data = temp
        else:
            self.data.extend(bytearray(num))

    def get_highest_bit_index(self):
        for index in range(self.bits-1, -1, -1):
            if(self.get_bit(index)):
                return index
    
    def get_max_bit_index(self):
        return ((len(self.data)*8) - 1)

    def __repr__(self):
        return 'crc polynomial'
    def __str__(self):
        return ( ('polynomial class with:\n') + ('bits: ' + str(self.bits)) + ('\ndata:' + str(self.data)) + '\n' )
        


# So to implement CRC division, we have to feed the message through a
# division register. At this point, we have to be absolutely precise
# about the message data. In all the following examples the message will
# be considered to be a stream of bytes (each of 8 bits) with bit 7 of
# each byte being considered to be the most significant bit (MSB). The
# bit stream formed from these bytes will be the bit stream with the MSB
# (bit 7) of the first byte first, going down to bit 0 of the first
# byte, and then the MSB of the second byte and so on.

# With this in mind, we can sketch an implementation of the CRC
# division. For the purposes of example, consider a poly with W=4 and
# the poly=10111. Then, the perform the division, we need to use a 4-bit
# register:

#                   3   2   1   0   Bits
#                 +---+---+---+---+
#        Pop! <-- |   |   |   |   | <----- Augmented message
#                 +---+---+---+---+

#              1    0   1   1   1   = The Poly

# (Reminder: The augmented message is the message followed by W zero bits.)

# To perform the division perform the following:

#    Load the register with zero bits.
#    Augment the message by appending W zero bits to the end of it.
#    While (more message bits)
#       Begin
#       Shift the register left by one bit, reading the next bit of the
#          augmented message into register bit position 0.
#       If (a 1 bit popped out of the register during step 3)
#          Register = Register XOR Poly.
#       End
#    The register now contains the remainder.

# (Note: In practice, the IF condition can be tested by testing the top
#  bit of R before performing the shift.)

# We will call this algorithm "SIMPLE".


def crc_simple( msg, poly ):
    # poly should be the generator polynomial in shortened form (i.e. do not include the MSB -- an N-bit poly will have an assumed '1' bit in the N bit position)
    # msg shoul be UNaugmented
    
    W = poly.bits                                                           # find the required register width
    register = polynomial(polynomial(bytearray(math.ceil(W/8)), bits=W))    # create the CRC division register with width W

            





# msg = polynomial(b'\xDE\xA3')
# poly = polynomial(b'\x0B',bits=4)

# result = (msg ^ poly)
# result.print_self()

msg = polynomial(b'\x57\x00')
poly = polynomial(b'\x01\x07',bits=9)

# crc_cs1( msg, poly )


# poly.add_high_bytes(1)

# test = polynomial(b'\x01',bits=1)
test = polynomial(b'\x81',bits=8)
print(test)

test <<= 9

print(test)