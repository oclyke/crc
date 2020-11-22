### foreward
Ross N. Williams' 19th of August 1993 publication of '```crc_v3.txt```' exemplified the encouraging and kind-spirited nature of the young internet. An ascii work of art the text clearly laid out the fundamentals of the modern cyclic redundancy check. Now that the text is lost from its home ([http://www.ross.net/crc/download/crc_v3.txt](http://www.ross.net/crc/download/crc_v3.txt)) it is up to the next generation to carry the flame. May this repository pay homage to that original spark of generosity. One will also find the file here: [crc_v3.txt](https://oclyke.dev/conservatory/ross.net/crc/download/crc_v3.txt)

## crc exploration
An interactive exploration of Cyclic Redundancy Check (CRC) math/computation following along with '```crc_v3.txt```'

Defines an abstract ```polynomial``` class to represent 'polynomical arithmetic mod 2' which is used in computation of CRCs. This makes it easy to write code such as 

```python
pA = polynomial(b'\x0d', bits=4)
pB = polynomial(b'\x0b', bits=4)

print('pA = ' + str(pA))
print('pB = ' + str(pB))
print('Under polynomical arithmetic mod 2:')
print('pA*pB = ' + str(pA*pB))
```

Output
``` bash
pA = 1011
pB = 1101
Under polynomical arithmetic mod 2:
pA*pB = 1111111
```

Which in turn strengthens the relationship between the mathematical operation of calculating a CRC and the code that is written. 

Of course this is not a 'performance' implementation -- for production use one should use the table-driven CRC generation as described in the ```crc_v3.txt``` document.

## Development Status
In-progress - being a side project there are still some bugs and things left to do. If you want to help out I'd love to hear of issues and pull requests. Thanks!
