"""
Model_Basics.py

Core simulation framework for ensemble-based information dynamics.

Main Responsibilities
---------------------
- Manage network topology
- Construct ensemble realizations
- Control time evolution
- Support two modes:
    (1) Realtime estimation
    (2) Post-analysis estimation

Workflow
--------
1. Initialize topology
2. Construct ensemble of trajectories
3. Update states over time
4. Compute information measures via selected estimator
5. Save temporal results

Outputs
-------
- Time-resolved entropy and information variables
- Optional ensemble snapshots for post-analysis

Design Philosophy
-----------------
Separates:
- Simulation logic
- Estimation logic
- Network representation

Notes
-----
- Realtime mode recomputes ensemble slices per time step.
- Post-analysis mode stores ensemble trajectories to disk.
- Large ensembles may require memory optimization.

Limitations
-----------
- Current implementation assumes synchronous discrete-time updates.
"""
import random
import time

from on_Model.InfoDyn_lib import Information_Network
from on_Model.InfoDyn_lib.Estimators import Simple_Binning, KSG

from on_Model.InfoDyn_lib.Estimators import Several_Information_Variables

class Custom_FIFO():
	def __init__(self):
		self.Properties = {}
		self.Simulation_Nodes = ""	
		self.Info_Network = ""
		self.Additional_InfoVar = ""
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
		a_node = self.Info_Network.Nodes[self.Simulation_Nodes[0]]
		Save_File = open(self.Save_Directory+"Node_%s.txt"%self.Simulation_Nodes[0],'a')
		Save_File.write("%03d:%0.3f|%0.3f|\n"%(Simulation_Time,a_node.Var_["H0"],a_node.Alpha_["partial1"]))
		Save_File.close()
		
		a_node = self.Info_Network.Nodes[self.Simulation_Nodes[1]]
		Save_File = open(self.Save_Directory+"Node_%s.txt"%self.Simulation_Nodes[1],'a')
		Save_File.write("%03d:%0.3f|%0.3f|\n"%(Simulation_Time,a_node.Var_["H0"],a_node.Alpha_["partial1"]))
		Save_File.close()
		
		Save_File = open(self.Save_Directory+"Link_%s_%s.txt"%self.Simulation_Nodes,'a')
		Save_File.write("%03d:"%Simulation_Time)
		for key in self.Info_Network.Links[self.Simulation_Nodes].Var_:
			value = self.Info_Network.Links[self.Simulation_Nodes].Var_[key]
			if value >= 0:
				Save_File.write("+%0.3f|"%value)
			else:
				Save_File.write("%0.3f|"%value)
		for key in self.Info_Network.Links[self.Simulation_Nodes].Alpha_:
			value = self.Info_Network.Links[self.Simulation_Nodes].Alpha_[key]
			if value >= 0:
				Save_File.write("+%0.3f|"%value)
			else:
				Save_File.write("%0.3f|"%value)
		Save_File.write("\n")
		Save_File.close()
		
		self.Additional_InfoVar.Save_the_Variable(self.Save_Directory, Simulation_Time)
		

