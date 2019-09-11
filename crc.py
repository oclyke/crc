# an exploration of CRC calculation following along with 
# https://en.wikipedia.org/wiki/Computation_of_cyclic_redundancy_checks
# and
# http://www.ross.net/crc/download/crc_v3.txt

import math




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