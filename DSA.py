from random import getrandbits

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
	N = (len(bin(p))-2)
	c = getrandbits(N+64)
	k = (c % (q-1))+1
	try:
		k_ = inverse(k,q)
		return (k,k_) 
	except 'Inverse Error':
		return number_gen(p,q,g)

def sign((p,q,g),z, H, (x, y)):
	k,k_ = number_gen(p,q,g)
	r = ((g**k)%p)%q
	z = long(H, 16)
	s = (k_*(z+x*r)) % q

	return (r, s)
