import math


class Entropy():
	def __init__(self, Source_Statistics, For = []):
		self.PDF = Source_Statistics.Generate_Desired_PDF(For)
		self.Value = 0

		self.Calculate_Entropy()

	def Calculate_Entropy(self):
		self.Value = 0
		for case_p in self.PDF:
			p = self.PDF[case_p]
			if p != 0:
				self.Value -= p*math.log(p)
		return

class Conditional_Entropy():
	def __init__(self,Source_Statistics, For = [], Known = []):
		if len(Known) == 0 :
			self.Value = Entropy(Source_Statistics, For).Value
		else:
			self.H_x = Entropy(Source_Statistics, Known).Value
			self.H_xy = Entropy(Source_Statistics, For+Known).Value
			self.Value = self.H_xy - self.H_x
		
class Mutual_Information():
	def __init__(self,Source_Statistics, For = [], Known = []):
		self.H_x = Conditional_Entropy(Source_Statistics, For = [For[0]], Known = Known).Value
		self.H_y = Conditional_Entropy(Source_Statistics, For = [For[1]], Known = Known).Value
		self.H_xy = Conditional_Entropy(Source_Statistics, For = For, Known = Known).Value
		self.Value = self.H_x + self.H_y - self.H_xy


class Multiple_Mutual_Information():
	def __init__(self,Source_Statistics, For = [], Known = []):
		self.Statistics = Source_Statistics
		Order = len(For) - 1
		self.Value = self.Recursive_Calculation(Order, For = For, Known = Known)

	def Recursive_Calculation(self, Order, For = [], Known = []):
		if Order == 2:
			return Mutual_Information(self.Statistics, For = For[:-1], Known = Known).Value - Mutual_Information(self.Statistics, For = For[:-1], Known = Known + [For[-1]]).Value
		else:
			return self.Recursive_Calculation(Order-1, For = For[:-1], Known = Known) - self.Recursive_Calculation(Order-1, For = For[:-1], Known = Known + [For[-1]])
			
		
		
		
		