class Model_Basic(Custom_FIFO):
	def __init__(self):
		self.Q = 0
		self.Total_Nodes = 0
		
		self.Simulation_Time_Limit = 0
		self.Simulation_Cut_up = -1
		self.Simulation_Cut_down = 0
		self.Save_Interval = 1
		
		self.Properties = {}
		
		self.State_Space = {}
		self.Update_Buffer = {}
		self.Simulation_Nodes = ()		
		
		self.Estimator = ""
			
		self.Info_Network = Information_Network.A_Network()
		self.Additional_InfoVar = Several_Information_Variables.An_Additional_Information_Variable_BIN(0,4) # Do nothing.

		self.Save_Directory = ""
		self.Ensemble_Directory = ""
		
		self.Selected = []
		
	def Initialize(self):
		self.Set_Topology()	
		self.Init_Space()
		self.Set_Estimator()

		self.Register_Properties()
		self.Save_Properties()
		
		self.Create_File_Header()	
		
	def Init_Space(self):
		for k in self.Info_Network.Nodes:
			self.State_Space[k] = 0
			self.Update_Buffer[k] = 0
		
		random.seed(time.time())	
		
		if len(self.Selected)==0:
			for ind_link in self.Info_Network.Links:
				self.Selected.append(ind_link)
			
	def Generate_Data(self):
		if self.Simulation_Cut_up == -1 :
			self.Simulation_Cut_up = self.Simulation_Time_Limit		
			
		if self.Estimator.Source.Analysis == "Realtime":
			for ind_tuple in self.Selected:
				self.Simulation_Nodes = ind_tuple
				for t in range(self.Simulation_Time_Limit):
					if t >= self.Simulation_Cut_down and t < self.Simulation_Cut_up:
						self.Construct_Ensemble(t+1)
				print("\tComplete simulations for the link %s ~ %s"%self.Simulation_Nodes)
				
		elif self.Estimator.Source.Analysis == "Post_Analysis":
			self.Construct_Ensemble(self.Simulation_Time_Limit)
				
	def Construct_Ensemble(self, Simulation_Time):
		self.Estimator.Source.Init_Source_Realtime(self.Simulation_Nodes)
		self.Additional_InfoVar.Source.Init_Source_Realtime(self.Simulation_Nodes)
		for c in range(self.Size_of_Ensemble):
			self.Init_State_Space()
			self.Simulate_Model(Simulation_Time)
			
		if self.Estimator.Source.Analysis == "Realtime":		
			self.Calculate_Info_Vars()
			self.Save_Info_Vars(Simulation_Time)
			
	def Simulate_Model(self, Simulation_Time):
		Previous_States = {}
		for t in range(Simulation_Time):
			self.Dynamics_of_States()
			if t == Simulation_Time-1:
				self.Estimator.Source.Update_Source_Realtime(self.State_Space,self.Update_Buffer)
				self.Additional_InfoVar.Source.Update_Source_Realtime(self.State_Space,self.Update_Buffer)
				
			if self.Estimator.Source.Analysis == "Post_Analysis" and t%self.Save_Interval == 0:
				if t != 0:
					self.Save_States(t, Previous_States)
				for k in self.Info_Network.Nodes:
					Previous_States[k] = self.State_Space[k]
				
			self.Update_States()
			
	def Calculate_Info_Vars(self):
		self.Info_Network.Nodes[self.Simulation_Nodes[0]].Calculate(self.Estimator)
		self.Info_Network.Nodes[self.Simulation_Nodes[1]].Calculate(self.Estimator)
		self.Info_Network.Links[self.Simulation_Nodes].Calculate(self.Estimator)
		self.Additional_InfoVar.Estimate_the_Variable()

	def Update_States(self):
		for k in self.Info_Network.Nodes:
			self.State_Space[k] = self.Update_Buffer[k]
			
	def Save_States(self, Simulation_Time, Previous_States):
		Data = ""
		for k in self.Info_Network.Nodes:
			Data = Data + "%0.4f|"%Previous_States[k]		
			Data = Data + "%0.4f|"%self.State_Space[k]
		Data = Data[:-1] + "\n"
		
		Save_File = open(self.Ensemble_Directory+"at_time%03d.txt"%Simulation_Time,'a')
		Save_File.write(Data)
		Save_File.close()
		
	def Post_Analysis(self):
		for ind_tuple in self.Selected:
			self.Simulation_Nodes = ind_tuple
			for t in range(int(self.Simulation_Time_Limit/self.Save_Interval)):
				if t != 0:
					ensemble_data = self.Ensemble_Directory+"at_time%03d.txt"%(t*self.Save_Interval)
					self.Estimator.Source.Init_Source_Post_Analysis(self.Info_Network.Nodes, ensemble_data)
					self.Calculate_Info_Vars()
					self.Save_Info_Vars(t*self.Save_Interval)
				
	def Set_Topology(self):
		raise NotImplementedError("Need to override this function")
		
	def Init_State_Space(self):
		raise NotImplementedError("Need to override this function")
				
	def Set_Estimator(self):
		raise NotImplementedError("Need to override this function")
				
	def Dynamics_of_States(self):
		raise NotImplementedError("Need to override this function")

	
