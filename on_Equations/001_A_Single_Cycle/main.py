
import math
import random

import numpy

from Core import Information_Network
from Core import Model_Basics
from Core import Information_Dynamic_Equation

class ID_of_Single_Ring(Information_Dynamic_Equation.Information_Dynamics):
	def __init__(self, m):
		super().__init__()
		
		self.N = m
		
		self.Simulation_Time_Limit = 100
		
		self.Save_Directory = "./on_Equations/001_A_Single_Cycle/Temporal_Results/"
		
		self.Initialize()
		self.Generate_Data()
		
	def Register_Properties(self):
		self.Properties["N"] = str(self.N)
		self.Properties["Simulation_Time_Limit"] = str(self.Simulation_Time_Limit)
		self.Properties["Blocked_Flows"] = str(self.Blocked_Flows)
		
		self.Register_Topology()
		
	def Set_Topology(self):
		index_list = []
		for i in range(self.N):
			index_list.append("A%d"%(i+1))
		self.Info_Network.Set_Nodes(index_list)
		
		for i in range(self.N):
			self.Info_Network.Add_a_Link(("A%d"%(i+1),"A%d"%((i+1)%self.N+1)))
		
			
	def Set_Blocking_Flows_Condition(self):
		for i in range(self.N):
			self.Blocked_Flows.append(("A"+str((i+1)%self.N+1),"A"+str(i+1)))
			
	def Set_Initial_Conditions(self):
		for ind_link in self.Info_Network.Links:
			if ind_link in [("A1","A2")]:
				self.Info_Network.Links[ind_link].Var_["MI"][0] = 0.6
				self.Info_Network.Links[ind_link].Var_["TE1"][0] = 0
				self.Info_Network.Links[ind_link].Var_["rTE1"][0] = 0.5
				self.Info_Network.Links[ind_link].Var_["TE2"][0] = 0.5
				self.Info_Network.Links[ind_link].Var_["rTE2"][0] = 0
			else:
				self.Info_Network.Links[ind_link].Var_["MI"][0] = 0.6
				self.Info_Network.Links[ind_link].Var_["TE1"][0] = 0
				self.Info_Network.Links[ind_link].Var_["rTE1"][0] = 0.2
				self.Info_Network.Links[ind_link].Var_["TE2"][0] = 0.2
				self.Info_Network.Links[ind_link].Var_["rTE2"][0] = 0
				
		for ind_node in self.Info_Network.Nodes:
			self.Info_Network.Nodes[ind_node].Var_["H0"][0] = 0.6
		
	def Set_Overall_Alphas_and_E(self):
		for t in range(self.Simulation_Time_Limit):
			for ind_link in self.Info_Network.Links:
				self.Info_Network.Links[ind_link].Alpha_["2"][0] = 0
				self.Info_Network.Links[ind_link].Alpha_["3_1"][0] = 0
				self.Info_Network.Links[ind_link].Alpha_["3_2"][0] = 0
				self.Info_Network.Links[ind_link].Alpha_["6_1"][0] = 0
				self.Info_Network.Links[ind_link].Alpha_["6_2"][0] = 0
			for ind_node in self.Info_Network.Nodes:
				self.Info_Network.Nodes[ind_node].Alpha_["1"][0] = 0
				self.Info_Network.Nodes[ind_node].Var_["E"][0] = 0
		
if __name__ == "__main__":
				
	TEST = ID_of_Single_Ring(8)