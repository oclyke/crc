
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

    @classmethod
    def from_random(cls, bits, rbyte, order='big'):
        data = bytearray(math.ceil(bits/8))
        for i in range(len(data)):
            data[i] = rbyte()
        polynomial = cls(data, bits, order)
        return polynomial

    def __add__(self, o):
        return (self^o)

    def __sub__(self, o):
        return (self^o)
    
    def __mul__(self, o):
        size = (self.bits + o.bits)
        if(size > 1):
            size -= 1
        retval = polynomial(bytearray(math.ceil(size/8)), bits=size)
        for i in range(o.bits):
            if(o.get_bit(i)):
                retval += (self << i)
        return retval

    def __truediv__(self, o):
        # # X is greater than or equal to Y iff the position of the highest 1 bit of 
        # # X is the same or greater than the position of the highest 1 bit of Y.
        if(self.get_highest_bit_index() >= o.get_highest_bit_index()):
            return 1
        else:
            return 0

    def __xor__(self, o):
        size = max(self.bits, o.bits)
        retval = polynomial(bytearray(math.ceil(size/8)), bits=size)
        for bit in range(min(self.bits, o.bits)):
            retval.set_bit(bit, self.get_bit(bit) ^ o.get_bit(bit))
        return retval

    def __lshift__(self, num):
        size = self.bits + num
        retval = polynomial(bytearray(math.ceil(size/8)), bits=size)
        for i in range(self.bits):
            retval.set_bit(i+num,self.get_bit(i))
        for i in range(num):
            retval.set_bit(i, 0)
        return retval

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
        return self
    
    def get_bit(self, bit):
        if( bit >= self.bits ):
            raise Exception('bit index exceeded allocated size. requested index: {}, max index: {}'.format(bit, self.bits))
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
        if(self.order=='big'):
            temp = bytearray(num)
            temp.extend(self.data)
            self.data = temp
        else:
            self.data.extend(bytearray(num))
        return self

    def get_highest_bit_index(self):
        for index in range(self.bits-1, -1, -1):
            if(self.get_bit(index)):
                return index
        return 0
    
    def get_max_bit_index(self):
        return ((len(self.data)*8) - 1)

    def __repr__(self):
        return 'crc polynomial'
    def __str__(self):
        return ( ('polynomial class with:\n') + ('bits: ' + str(self.bits)) + ('\ndata:' + str(self.data)) + '\n' )
        
