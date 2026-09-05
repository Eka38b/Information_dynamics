
import time
import random
import numpy

import os
import matplotlib.pyplot as plt

from Core import Model_Basics
from Core.Estimators import Simple_Binning

class Fredkin_Switch_Gate(Model_Basics.Model_Basic):
	def __init__(self, n=3, theta=0.1):			# 0 <= theta < 0.25
		super().__init__()
		
		self.Q = 4
		self.N = n
		
		self.theta = theta
		self.Probability_Mass = numpy.array([0.25, 0.25+self.theta, 0.25-self.theta, 0.25])
		self.Cumulative_Mass = numpy.cumsum(self.Probability_Mass)
		numpy.random.seed(int(time.time()))
		
		self.Simulation_Time_Limit = 40
		self.Start_of_Interaction = 25
		self.Size_of_Ensemble = 10000
		
		
		self.Save_Directory = "./on_Model/019_Fredkin_Switch_Gate/Temporal_Results/"
		
		self.Selected_Nodes = ["p"]
		self.Selected_Links = [("A%d"%self.N,"p"), ("Ext","p"),("p","A1")]
		
		
	def Register_Properties(self):
		self.Properties["Model_Name"] = "Fredkin_Switch_Gate"
		self.Properties["Estimator"] = "Simple Binning"
		self.Properties["Q"] = str(self.Q)
		self.Properties["N"] = str(self.N)
		self.Properties["theta"] = str(self.theta)
		self.Properties["Simulation_Time_Limit"] = str(self.Simulation_Time_Limit)
		self.Properties["Start_of_Interaction"] = str(self.Start_of_Interaction)
		self.Properties["Size_of_Ensemble"] = str(self.Size_of_Ensemble)
		
		self.Register_Topology()
			
	def Set_Topology(self):
		index_list = ["Ext","p"]
		for i in range(self.N):
			index_list.append("A%d"%(i+1))
		self.Info_Network.Set_Nodes(index_list)
		
		for i in range(self.N-1):
			self.Info_Network.Add_a_Link(("A%d"%(i+1),"A%d"%(i+2)))
			
		self.Info_Network.Add_a_Link(("A%d"%(self.N),"p"))
		self.Info_Network.Add_a_Link(("p","A1"))	
		self.Info_Network.Add_a_Link(("Ext","p"))
		
	def Init_State_Space(self):
		# 0: 00 / 1: 01 / 2: 10 / 3: 11
		for k in self.Info_Network.Nodes:
			s = numpy.random.random()
			self.State_Space[k] = numpy.searchsorted(self.Cumulative_Mass,s, side='right')
		self.State_Space["Ext"] = numpy.random.randint(0, self.Q)
			
	def Set_Estimator(self):
		self.Estimator = Simple_Binning.Estimator(self.Q, 4)
		self.Estimator.Source.Analysis = "Realtime"
		
	def Dynamics_of_States(self, t):
		for i in range(self.N-1):
			self.Update_Buffer["A%d"%(i+2)] = self.State_Space["A%d"%(i+1)]
			
		self.Update_Buffer["A1"] = self.State_Space["p"]
		self.Update_Buffer["Ext"] = numpy.random.randint(0, self.Q)
				
		if t < self.Start_of_Interaction:
			self.Update_Buffer["p"] = self.State_Space["A%d"%self.N]
		else:
			if self.State_Space["Ext"] > 1: # Ext == 2 or 3 : the first bit equals 1.
				if self.State_Space["A%d"%self.N] == 1 or self.State_Space["A%d"%self.N] == 2:
					self.Update_Buffer["p"] = 3 - self.State_Space["A%d"%self.N]
				else:
					self.Update_Buffer["p"] = self.State_Space["A%d"%self.N]
			else:							# Ext == 0 or 1 : the first bit equals 0.
				self.Update_Buffer["p"] = self.State_Space["A%d"%self.N]
		
	def Plot_Data(self, N_Trials, N_Param):
		Total_X = []
		Total_Y = []
		X_Data = []
		Y_Data = []
		for i in range(N_Param):
			X_Data.append([])
			Y_Data.append([])
		for j in range(N_Trials): #the number of trials
			for i in range(N_Param):
				Directory = self.Save_Directory + "Paper_%03d/Case%03d/Link_Ext_p.txt"%(j+1,i)
				Data_Flow = self.Read_for_(Directory)
				Y_Data[i].append(Data_Flow["TE2"][25])
				Total_Y.append(Data_Flow["TE2"][25])
				
				Directory = self.Save_Directory + "Paper_%03d/Case%03d/Link_A%d_p.txt"%(j+1,i,self.N)
				Data_Flow = self.Read_for_(Directory)
				X_Data[i].append(Data_Flow["TE2"][24])
				Total_X.append(Data_Flow["TE2"][24])
		X_Exact = []
		Y_Exact = []
		for i in range(N_Param):
			X_Exact.append(numpy.mean(X_Data[i]))
			Y_Exact.append(numpy.log(4)-numpy.mean(X_Data[i]))
		
		plt.figure(figsize=(9,4))
		plt.plot(Total_X, Total_Y, label="Estimations",marker='o', markersize = 4, markerfacecolor = 'none', linewidth = 0)
		plt.plot(X_Exact, Y_Exact, label="x + y = ln(4)",marker='o', markersize = 4, markerfacecolor = 'none', linewidth = 1)
		plt.xlabel(r'$T_{A3 \to p} (t_{0})$(nats)')
		plt.ylabel(r'$T_{Ext \to p} (t_{1})$(nats)')
		plt.title("Competing Information Flows : "+r'$T_{A3 \to p} (t_{0})$ vs $T_{Ext \to p} (t_{1})$')
		plt.legend()
		plt.tight_layout()
		plt.savefig(self.Save_Directory+"Figure3_a.png")
		plt.close()

	def Plot_Data2(self, N_Trials):
		Internal_Data = []
		External_Data = []
		i = 5
		for j in range(N_Trials): #the number of trials
			Directory = self.Save_Directory + "Paper_%03d/Case%03d/Link_Ext_p.txt"%(j+1,i)
			Data_Flow = self.Read_for_(Directory)
			External_Data.append(Data_Flow["TE2"])
				
			Directory = self.Save_Directory + "Paper_%03d/Case%03d/Link_A%d_p.txt"%(j+1,i,self.N)
			Data_Flow = self.Read_for_(Directory)
			Internal_Data.append(Data_Flow["TE2"])
			
		Internal_Data = numpy.asarray(Internal_Data, dtype=float)
		External_Data = numpy.asarray(External_Data, dtype=float)
		Internal_Mean = numpy.mean(Internal_Data, axis=1)
		External_Mean = numpy.mean(External_Data, axis=1)
		time_st = 20
		time_ed = 35
		timeline = list(range(time_st,time_ed))
		plt.figure(figsize=(9,4))
		for j in range(N_Trials):
			plt.plot(timeline, Internal_Data[j][time_st:time_ed], label="Estimation"+r'$T_{A3 \to p} (t)$',marker='o', markersize = 4, markerfacecolor = '#2166ac', linewidth = 0)
			plt.plot(timeline, External_Data[j][time_st:time_ed], label="Estimation"+r'$T_{Ext \to p} (t)$',marker='o', markersize = 4, markerfacecolor = '#d95f02', linewidth = 0)
		plt.plot(timeline, Internal_Mean[time_st:time_ed], label="mean curve"+r'$T_{A3 \to p} (t)$',marker='o', markersize = 4, markerfacecolor = '#2188dd', linewidth = 1)
		plt.plot(timeline, External_Mean[time_st:time_ed], label="mean curve"+r'$T_{Ext \to p} (t)$',marker='o', markersize = 4, markerfacecolor = '#fb9f02', linewidth = 1)
		plt.xlabel(r'Time steps')
		plt.ylabel(r'Transfer Entropy (nats)')
		plt.title("Evolution of Information Flows : Time"+r'$ t vs T_{A3 \to p} (t)$, $T_{Ext \to p} (t)$')
		plt.legend()
		plt.tight_layout()
		plt.savefig(self.Save_Directory+"Figure3_b.png")
		plt.close()
				
if __name__ == "__main__":
	N_Trials = 5
	N_Param = 10
	for j in range(N_Trials): #the number of trials
		os.makedirs("./on_Model/019_Fredkin_Switch_Gate/Temporal_Results/Paper_%03d/"%(j+1), exist_ok=True)
		for i in range(N_Param):
			print("\n Trial %03d , Case %03d"%(j+1,i))
			TEST = Fredkin_Switch_Gate(n = 3, theta = 0.24 - 0.02 * i)
			TEST.Save_Directory = "./on_Model/019_Fredkin_Switch_Gate/Temporal_Results/Paper_%03d/Case%03d/"%(j+1,i)
			try:
				os.mkdir(TEST.Save_Directory)
				TEST.Initialize()		
				TEST.Generate_Data()
			except FileExistsError:
				print("exists")
			
	TEST = Fredkin_Switch_Gate(n = 3)
	TEST.Plot_Data(N_Trials,N_Param)
	TEST.Plot_Data2(N_Trials)
		
