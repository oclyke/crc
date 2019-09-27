# Copyright (c) 2019 Owen Lyke

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import math

# Here is a first draft of some pseudocode for computing an n-bit CRC. It uses a contrived composite 
# data type for polynomials, where x is not an integer variable, but a constructor generating a Polynomial 
# object that can be added, multiplied and exponentiated. To xor two polynomials is to add them, modulo 
# two; that is, to exclusive OR the coefficients of each matching term from both polynomials.


def poly_access_exception(index, poly):
    return ('polynomial: index out of range. requested: {}, max: {}'.format(index, poly.bits-1))

def poly_type_exception():
    return ('polynomial: need polynomial type as argument')

def poly_size_exception(size, poly):
    return ('polynomial: need polynomial of length {}, got length {}'.format(size, poly.bits))

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

    def check_index(self, index):
        if((index < 0) or (index >= self.bits)):
            raise Exception(poly_access_exception(index, self))

    def __add__(self, o):
        return (self^o)

    def __sub__(self, o):
        return (self^o)
    
    def __mul__(self, o):
        if isinstance(o, polynomial):
            size = (self.bits + o.bits)
            if(size > 1):
                size -= 1
            retval = polynomial(bytearray(math.ceil(size/8)), bits=size)
            for bit in range(o.bits):
                if(o[bit]):
                    retval += (self << bit)
            return retval
        else:
            size = (self.bits)
            retval = polynomial(bytearray(math.ceil(size/8)), bits=size)
            for bit in range(retval.bits):
                retval.set_bit(bit, self.get_bit(bit)*o)
            return retval

    def __rmul__(self, o):
        return self * o

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
        if(self.bits >= o.bits):
            for bit in range(size):
                retval[bit] = self[bit]
        else:
            for bit in range(size):
                retval[bit] = o[bit]
        for bit in range(min(self.bits, o.bits)):
            retval[bit] = (self[bit] ^ o[bit])
        return retval

    def __lshift__(self, num):
        size = self.bits + num
        retval = polynomial(bytearray(math.ceil(size/8)), bits=size)
        for i in range(self.bits):
            retval[i+num] = self[i]
        for i in range(num):
            retval[i] = 0
        return retval

    # def __rshift__(self, num):
    #     # shift over data by num bits

    def __getitem__(self, key):
        if isinstance(key, slice):
            self.check_index(key.start)
            self.check_index(key.stop)
            request = range(key.start, key.stop, 1 if (key.step == None) else key.step)
            size = len(request)
            retval = polynomial(bytearray(math.ceil(size/8)), bits=size)
            for i in range(len(request)):
                retval[i] = self[request[i]]
                # This method returns a condensed polynomial, as opposed to leaving locations intact
            return retval
        else:
            self.check_index(key)
            return self.get_bit(key)

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            self.check_index(key.start)
            self.check_index(key.stop)
            request = range(key.start, key.stop, 1 if (key.step == None) else key.step)
            size = len(request)
            if not isinstance(value, polynomial):
                raise Exception(poly_type_exception())
            if( value.bits != size ):
                raise Exception(poly_size_exception(size, value))
            for i in range(len(request)):
                self[request[i]] = value[i]
                # This expands a condensed poly into the desired slice, as opposed to preserving index locations
            return self
        else:
            self.check_index(key)
            self.set_bit(key, value)
            return self


    def set_bit(self, bit, val):
        if( bit >= self.bits ):
            return self
        byte = self.get_byte_index_by_bit(bit)
        temp = self.data[byte]
        temp &= ~(0x01 << (bit%8))
        if(val):
            temp |= (0x01 << (bit%8))
        self.data[byte] = temp
        return self
    
    def get_bit(self, bit):
        self.check_index(bit)
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
            if(self[index]):
                return index
        return 0
    
    def get_max_bit_index(self):
        return ((len(self.data)*8) - 1)

    def to_str(self, bits=None):
        return (''.join(map(str, (self[i] for i in range((self.bits if (bits == None) else bits)-1, -1, -1))))) # print bit representation

    def __repr__(self):
        return ( ('polynomial class with:\n') + ('bits: ' + str(self.bits)) + ('\ndata:' + str(self.data)) + '\n' ) # print information
    def __str__(self):
        return self.to_str()
