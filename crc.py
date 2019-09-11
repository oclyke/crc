# an exploration of CRC calculation following along with 
# https://en.wikipedia.org/wiki/Computation_of_cyclic_redundancy_checks
# and
# http://www.ross.net/crc/download/crc_v3.txt

import math

print('1. Introduction: Error Detection')
print('--------------------------------')
# Checksums are values transmitted along with a message to detect errors introduced in the transmission/
# reception process, but they are not all created equally secure

print()
print('2. The Need For Complexity')
print('--------------------------')
# Here the text describes that the two criteria for a good checksum are
#   WIDTH - reduces the probability that an erroneous checksum will match a valid checksum
#   CHAOS - allows for full utilization of a wide checksum

print()
print('3. The Basic Idea Behind CRC Algorithms')
print('---------------------------------------')
# Ross Williams explains that while simple addition is not chaotic enough division is as long as the 
# divisor is about as 'wide' as the checksum register. 
# (Here 'wide' roughly means how many binary digits there are before the most significant bit that is set)
# The reason that this is important is because the remainder is used as the checksum, and the remainder
# cannot be larger than the divisior
# The remainder is a good checksum b/c it is affected pretty equally by each bit in the dividend (the message)

print()
print('4. Polynomical Arithmetic')
print('-------------------------')
# To make division more applicable to the computer systems on which CRC checksums are implemented we introduce
# 'Polynomial Arithmetic.' (P.A.) Generally this is covered very well by R. Williams, but there are a few points to 
# explicate.

# In P.A. numbers are represented as polynomials with binary coefficients. e.g:
# (23) is (0x17) is (0b10111) is (1*x^4 + 0*x^3 + 1*x^2 + 1*x^1 + 1*x^0) or (x^4 + x^2 + x^1 + x^0) when zero-coefficients are omitted

# To multiply 1101 by 1011 perform the P.A:
# (x^3 + x^2 + x^0)(x^3 + x^1 + x^0)
# x^6 + x^5 + x^4 + 3*x^3 + x^2 + x^1 + x^0

# However this is an 'invalid' result in P.A. because it contians a non-binary coefficient (3) for the x^3 term
# R. Williams explains that 
# 'to get the right answer, we have to pretend that x is 2 and propagate binary carries from the 3*x^3 yielding
#   x^7 + x^3 + x^2 + x^1 + x^0'

# To make this step as clear as it can be let's consider that any polynomial simply represents a sum of addition-
# compatible terms - each x^n term can always be added with each other but without knowning the value of x you
# cannot make precise statements about the relationship of, say, x^m wrt x^p. That point is made clear in the original
# text. So what the polynomial (x^6 + x^5 + x^4 + 3*x^3 + x^2 + x^1 + x^0) tells us is that it is the sum of these polys:
#
#    1 <-- this is the carry result from adding up 3 of the 1000 terms
#   1  <-- subsequent carries
#  1   <-- 
# 1    <--
#  1000000
#   100000
#    10000
#     1000
#     1000
#     1000
#      100
#       10
# +      1
# --------
# 10001111

# The result here is indeed equivalent (in P.A.) to (x^7 + x^3 + x^2 + x^1 + x^0). This illustrates what is meant by:
# 'propagate binary carries from the 3*x^3'

# The original text clearly explains the advantages of performing the arithmetic in terms of polynomials

print()
print('5. Binary Arithmetic with No Carries')
print('------------------------------------')
# This section explains the particular flavor of polynomial arithmetic that is used in CRC calculation
# The most useful fact is that binary arithmetic with no carries only operates within a given bit position, reducing state.

print()
print('6. A Fully Worked Example')
print('-------------------------')
# Here the original text performs a long division using 'binary arithmetic without carries' which is an equivalent operation
# to the core of CRC generation algorithms.

print()
print('7. Choosing A Poly')
print('------------------')
# Interesting math + implemntation facts that are best explianed in the original text

print()




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