# Simulation model for Autonomous Boolean Network(ABN) of the Gene Regulartory Network(GRN)
#
# This python script generates time-evolution data of information dynamical values from the ensemble by using the simple binning method
#
# The Main reference for the Figure-8 network of ABN : 
# M. Sun, X. Cheng, and J. E. S. Socolar, Causal structure of oscillations in gene regulatory networks: Boolean analysis of ordinary differential equation attractors, CHAOS 23, 025104 (2013)

import random

from on_Model.InfoDyn_lib import Model_Basics
from on_Model.InfoDyn_lib.Estimators import Simple_Binning

class ABN_Model(Model_Basics.Model_Basic):
	def __init__(self, n, m):
		super().__init__()
		
		self.Q = 2
		self.N_B = n
		self.N_C = m
		self.Total_Nodes = self.N_B + self.N_C + 1
		
		self.Simulation_Time_Limit = 40
		self.Size_of_Ensemble = 10000
		
		self.Save_Directory = "./on_Model/004_ABN_model_of_GRN/Temporal_Results/"
		
		self.Selected = []
		self.Initialize()		
		self.Generate_Data()
		
	def Register_Properties(self):
		self.Properties["Model_Name"] = "Figure-8 ABN for GRN"
		self.Properties["Estimator"] = "Simple Binning"
		self.Properties["Q"] = str(self.Q)
		self.Properties["N_B"] = str(self.N_B)
		self.Properties["N_C"] = str(self.N_C)
		self.Properties["Simulation_Time_Limit"] = str(self.Simulation_Time_Limit)
		self.Properties["Size_of_Ensemble"] = str(self.Size_of_Ensemble)
		
		self.Register_Topology()
			
	def Set_Topology(self):
		# Set Topology : Figure-8 network
		# Create labels of nodes : node A, B1, ..., Bn, C1, ..., Cm
		index_list = ["A"]
		for i in range(self.N_B):
			index_list.append("B%d"%(i+1))
		for i in range(self.N_C):
			index_list.append("C%d"%(i+1))
		self.Info_Network.Set_Nodes(index_list)
		
		# Set Links B_1 ~ B_2 ~ ... ~ B_n
		for i in range(self.N_B-1):
			self.Info_Network.Add_a_Link(("B%d"%(i+1),"B%d"%(i+2)))
		# Set Links C_1 ~ C_2 ~ ... ~ C_m
		for i in range(self.N_C-1):
			self.Info_Network.Add_a_Link(("C%d"%(i+1),"C%d"%(i+2)))
		# Set Link B_1 ~ A
		self.Info_Network.Add_a_Link(("B1","A"))
		# Set Link B_n ~ A
		self.Info_Network.Add_a_Link(("B%d"%(self.N_B),"A"))
		# Set Link C_1 ~ A
		self.Info_Network.Add_a_Link(("C1","A"))
		# Set Link C_m ~ A
		self.Info_Network.Add_a_Link(("C%d"%(self.N_C),"A"))
		
	def Init_State_Space(self):
		for k in self.Info_Network.Nodes:
			initial_value = random.randint(0,self.Q-1)
			self.State_Space[k] = initial_value	
			
	def Set_Estimator(self):
		self.Estimator = Simple_Binning.Estimator(self.Q, 4)
		self.Estimator.Source.Analysis = "Realtime"
		
	def Dynamics_of_States(self):
		# B_1(t') = A(t)
		self.Update_Buffer["B1"] = self.State_Space["A"]
		for i in range(self.N_B-1):
			# B_(i+2)(t') = B_(i+1)(t)
			self.Update_Buffer["B%d"%(i+2)] = self.State_Space["B%d"%(i+1)]
		# C_1(t') = A(t)
		self.Update_Buffer["C1"] = self.State_Space["A"]
		for i in range(self.N_C-1):
			# C_(i+2)(t') = C_(i+1)(t)
			self.Update_Buffer["C%d"%(i+2)] = self.State_Space["C%d"%(i+1)]
		# If B_n(t) = 1 and C_m(t) = 0
		if self.State_Space["B%d"%(self.N_B)] == 1 and self.State_Space["C%d"%(self.N_C)] == 0:
			# A(t') = 1
			self.Update_Buffer["A"] = 1
		else:
			# A(t') = 0
			self.Update_Buffer["A"] = 0
		
	def Plot_Data(self):
		pass
		
if __name__ == "__main__":
	TEST = ABN_Model(5,8)

