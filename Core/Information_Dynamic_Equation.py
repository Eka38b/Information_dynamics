
import math
import random

import numpy

from Core import Information_Network
from Core import Model_Basics

#not used.
from Core.Estimators import Several_Information_Variables
from Core.Estimators import Estimator_Basics

class Information_Dynamics(Model_Basics.Custom_FIFO):
	def __init__(self):
		
		self.Info_Network = Information_Network.A_Network()
		self.Blocked_Flows = []
		
		self.Simulation_Time_Limit = 80
		
		self.Properties = {}
		self.Save_Directory = ""
		
		self.Additional_InfoVar = [Several_Information_Variables.An_Additional_Information_Variable_BIN(0,4)] # Do nothing.
		self.Estimator = Estimator_Basics.Estimator() # Do nothing.
		
	def Initialize(self):
		self.Set_Topology()
		self.Set_Blocking_Flows_Condition()
		
		self.Register_Properties()
		self.Save_Properties()
		
		self.Create_File_Header()	
		
		self.Init_Overall_Vars_and_Alphas()

	def Generate_Data(self):
		self.Set_Initial_Conditions()		
		self.Set_Overall_Alphas_and_E()
		
		for t in range(self.Simulation_Time_Limit):
			self.Set_Realtime_Alphas_and_E()
			self.Impose_Blocking_Flows_Condition(t)
		
			for ind_link in self.Info_Network.Links:
				self.Simulation_Nodes = ind_link
				self.Estimator.Source.Type = "Pairwise"
				self.Save_Info_Vars(t+1)
				
				self.Info_Network.Links[self.Simulation_Nodes].Var_["MI"][t+1] = self.Updated_MI(t)
				self.Info_Network.Links[self.Simulation_Nodes].Var_["TE"+str(1)][t+1] = self.Updated_TE(t,1)
				self.Info_Network.Links[self.Simulation_Nodes].Var_["rTE"+str(1)][t+1] = self.Updated_rTE(t,1)
				self.Info_Network.Links[self.Simulation_Nodes].Var_["TE"+str(2)][t+1] = self.Updated_TE(t,2)
				self.Info_Network.Links[self.Simulation_Nodes].Var_["rTE"+str(2)][t+1] = self.Updated_rTE(t,2)
			
			for ind_node in self.Info_Network.Nodes:
				self.Simulation_Nodes = [ind_node] + self.Info_Network.Nodes[ind_node].Neighbors
				self.Estimator.Source.Type = "Point"
				self.Save_Info_Vars(t+1)
				
				self.Info_Network.Nodes[self.Simulation_Nodes[0]].Var_["H0"][t+1] = self.Updated_H0(t)
				
	def Updated_MI(self, Simulation_Time):
		MI_t0 = self.Info_Network.Links[self.Simulation_Nodes].Var_["MI"][Simulation_Time]
		TE1_t0 = self.Info_Network.Links[self.Simulation_Nodes].Var_["TE1"][Simulation_Time]
		rTE1_t0 = self.Info_Network.Links[self.Simulation_Nodes].Var_["rTE1"][Simulation_Time]
		TE2_t0 = self.Info_Network.Links[self.Simulation_Nodes].Var_["TE2"][Simulation_Time]
		rTE2_t0 = self.Info_Network.Links[self.Simulation_Nodes].Var_["rTE2"][Simulation_Time]
		Alpha_2 = self.Info_Network.Links[self.Simulation_Nodes].Alpha_["2"][Simulation_Time]
		
		MI_t1 = MI_t0 + (TE1_t0 - rTE1_t0) + (TE2_t0 - rTE2_t0) + Alpha_2
		return MI_t1
		
	def Updated_TE(self, Simulation_Time, Flow_Direction):
		TE_t0 = self.Info_Network.Links[self.Simulation_Nodes].Var_["TE"+str(Flow_Direction)][Simulation_Time]
		rTE_t0 = self.Info_Network.Links[self.Simulation_Nodes].Var_["rTE"+str(Flow_Direction)][Simulation_Time]
		
		node_index = self.Simulation_Nodes[(2 - Flow_Direction)]
		Flow_Sum = 0
		for neighbor in self.Info_Network.Nodes[node_index].Neighbors:
			if (node_index, neighbor) in self.Info_Network.Links:
				link_ind = (node_index, neighbor)
				direction = "1"
			else:
				link_ind = (neighbor, node_index)
				direction = "2"
			if link_ind != self.Simulation_Nodes:
				T = self.Info_Network.Links[link_ind].Var_["TE"+direction][Simulation_Time]
				rT = self.Info_Network.Links[link_ind].Var_["rTE"+direction][Simulation_Time]
				Flow_Sum += T - rT
			
		E = self.Info_Network.Nodes[node_index].Var_["E"][Simulation_Time]
		Alpha_1 = self.Info_Network.Nodes[node_index].Alpha_["1"][Simulation_Time]
		Alpha_2 = self.Info_Network.Links[self.Simulation_Nodes].Alpha_["2"][Simulation_Time]
		Alpha_3 = self.Info_Network.Links[self.Simulation_Nodes].Alpha_["3_"+str(Flow_Direction)][Simulation_Time]
		
		TE_t1 = TE_t0 + Flow_Sum - (TE_t0 - rTE_t0) - E + Alpha_1 - Alpha_2 - Alpha_3
		return TE_t1
		
	def Updated_rTE(self, Simulation_Time, Flow_Direction):
		TE_t0 = self.Info_Network.Links[self.Simulation_Nodes].Var_["TE"+str(Flow_Direction)][Simulation_Time]
		TE_t1 = self.Info_Network.Links[self.Simulation_Nodes].Var_["TE"+str(Flow_Direction)][Simulation_Time+1]
		rTE_t0 = self.Info_Network.Links[self.Simulation_Nodes].Var_["rTE"+str(Flow_Direction)][Simulation_Time]
		
		Alpha3456 = 0
		node_index = self.Simulation_Nodes[(Flow_Direction-1)]
		n = len(self.Info_Network.Nodes[node_index].Neighbors)
		if n == 1:
			print("Warning: 1 NEIGHBOR. Set their alphas properly.")
			Alpha_3 = self.Info_Network.Links[self.Simulation_Nodes].Alpha_["3_"+str(Flow_Direction)][Simulation_Time]
			Alpha_4 = self.Info_Network.Links[self.Simulation_Nodes].Alpha_["4_"+str(3-Flow_Direction)][Simulation_Time]
			Alpha_5 = self.Info_Network.Links[self.Simulation_Nodes].Alpha_["5"][Simulation_Time]
			Alpha_6 = self.Info_Network.Links[self.Simulation_Nodes].Alpha_["6_"+str(Flow_Direction)][Simulation_Time]
			Alpha3456 = - Alpha_3 - Alpha_4 + Alpha_5 + Alpha_6
			
		else:
			Flow_Sum = 0
			for neighbor in self.Info_Network.Nodes[node_index].Neighbors:
				if (node_index, neighbor) in self.Info_Network.Links:
					link_ind = (node_index, neighbor)
					direction = "2"
				else:
					link_ind = (neighbor, node_index)
					direction = "1"
				if link_ind != self.Simulation_Nodes:
					Delta_Alpha_2 = self.Info_Network.Links[link_ind].Alpha_["2"][Simulation_Time+1] - self.Info_Network.Links[link_ind].Alpha_["2"][Simulation_Time]
					Alpha_3 = self.Info_Network.Links[link_ind].Alpha_["3_"+direction][Simulation_Time]
					Alpha_6 = self.Info_Network.Links[link_ind].Alpha_["6_"+direction][Simulation_Time]
					Flow_Sum += Alpha_3 - Alpha_6 - Delta_Alpha_2

		
			Delta_Alpha_2 = self.Info_Network.Links[self.Simulation_Nodes].Alpha_["2"][Simulation_Time+1] - self.Info_Network.Links[self.Simulation_Nodes].Alpha_["2"][Simulation_Time]
			Alpha_3 = self.Info_Network.Links[self.Simulation_Nodes].Alpha_["3_"+str(3-Flow_Direction)][Simulation_Time]
			Alpha_6 = self.Info_Network.Links[self.Simulation_Nodes].Alpha_["6_"+str(3-Flow_Direction)][Simulation_Time]
			Delta_E = self.Info_Network.Nodes[node_index].Var_["E"][Simulation_Time+1] - self.Info_Network.Nodes[node_index].Var_["E"][Simulation_Time]
			Delta_Alpha_1 =	self.Info_Network.Nodes[node_index].Alpha_["1"][Simulation_Time+1] - self.Info_Network.Nodes[node_index].Alpha_["1"][Simulation_Time]	
			Alpha3456 += (n-2)/(n-1) * (Alpha_3 - Alpha_6 - Delta_Alpha_2)
			Alpha3456 -= 1/(n-1) * Flow_Sum	
			Alpha3456 += 1/(n-1) * (Delta_E - Delta_Alpha_1)	

		rTE_t1 = rTE_t0 + (TE_t1 - TE_t0) - Alpha3456
		
		return rTE_t1
		
	def Updated_H0(self, Simulation_Time):
		H0_t0 = self.Info_Network.Nodes[self.Simulation_Nodes[0]].Var_["H0"][Simulation_Time]
		
		node_index = self.Simulation_Nodes[0]
		Flow_Sum = 0
		for neighbor in self.Info_Network.Nodes[node_index].Neighbors:
			if (node_index, neighbor) in self.Info_Network.Links:
				link_ind = (node_index, neighbor)
				direction = "1"
			else:
				link_ind = (neighbor, node_index)
				direction = "2"
			if link_ind != self.Simulation_Nodes:
				T = self.Info_Network.Links[link_ind].Var_["TE"+direction][Simulation_Time]
				rT = self.Info_Network.Links[link_ind].Var_["rTE"+direction][Simulation_Time]
				Flow_Sum += T - rT
			
		E = self.Info_Network.Nodes[node_index].Var_["E"][Simulation_Time]
		Alpha_1 = self.Info_Network.Nodes[node_index].Alpha_["1"][Simulation_Time]

		H0_t1 = H0_t0 + Flow_Sum - E + Alpha_1
		return H0_t1
	
	def Init_Overall_Vars_and_Alphas(self):
		for t in range(self.Simulation_Time_Limit+1):
			for ind_link in self.Info_Network.Links:
				for Key in self.Info_Network.Links[ind_link].Var_:
					self.Info_Network.Links[ind_link].Var_[Key].append(0)
				for Key in self.Info_Network.Links[ind_link].Alpha_:
					self.Info_Network.Links[ind_link].Alpha_[Key].append(0)
			for ind_node in self.Info_Network.Nodes:
				for Key in self.Info_Network.Nodes[ind_node].Var_:
					self.Info_Network.Nodes[ind_node].Var_[Key].append(0)
				for Key in self.Info_Network.Nodes[ind_node].Alpha_:
					self.Info_Network.Nodes[ind_node].Alpha_[Key].append(0)
		
	def Impose_Blocking_Flows_Condition(self, Simulation_Time):
		# Block T-flows
		for the_blocked in self.Blocked_Flows:
			if the_blocked in self.Info_Network.Links:
				link_ind = the_blocked
				direction = "2"
			else:
				link_ind = (the_blocked[1], the_blocked[0])
				direction = "1"
				
			self.Simulation_Nodes = link_ind
			self.Info_Network.Links[link_ind].Alpha_["3_"+direction][Simulation_Time] = 0
			self.Info_Network.Links[link_ind].Alpha_["3_"+direction][Simulation_Time] = self.Updated_TE(Simulation_Time,int(direction))

		# Block rT-flows
		self.blocked_rTE = []
		for the_blocked in self.Blocked_Flows:
			if the_blocked in self.Info_Network.Links:
				link_ind = the_blocked
				direction = "1"
			else:
				link_ind = (the_blocked[1], the_blocked[0])
				direction = "2"
			self.Simulation_Nodes = link_ind
			self.blocked_rTE.append((link_ind,direction))
			
		for node_index in self.Info_Network.Nodes:
			Candidates = []
			for neighbor in self.Info_Network.Nodes[node_index].Neighbors:
				if (node_index, neighbor) in self.Info_Network.Links:
					link_ind = (node_index, neighbor)
					direction_2 = "1"
				else:
					link_ind = (neighbor, node_index)
					direction_2 = "2"
				if (link_ind, direction_2) in self.blocked_rTE:
					Candidates.append((link_ind, direction_2))
			n = len(Candidates)

			if n > 1:
				for j in range(1,n):
					res = self.Info_Network.Links[Candidates[j][0]].Alpha_["3_"+str(3-int(Candidates[j][1]))][Simulation_Time]
					res -= self.Info_Network.Links[Candidates[j][0]].Alpha_["2"][Simulation_Time+1] - self.Info_Network.Links[Candidates[j][0]].Alpha_["2"][Simulation_Time]
	
					Delta_Alpha_2 = self.Info_Network.Links[Candidates[0][0]].Alpha_["2"][Simulation_Time+1] - self.Info_Network.Links[Candidates[0][0]].Alpha_["2"][Simulation_Time]
					Alpha_3 = self.Info_Network.Links[Candidates[0][0]].Alpha_["3_"+str(3-int(Candidates[0][1]))][Simulation_Time]
					Alpha_6 = self.Info_Network.Links[Candidates[0][0]].Alpha_["6_"+str(3-int(Candidates[0][1]))][Simulation_Time]
					res -= Alpha_3 - Alpha_6 - Delta_Alpha_2
					
					TE_t0 = self.Info_Network.Links[Candidates[j][0]].Var_["TE"+Candidates[j][1]][Simulation_Time]
					self.Simulation_Nodes = Candidates[j][0]
					TE_t1 = self.Updated_TE(Simulation_Time,int(Candidates[j][1]))
					res -= TE_t1 -TE_t0
					
					TE0_t0 = self.Info_Network.Links[Candidates[0][0]].Var_["TE"+Candidates[0][1]][Simulation_Time]
					self.Simulation_Nodes = Candidates[0][0]
					TE0_t1 = self.Updated_TE(Simulation_Time,int(Candidates[0][1]))
					res += TE0_t1 -TE0_t0
					
					self.Info_Network.Links[Candidates[j][0]].Alpha_["6_"+str(3-int(Candidates[j][1]))][Simulation_Time] = res
					
		for the_blocked in self.Blocked_Flows:
			if the_blocked in self.Info_Network.Links:
				link_ind = the_blocked
				direction = "1"
			else:
				link_ind = (the_blocked[1], the_blocked[0])
				direction = "2"
				
			self.Simulation_Nodes = link_ind
			self.Info_Network.Links[self.Simulation_Nodes].Var_["TE"+direction][Simulation_Time+1] = self.Updated_TE(Simulation_Time,int(direction))
			
			TE_t0 = self.Info_Network.Links[self.Simulation_Nodes].Var_["TE"+direction][Simulation_Time]
			TE_t1 = self.Info_Network.Links[self.Simulation_Nodes].Var_["TE"+direction][Simulation_Time+1]
			
			Alpha3456 = 0
			node_index = self.Simulation_Nodes[(int(direction)-1)]
			Flow_Sum = 0
			Candidates = []
			for neighbor in self.Info_Network.Nodes[node_index].Neighbors:
				if (node_index, neighbor) in self.Info_Network.Links:
					link_ind = (node_index, neighbor)
					direction_2 = "2"
				else:
					link_ind = (neighbor, node_index)
					direction_2 = "1"
				if link_ind != self.Simulation_Nodes:
					Delta_Alpha_2 = self.Info_Network.Links[link_ind].Alpha_["2"][Simulation_Time+1] - self.Info_Network.Links[link_ind].Alpha_["2"][Simulation_Time]
					Alpha_3 = self.Info_Network.Links[link_ind].Alpha_["3_"+direction_2][Simulation_Time]
					Alpha_6 = self.Info_Network.Links[link_ind].Alpha_["6_"+direction_2][Simulation_Time]
					Flow_Sum += Alpha_3 - Alpha_6 - Delta_Alpha_2
					if (link_ind,direction_2) in self.blocked_rTE:
						Candidates.append((link_ind,direction_2))
			n = len(self.Info_Network.Nodes[node_index].Neighbors)
			if n == 1:
				print("ERROR in Blocking: 1 NEIGHBOR. THIS IS AN END POINT.")
				return
			Delta_Alpha_2 = self.Info_Network.Links[self.Simulation_Nodes].Alpha_["2"][Simulation_Time+1] - self.Info_Network.Links[self.Simulation_Nodes].Alpha_["2"][Simulation_Time]
			Alpha_3 = self.Info_Network.Links[self.Simulation_Nodes].Alpha_["3_"+str(3-int(direction))][Simulation_Time]
			Alpha_6 = self.Info_Network.Links[self.Simulation_Nodes].Alpha_["6_"+str(3-int(direction))][Simulation_Time]
			Delta_E = self.Info_Network.Nodes[node_index].Var_["E"][Simulation_Time+1] - self.Info_Network.Nodes[node_index].Var_["E"][Simulation_Time]
			Delta_Alpha_1 =	self.Info_Network.Nodes[node_index].Alpha_["1"][Simulation_Time+1] - self.Info_Network.Nodes[node_index].Alpha_["1"][Simulation_Time]	
			Alpha3456 += (n-2)/(n-1) * (Alpha_3 - Alpha_6 - Delta_Alpha_2)
			Alpha3456 -= 1/(n-1) * Flow_Sum	
			Alpha3456 += 1/(n-1) * (Delta_E - Delta_Alpha_1)
		
			self.Info_Network.Links[Candidates[0][0]].Alpha_["6_"+Candidates[0][1]][Simulation_Time] += (n-1)*((TE_t1 - TE_t0) - Alpha3456)
				
	def Set_Topology(self):
		raise NotImplementedError("Need to override this function")
		
	def Set_Blocking_Flows_Condition(self):
		raise NotImplementedError("Need to override this function")	
		
	def Set_Initial_Conditions(self):
		raise NotImplementedError("Need to override this function")
		
	def Set_Overall_Alphas_and_E(self):
		raise NotImplementedError("Need to override this function")
		
	def Set_Realtime_Alphas_and_E(self):	
		pass	