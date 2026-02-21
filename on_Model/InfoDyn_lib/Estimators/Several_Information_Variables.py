
from on_Model.InfoDyn_lib.Estimators import Estimator_Basics 
from on_Model.InfoDyn_lib.Estimators import Simple_Binning
#from InfoDyn_lib.Estimators import KSG

class An_Additional_Information_Variable_BIN(Simple_Binning.Estimator):
	def __init__(self, Q, Dimension):
		super().__init__(Q, Dimension)
		self.Source.Analysis = ""
		
		self.Name = ""
		self.Value = {}
		
	def Estimate_the_Variable(self):
		pass
		
	def Save_the_Variable(self, Save_Directory, Simulation_Time):
		if self.Source.Analysis != "Realtime":
			return
		save_file = open(Save_Directory + self.Name + ".txt",'a')
		save_file.write("%03d: "%(Simulation_Time))
		for val in self.Value:
			save_file.write("%0.3f|"%(self.Value[val]))
		save_file.write("\n")
		save_file.close()

class H_XYZ(An_Additional_Information_Variable_BIN):
	def __init__(self, Q, Index_Tuple):
		super().__init__(Q, 3)
		self.Analysis = "Realtime"
		self.Source.Type = "not_Pairwise"
		
		self.Name = "H_%s%s%s"%Index_Tuple
		self.Source.Variable_Names = Index_Tuple
		
	def Estimate_the_Variable(self):	
		self.Value["H"] = self.Conditional_Entropy(For = self.Source.Variable_Names)
		return
		
		
class H_XYZW(An_Additional_Information_Variable_BIN):
	def __init__(self, Q, Index_Tuple):
		super().__init__(Q, 4)
		self.Analysis = "Realtime"
		self.Source.Type = "not_Pairwise"
		
		self.Name = "H_%s%s%s%s"%Index_Tuple
		self.Source.Variable_Names = Index_Tuple
		
	def Estimate_the_Variable(self):	
		self.Value["H"] = self.Conditional_Entropy(For = self.Source.Variable_Names)
		return
		
class T2(An_Additional_Information_Variable_BIN):
	def __init__(self, Q, Index_Tuple): # Index_Tuple = (X, Y, Ext)
		super().__init__(Q, 5)
		self.Analysis = "Realtime"
		self.Source.Type = "not_Pairwise"
		
		self.Name = "Multiple_Transfer_Entropy_%s_%s_%s"%Index_Tuple
		self.Source.Variable_Names = list(Index_Tuple) + [Index_Tuple[0]+"'"] + [Index_Tuple[1]+"'"]
		
	def Estimate_the_Variable(self):	
		X_t1 = self.Source.Variable_Names[0]
		Y_t1 = self.Source.Variable_Names[1]
		Ext_t1 = self.Source.Variable_Names[2]
		X_t2 = self.Source.Variable_Names[3]
		Y_t2 = self.Source.Variable_Names[4]
		# T^2_{%s %s -> %s}
		self.Value["T^2_v1"] = self.Multiple_Mutual_Information(For = [Ext_t1,X_t1,Y_t2],  Known = [Y_t1])
		self.Value["T^2_v2"] = self.Multiple_Mutual_Information(For = [Ext_t1,X_t2,Y_t2],  Known = [X_t1,Y_t1])
		self.Value["T^2_v3"] = self.Multiple_Mutual_Information(For = [Ext_t1,Y_t1,X_t2],  Known = [X_t1])
		return
		
		