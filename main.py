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

# an exploration of CRC calculation following along with 
# http://www.ross.net/crc/download/crc_v3.txt
# also see these resources
# https://en.wikipedia.org/wiki/Computation_of_cyclic_redundancy_checks

import math
import random
from polynomial import polynomial

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
#  1000000 <-- x^6
#   100000 <-- x^5
#    10000 <-- x^4
#     1000 <-- x^3 \
#     1000 <-- x^3 | - 3*x^3
#     1000 <-- x^3 /
#      100 <-- x^2
#       10 <-- x^1
# +      1 <-- x^0
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
print('example of binary arithmetic with no carries')
pA = polynomial(b'\x9B')
pB = polynomial(b'\xCA')
print(' ' + str(pA))
print('+' + str(pB))
print('--------')
print(' ' + str( pA + pB ))

print()
print('there are only four cases for each bit position')
p0 = polynomial(b'\x00', bits=1)
p1 = polynomial(b'\x01', bits=1)
print(str(p0)+'+'+str(p0)+'='+str(p0+p0))
print(str(p0)+'+'+str(p1)+'='+str(p0+p1))
print(str(p1)+'+'+str(p0)+'='+str(p1+p0))
print(str(p1)+'+'+str(p1)+'='+str(p1+p1)+'  (no carry)')

print()
print('subtraction is identical')
print(' ' + str(pA))
print('-' + str(pB))
print('--------')
print(' ' + str( pA - pB ))

print()
print('with')
print(str(p0)+'-'+str(p0)+'='+str(p0-p0))
print(str(p0)+'-'+str(p1)+'='+str(p0-p1)+'  (wraparound)')
print(str(p1)+'-'+str(p0)+'='+str(p1-p0))
print(str(p1)+'-'+str(p1)+'='+str(p1-p1))

print()
# There may be a typo in the original text on this section. It should say:
#   1001 = 1010 + 0011
#   1001 = 1010 - 0011
# But instead it lists 1010 in both the 1010 position and also the 1001 position
print('Binary ariethmetic w/o carry makes nonsense of any (traditional) notion of order')
pA = polynomial(b'\x0a', bits=4)
pB = polynomial(b'\x03', bits=4)
print(str(pA+pB)+' = '+str(pA)+' + '+str(pB))
print(str(pA-pB)+' = '+str(pA)+' - '+str(pB))

print()
print('Multiplication is absolutely straightforward, being the sum of the\nfirst number, shifted in accordance with the second number.')
# So why does Ross Williams say that the result is just:
# 'the sum of the first number, shifted in accordance with the second number?'
# That part may seem a little obscure but we have to remember the origins of the binary arithmetic w/o carries

# Lets do a few examples to get a feel:
# 1   x 1101 ? well clearly just 1101
# 10  x 1101 ? okay that is:
#              x^1 * (x^3 + x^2 + x^0)
#              x^4 + x^3 + x^1
#              which is 11010  <> notice that this is 1101 shifted left by one bit...
# 100 x 1101 ? alright:
#              x^2 * (x^3 + x^2 + x^0)
#              x^5 + x^4 + x^2
#              which is 110100 <> notice again, the result is 1101 shifted left by two bits
# 
# We can see a pattern as well as it's mathematic origins.
# With only one binary coefficient set the x^n (where n is the nth bit that is set) term
# distributes into the other terms and only changes their order (power). Well the order in
# polynomial arithmetic determines which bit is used to represent that coefficient. Finally 
# thanks to the multiplicative exponent rule we know that a number with the nth bit set will
# add n to the order of all the terms in the result. That is equivalent to adding n to the 
# index of the bit used to represent the coefficient - i.e. shifting the bits left.
#
# When multiplying a more complex pair you can decompose into additions for the multiplication 
# of each individual bit index.
#
# (this text example reflects that of the original text adding powers 
#  of '1011' to demonstrate that multiplication is commutative)
# 
#     1011
#   x 1101
#     ----
#     1011
#    0000.
#   1011..
#  1011...
#  -------
#  1111111  Note: the sum uses CRC addition
#
pA = polynomial(b'\x0d', bits=4)
pB = polynomial(b'\x0b', bits=4)
print('   '+str(pA))
print(' x '+str(pB))
print('   ----')
print('   '+str(1*(pA << 0)))
print('  '+str(1*(pA << 1)))
print(' '+str(0*(pA << 2)))
print(''+str(1*(pA << 3)))
print('-------')
print(pA*pB)

print()
print('Division is a little messier as we need to know when "a number goes into another number"')
pN = polynomial(b'\x35\xb0', bits=14)
pD = polynomial(b'\x13\xb0', bits=5)
print('-- in this example the quotient is not calculated --')
def long_division_crc(pN, pD):
    pW = pN
    pW_virtual_bits = pW.bits
    print('       ---------------')
    print(str(pD)+' ) '+str(pW))
    for i in range(pN.bits-pD.bits,-1,-1):
        s = ' '*(8+(pN.bits-pD.bits-i))
        if(pW/(pD<<i)):
            print(s+str(pD<<i))
            pW -= (pD<<i)
        else:
            print(s+str(p0*(pD<<i)))
        print(s+'-----')
        pW_virtual_bits-=1
        print(' '+s+pW.to_str(pW_virtual_bits))
    print('The remainder is the CRC checksum')
    return pW[0:pD.bits-1]

print(long_division_crc(pN, pD))

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
print('8. A Straightforward CRC Implementation')
print('---------------------------------------')

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

def rand_byte():
    return random.getrandbits(8)

def aa_byte():
    return 0xaa

bits = 32
p = polynomial.from_random(bits, aa_byte)
print('p: ' + str(p))

a = polynomial(bytearray(math.ceil(bits/8)))
g = polynomial(b'\xed', bits=5)
print('g: ' + str(g))
a[1:10:2] = g
print('a: ' + str(a))
