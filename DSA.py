from random import getrandbits
from math import sqrt
from sys import exit
from gmpy2 import is_prime   	# miller-rabin primality test
from gmpy2 import powmod		# (x ** y) mod m
from sys import stdin

# z^-1 mod a
def inverse(z,a):
	if z > 0 and z < a and a > 0:
		i = a
		j = z
		y1 = 1
		y2 = 0
		while j > 0:
			q = i/j
			r = i-j*q
			y = y2 - y1*q
			i, j = j, r
			y2, y1 = y1, y
		if i == 1:
			return y2 % a
    
	raise Exception('Inverse Error')

# Per-Message Secret Number generator
def number_gen(p,q,g):
	N = no_bits(p)
	c = getrandbits(N+64)
	k = (c % (q-1))+1
	try:
		k_ = inverse(k,q)
		return (k,k_) 
	except 'Inverse Error':
		return number_gen(p,q,g)
# Sign opertation
def sign((p,q,g), H, (x, y)):
	k,k_ = number_gen(p,q,g)
	r = powmod(g,k,p) % q
	z = long(H, 16)
	s = (k_*(z+x*r)) % q

	return (r, s)

# Verify operation
def verify((p,q,g), H, y, (r,s)):
	if 0 < r and r < q and 0 < s and s < q:
		w = inverse(s, q)
		z = long(H, 16)
		u1 = (z*w) % q
		u2 = (r*w) % q
		v = ((powmod(g,u1,p) * powmod(y,u2,p)) % p) % q
		return v == r
	raise Exception('Verify Error')
		
def is_valid(p,q,g):
	return  ( is_prime(p) and is_prime(q)
			and no_bits(p) == 1024 and no_bits(q) == 160
			and (p-1) % q == 0 and powmod(g,q,p) == 1 and g > 1)

# number of bits
def no_bits(p):
	return (len(bin(p))-2)

def range_(begin, stop):
   i = begin
   while i < stop:
       yield i
       i += 1

def group(list, n):
	return zip(* [list[i::n] for i in range(n)])

def gen_pair((p,q,g)):
        N = no_bits(p)
	c = getrandbits(N+64)
        x = (c % (q-1)) + 1
        y = powmod(g,x,p)
        return (x,y)

if __name__=='__main__':

	p = long(raw_input()[2:])
	q = long(raw_input()[2:])
	g = long(raw_input()[2:])

	if not is_valid(p,q,g):
		print 'invalid_group'
		exit(-1)

	print 'valid_group'

	token = raw_input()
	if token == 'genkey':
                n = long(raw_input()[2:])
                while n > 0:
                        (x,y) = gen_pair((p,q,g))
                        print "x=" + str(x)
                        print "y=" + str(y)
                        n -= 1

	elif token == 'sign':
		x = long(raw_input()[2:])
		y = long(raw_input()[2:])
		Ds = [l[2:-1] for l in stdin]
		signs = [sign((p,q,g), d, (x,y)) for d in Ds]
		for (r,s) in signs:
			print 'r='+str(r)
			print 's='+str(s)

	elif token == 'verify':
		y = long(raw_input()[2:])
		tuples = group([l[2:-1] for l in stdin], 3)  # tuples (D, r, s)
		verifies = [verify((p,q,g), t[0], y, (long(t[1]), long(t[2]))) for t in tuples]
                for v in verifies:
                        if v:
                                print 'signature_valid'
                        else:
                                print 'signature_invalid'
