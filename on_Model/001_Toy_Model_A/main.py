
import random

from Core import Model_Basics
from Core.Estimators import Simple_Binning

class Toy_Model_A(Model_Basics.Model_Basic):
	def __init__(self, n, a, b, c):
		super().__init__()
		
		self.Q = 5
		self.N = n
		self.coeff_in = a
		self.coeff_ext = b
		self.internal_noise = c
		self.Total_Nodes = self.N + 1
		
		self.Simulation_Time_Limit = 40
		self.Start_of_Interaction = 25
		self.Size_of_Ensemble = 10000
		
		self.Save_Directory = "./Data/on_Model001/"
		
		self.Selected_Nodes = ["A1","A%d"%self.N]
		self.Selected_Links = []
		
		self.Initialize()		
		self.Generate_Data()
		
	def Register_Properties(self):
		self.Properties["Model_Name"] = "Cycle_and_Source_on_Toy_Model_A"
		self.Properties["Estimator"] = "Simple Binning"
		self.Properties["Q"] = str(self.Q)
		self.Properties["N"] = str(self.N)
		self.Properties["Simulation_Time_Limit"] = str(self.Simulation_Time_Limit)
		self.Properties["Size_of_Ensemble"] = str(self.Size_of_Ensemble)
		
		self.Register_Topology()
			
	def Set_Topology(self):
		index_list = ["Ext"]
		for i in range(self.N):
			index_list.append("A%d"%(i+1))
		self.Info_Network.Set_Nodes(index_list)
		
		self.Info_Network.Add_a_Link(("Ext","A1"))
		for i in range(self.N):
			self.Info_Network.Add_a_Link(("A%d"%(i+1),"A%d"%((i+1)%self.N+1)))
		
	def Init_State_Space(self):
		for k in self.Info_Network.Nodes:
			initial_value = random.randint(0,self.Q-1)
			self.State_Space[k] = initial_value	
			
	def Set_Estimator(self):
		self.Estimator = Simple_Binning.Estimator(self.Q, 4)
		self.Estimator.Source.Analysis = "Realtime"
		
	def Dynamics_of_States(self, t):
		if t < self.Start_of_Interaction:
			self.Update_Buffer["Ext"] = random.randint(0,self.Q-1)
			for i in range(self.N-1):
				self.Update_Buffer["A%d"%(i+2)] = int(self.State_Space["A%d"%(i+2)] + self.coeff_in * (self.State_Space["A%d"%(i+1)]- self.State_Space["A%d"%(i+2)]) + self.internal_noise * random.randint(0,self.Q-1))%self.Q
			self.Update_Buffer["A1"] = int(self.State_Space["A1"] + self.coeff_in * (self.State_Space["A%d"%self.N]- self.State_Space["A1"]) + self.internal_noise * random.randint(0,self.Q-1))%self.Q
		
		else:
			self.Update_Buffer["Ext"] = random.randint(0,self.Q-1)
			for i in range(self.N-1):
				self.Update_Buffer["A%d"%(i+2)] = int(self.State_Space["A%d"%(i+2)] + self.coeff_in * (self.State_Space["A%d"%(i+1)]- self.State_Space["A%d"%(i+2)]) + self.internal_noise * random.randint(0,self.Q-1))%self.Q
			self.Update_Buffer["A1"] = int(self.State_Space["A1"] + self.coeff_in * (self.State_Space["A%d"%self.N]- self.State_Space["A1"]) + self.coeff_ext * (self.State_Space["Ext"]- self.State_Space["A1"]) + self.internal_noise * random.randint(0,self.Q-1))%self.Q
		
		
if __name__ == "__main__":
	TEST = Toy_Model_A(5, 0.7, 0.5, 0.4)
