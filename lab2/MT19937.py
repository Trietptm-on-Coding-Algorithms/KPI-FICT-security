def _int32(x):
	return int(0xFFFFFFFF & x)


class MT19937:
	def __init__(self, seed, state=False):
		self.index = 624
		if state:
			self.mt = seed
		else:
			self.mt = [0] * 624
			self.mt[0] = seed
			for i in range(1, 624):
				self.mt[i] = _int32(
					1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i)

	def print_state(self):
		print(self.mt)

	def extract_number(self):
		if self.index >= 624:
			self.twist()

		y = self.mt[self.index]

		y = y ^ y >> 11
		y = y ^ y << 7 & 0x9d2c5680
		y = y ^ y << 15 & 0xefc60000
		y = y ^ y >> 18

		self.index = self.index + 1

		return _int32(y)

	def twist(self):
		for i in range(624):
			y = _int32((self.mt[i] & 0x80000000) + (self.mt[(i + 1) % 624] & 0x7fffffff))
			self.mt[i] = self.mt[(i + 397) % 624] ^ y >> 1

			if y % 2 != 0:
				self.mt[i] = self.mt[i] ^ 0x9908b0df
		self.index = 0
