import math

class Source(object):
	def __init__(self, Statistics, Variable_Names):
		# Statistics = the dictionary of n-tuple {case : number of occations} , Variable_Names = names of elements of n-tuple
		self.Statistics = Statistics
		self.Variable_Names = Variable_Names

	# P(List_of_Mesh_Variables, Other_Variables) -> P(List_of_Mesh_Variables)
	def Meshed_for_(self, List_of_Mesh_Variables):
		if List_of_Mesh_Variables == []:
			return self.Statistics

		Mesh_Index = []
		for Mesh_Var in List_of_Mesh_Variables:
			Mesh_Index.append(self.Variable_Names.index(Mesh_Var))

		Meshed_Statistics = {}
		for a_Case in self.Statistics:
			mesh_case = self.Mesh_Tuple(a_Case, Mesh_Index)
			if mesh_case in Meshed_Statistics:
				Meshed_Statistics[mesh_case] += self.Statistics[a_Case]
			else:
				Meshed_Statistics[mesh_case] = self.Statistics[a_Case]
		return Meshed_Statistics

	def Mesh_Tuple(self, Raw_Tuple, Mesh_Index):
		Result = []
		for index in Mesh_Index :
			Result.append(Raw_Tuple[index])
		return tuple(Result)

	def Generate_Probability_Distribution_Function(self, Statistics):
		Total = self.Calculate_Total_Occurance(Statistics)
		PDF = {}
		for a_Case in Statistics:
			PDF[a_Case] = Statistics[a_Case]/Total
		return PDF

	def Generate_Desired_PDF(self, List_of_Mesh_Variables):
		return self.Generate_Probability_Distribution_Function(self.Meshed_for_(List_of_Mesh_Variables))

	def Calculate_Total_Occurance(self, Statistics):
		Total = 0
		for a_Case in Statistics:
			Total += Statistics[a_Case]
		if Total == 0:
			raise ValueError("Zero total occurrence in statistics")
		return Total
	


		

