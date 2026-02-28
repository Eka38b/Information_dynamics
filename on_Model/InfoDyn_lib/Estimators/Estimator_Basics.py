

# Empirical Data for Estimation : Histogram or Ensemble Data
class Source():
	def __init__(self):
		self.Analysis = ""
		self.Type = ""
		self.Variable_Names = []
		
	def Init_Source_Realtime(self, Simulation_Nodes):
		pass
		
	def Update_Source_Realtime(self, State_Space, Update_Buffer):
		pass
		
	def Init_Source_Post_Analysis(self, Nodes, Ensemble_Data_File):
		pass

class Estimator():
	def __init__(self):
		self.Name = ""
		self.Source = ""
		
	def Entropy(self, For = []):
		raise NotImplementedError("Need to override this function")
		
	def Conditional_Entropy(self, For = [], Known = []):
		raise NotImplementedError("Need to override this function")
		
	def Mutual_Information(self, For = [], Known = []):
		raise NotImplementedError("Need to override this function")
		
	def Multiple_Mutual_Information(self, For = [], Known = []):
		pass
