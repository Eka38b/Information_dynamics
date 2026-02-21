import math

from on_Model.InfoDyn_lib.Estimators import Estimator_Basics

class Source(Estimator_Basics.Source):
	def __init__(self, Q, Dimension):
		self.Analysis = "Realtime"
		self.Type = "Pairwise"
		
		self.Q = Q
		self.Dimension = Dimension
		self.Statistics = {}	
			
	def Init_Source_Realtime(self, Simulation_Nodes):
		if self.Analysis != "Realtime":
			return
		if self.Type == "Pairwise":
			self.Variable_Names = [Simulation_Nodes[0],Simulation_Nodes[1],Simulation_Nodes[0]+"'",Simulation_Nodes[1]+"'"]
		
		if len(self.Variable_Names) != self.Dimension:
			raise ValueError("Check the Variables")
		self._recursive_Init_Statistics(1, [])
			
	def _recursive_Init_Statistics(self, D, Index_List):
		for i in range(self.Q):
			if D < self.Dimension:
				self._recursive_Init_Statistics(D+1, Index_List+[i])
			else:
				self.Statistics[tuple(Index_List+[i])] = 0
		
	def Update_Source_Realtime(self, State_Space, Update_Buffer):
		if self.Analysis != "Realtime":
			return
		Index_list = []
		for Name in self.Variable_Names:
			if Name[-1] == "'":
				Index_list.append(Update_Buffer[Name[:-1]])
			else:
				Index_list.append(State_Space[Name])
		self.Statistics[tuple(Index_list)] += 1
		
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
			raise ValueError("ERROR : ZERO STAT")
		return Total

class Estimator(Estimator_Basics.Estimator):
	def __init__(self, Q, Dimension):
		self.Name = "Simple_Binning_Method"
		
		self.Source = Source(Q, Dimension)
		
	def Entropy(self, For = []):
		PDF = self.Source.Generate_Desired_PDF(For)
		Value = 0
		for case_p in PDF:
			p = PDF[case_p]
			if p != 0:
				Value -= p*math.log(p)
		return Value
		
	def Conditional_Entropy(self, For = [], Known = []):
		if len(Known) == 0 :
			Value = self.Entropy(For)
		else:
			H_x = self.Entropy(Known)
			H_xy = self.Entropy(For+Known)
			Value = H_xy - H_x
		return Value
		
	def Mutual_Information(self, For = [], Known = []):
		H_x = self.Conditional_Entropy(For = [For[0]], Known = Known)
		H_y = self.Conditional_Entropy(For = [For[1]], Known = Known)
		H_xy = self.Conditional_Entropy(For = For, Known = Known)
		Value = H_x + H_y - H_xy
		return Value
		
	def Multiple_Mutual_Information(self, For = [], Known = []):
		Order = len(For) - 1
		Value = self._Recursive_Calculation(Order, For = For, Known = Known)
		return Value
		
	def _Recursive_Calculation(self, Order, For = [], Known = []):
		if Order == 2:
			return self.Mutual_Information(For = For[:-1], Known = Known) - self.Mutual_Information(For = For[:-1], Known = Known + [For[-1]])
		else:
			return self._Recursive_Calculation(Order-1, For = For[:-1], Known = Known) - self._Recursive_Calculation(Order-1, For = For[:-1], Known = Known + [For[-1]])
			
		
		
		
		
		

