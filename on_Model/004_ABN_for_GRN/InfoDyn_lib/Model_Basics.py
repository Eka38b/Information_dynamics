
import random
import time

from InfoDyn_lib import Information_Network
from InfoDyn_lib import Several_Information_Variables

class Custom_FIFO():
	def __init__(self):
		self.Properties = {}
		self.Simulation_Link = ""	
		self.Info_Network = ""
		self.InfoVar_of_Interest = ""
		self.Save_Directory = ""
		
	def Register_Properties(self):
		pass
		
	def Register_Topology(self):
		self.Properties["Nodes"] = ""
		self.Properties["Links"] = ""
		for ind_node in self.Info_Network.Nodes:
			self.Properties["Nodes"] = self.Properties["Nodes"] + ind_node + "|"
		for ind_link in self.Info_Network.Links:
			self.Properties["Links"] = self.Properties["Links"] + "%s,%s|"%(ind_link) + " "
			
	def Save_Properties(self):
		Save_File = open(self.Save_Directory+"Simulation_Properties.txt",'w')
		for key in self.Properties:
			Save_File.write(key + " : " + self.Properties[key] + "\n")
		Save_File.close()
		
	def Create_File_Header(self):
		for ind_node in self.Info_Network.Nodes:
			Save_File = open(self.Save_Directory+"Node_%s.txt"%ind_node,'w')
			Save_File.close()
		for ind_link in self.Info_Network.Links:
			Save_File = open(self.Save_Directory+"Link_%s_%s.txt"%ind_link,'w')
			Save_File.close()
		
		
	def Save_Info_Vars(self, Simulation_Time):
		a_node = self.Info_Network.Nodes[self.Simulation_Link[0]]
		Save_File = open(self.Save_Directory+"Node_%s.txt"%self.Simulation_Link[0],'a')
		Save_File.write("%03d:%0.3f|%0.3f|\n"%(Simulation_Time,a_node.Var_["H0"],a_node.Alpha_["partial1"]))
		Save_File.close()
		
		a_node = self.Info_Network.Nodes[self.Simulation_Link[1]]
		Save_File = open(self.Save_Directory+"Node_%s.txt"%self.Simulation_Link[1],'a')
		Save_File.write("%03d:%0.3f|%0.3f|\n"%(Simulation_Time,a_node.Var_["H0"],a_node.Alpha_["partial1"]))
		Save_File.close()
		
		Save_File = open(self.Save_Directory+"Link_%s_%s.txt"%self.Simulation_Link,'a')
		Save_File.write("%03d:"%Simulation_Time)
		for key in self.Info_Network.Links[self.Simulation_Link].Var_:
			value = self.Info_Network.Links[self.Simulation_Link].Var_[key]
			if value >= 0:
				Save_File.write("+%0.3f|"%value)
			else:
				Save_File.write("%0.3f|"%value)
		for key in self.Info_Network.Links[self.Simulation_Link].Alpha_:
			value = self.Info_Network.Links[self.Simulation_Link].Alpha_[key]
			if value >= 0:
				Save_File.write("+%0.3f|"%value)
			else:
				Save_File.write("%0.3f|"%value)
		Save_File.write("\n")
		Save_File.close()
		
		self.InfoVar_of_Interest.Save_the_Variable(self.Save_Directory, Simulation_Time)
		

class Model_Basic(Custom_FIFO):
	def __init__(self):
		self.Q = 0
		self.Total_Nodes = 0
		
		self.Simulation_Time_Limit = 0
		self.Simulation_Cut_up = -1
		self.Simulation_Cut_down = 0
		
		self.Properties = {}
		
		self.State_Space = {}
		self.Update_Buffer = {}
		self.Simulation_Link = ()		
		self.Statistics = {}
			
		self.Info_Network = Information_Network.A_Network()
		self.InfoVar_of_Interest = Several_Information_Variables.An_Information_Variable() # Do nothing.

		self.Save_Directory = ""
		
	def Initialize(self):
		self.Set_Topology()
		self.Init_Space()
		
		self.Register_Properties()
		self.Save_Properties()
		
	def Init_Space(self):
		for k in self.Info_Network.Nodes:
			self.State_Space[k] = 0
			self.Update_Buffer[k] = 0
			
	def Set_Topology(self):
		pass
				
	def Init_State_Space(self):
		random.seed(time.time())
		for k in self.Info_Network.Nodes:
			initial_value = random.randint(0,self.Q-1)
			self.State_Space[k] = initial_value		
	
	def Init_Statistics(self):
		for i in range(self.Q):
			for j in range(self.Q):
				for k in range(self.Q):
					for l in range(self.Q):
						self.Statistics[(i,j,k,l)] = 0
		self.InfoVar_of_Interest.Initialize_Statistics(self.Q)
			
	def Generate_Data(self):
		if self.Simulation_Cut_up == -1 :
			self.Simulation_Cut_up = self.Simulation_Time_Limit
		if len(self.Selected)==0:
			for ind_link in self.Info_Network.Links:
				self.Selected.append(ind_link)
				
		self.Create_File_Header()
		for ind_link in self.Selected:
			self.Simulation_Link = ind_link
			for t in range(self.Simulation_Time_Limit):
				if t >= self.Simulation_Cut_down and t < self.Simulation_Cut_up:
					self.Make_Ensemble(t+1)
			print("\tComplete simulations for the link %s ~ %s"%self.Simulation_Link)
				
	def Make_Ensemble(self, Simulation_Time):
		self.Init_Statistics()
		for c in range(self.Size_of_Ensemble):
			self.Init_State_Space()
			self.Simulate_Model(Simulation_Time)
		self.Calculate_Info_Vars()
		self.Save_Info_Vars(Simulation_Time)
		
	def Simulate_Model(self, Simulation_Time):
		for t in range(Simulation_Time):
			self.Dynamics_of_States()
			if t == Simulation_Time-1:
				self.Update_Statistics()
			self.Update_States()

	def Calculate_Info_Vars(self):
		self.Info_Network.Nodes[self.Simulation_Link[0]].Calculate(self.Statistics, 0)
		self.Info_Network.Nodes[self.Simulation_Link[1]].Calculate(self.Statistics, 1)
		self.Info_Network.Links[self.Simulation_Link].Calculate(self.Statistics)
		self.InfoVar_of_Interest.Estimate_the_Variable()

	def Update_Statistics(self):
		self.Statistics[(self.State_Space[self.Simulation_Link[0]],self.State_Space[self.Simulation_Link[1]],self.Update_Buffer[self.Simulation_Link[0]],self.Update_Buffer[self.Simulation_Link[1]])] += 1
		self.InfoVar_of_Interest.Update_Statistics(self.State_Space,self.Update_Buffer)
		
	def Update_States(self):
		for k in self.Info_Network.Nodes:

			self.State_Space[k] = self.Update_Buffer[k]
