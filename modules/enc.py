import string, random

class ENC():
	def __init__(self, separator):
		self.separator = separator
		self.punctuation = string.punctuation

	def genID(self, length):
		simbols = string.ascii_letters + string.punctuation + string.digits
		return ''.join(random.choice(simbols) for i in range(length))

	def encrypt(self, text, KEY):
		result = ""
		for simbol in text:
			code = ord(simbol)
			# code transformation
			start_fake = random.randint(1, 9)
			end_fake = random.randint(0, 9)
			res = str(start_fake) + str(int(((code * KEY) / len(str(KEY)) + (end_fake * len(str(KEY)) - end_fake)) * start_fake)) + str(abs(end_fake - start_fake))
			int_code = ""

			for i in range(len(res)):
				for t in range(int(res[i])):
					int_code += self.separator.dot

				int_code += self.separator.dot_sep

			result += int_code[:len(int_code) - 1] + self.separator.global_sep

		return result[:len(result) - 1]

	def decrypt(self, code, KEY):	
		result = ""
		int_codes = code.split(self.separator.global_sep)

		for int_code in int_codes:
			number = ""
			dots = int_code.split(self.separator.dot_sep)
			for dot in dots:
				middle_num = 0
				for i in range(len(dot)):
					middle_num += 1
				number += str(middle_num)

			# code transformation		
			res_arr = list(str(number))
			start_fake = res_arr[0]
			end_fake = int(res_arr[len(res_arr) - 1]) + int(start_fake)
			del res_arr[0]
			del res_arr[len(res_arr) - 1]

			res = int(''.join(res_arr))
			res = round((((res - (end_fake * len(str(KEY)) - end_fake)) * len(str(KEY))) / KEY) / int(start_fake))

			try:
				result += chr(res)
			except:
				result += random.choice(self.punctuation)

		return result