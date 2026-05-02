
import time
import random
import numpy

#import os
import matplotlib.pyplot as plt

from Core import Model_Basics
from Core.Estimators import Simple_Binning

class Boolean_Probability_Update(Model_Basics.Model_Basic):
	def __init__(self, n=4, beta_Int = 1, beta_Ext = 1):
		super().__init__()
		
		self.Q = 2
		self.N = n
		
		self.beta_Int = beta_Int
		self.beta_Ext = beta_Ext
		numpy.random.seed(int(time.time()))
		
		self.Simulation_Time_Limit = 40
		self.Start_of_Interaction = 25
		self.Size_of_Ensemble = 10000
		
		
		self.Save_Directory = "./on_Model/015_Boolean_Probability_Update/Temporal_Results/"
		
		self.Selected_Nodes = ["p"]
		self.Selected_Links = [("A%d"%self.N,"p"), ("Ext","p"),("p","A1")]
		
		
	def Register_Properties(self):
		self.Properties["Model_Name"] = "Boolean_Probability_Update"
		self.Properties["Estimator"] = "Simple Binning"
		self.Properties["Q"] = str(self.Q)
		self.Properties["N"] = str(self.N)
		self.Properties["beta_Int"] = str(self.beta_Int)
		self.Properties["beta_Ext"] = str(self.beta_Ext)
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
		for k in self.Info_Network.Nodes:
			initial_value = numpy.random.binomial(1,0.5)
			self.State_Space[k] = initial_value	
			
	def Set_Estimator(self):
		self.Estimator = Simple_Binning.Estimator(self.Q, 4)
		self.Estimator.Source.Analysis = "Realtime"
		
	def Dynamics_of_States(self, t):
		for i in range(self.N-1):
			self.Update_Buffer["A%d"%(i+2)] = self.State_Space["A%d"%(i+1)]
			
		self.Update_Buffer["A1"] = self.State_Space["p"]
		self.Update_Buffer["Ext"] = numpy.random.binomial(1,0.5)
				
		if t < self.Start_of_Interaction:
			update_probability = numpy.exp(- self.beta_Int * self.State_Space["A%d"%self.N])			
		else:
			update_probability = numpy.exp(- self.beta_Int * self.State_Space["A%d"%self.N] - self.beta_Ext * self.State_Space["Ext"])
			
		self.Update_Buffer["p"] = numpy.random.binomial(1,update_probability)
		
	def Plot_Data(self):
		Total_X = []
		Total_Y = []
		X_Data = []
		Y_Data = []
		for i in range(10):
			X_Data.append([])
			Y_Data.append([])
		for j in range(9):
			for i in range(10):
				Directory = "./on_Model/015_Boolean_Probability_Update/Temporal_Results/Paper_%03d/Case%03d/Link_Ext_p.txt"%(j+1,i)
				Data_Flow = self.Read_for_(Directory)
				Y_Data[i].append(Data_Flow["TE2"][25])
				Total_Y.append(Data_Flow["TE2"][25])
				
				Directory = "./on_Model/015_Boolean_Probability_Update/Temporal_Results/Paper_%03d/Case%03d/Link_A4_p.txt"%(j+1,i)
				Data_Flow = self.Read_for_(Directory)
				X_Data[i].append(Data_Flow["TE2"][24])
				Total_X.append(Data_Flow["TE2"][24])
		X_Mean_data = []
		X_Std_data = []
		Y_Mean_data = []
		Y_Std_data = []
		for i in range(10):
			X_Mean_data.append(numpy.mean(X_Data[i]))
			X_Std_data.append(numpy.std(X_Data[i]))
			Y_Mean_data.append(numpy.mean(Y_Data[i]))
			Y_Std_data.append(numpy.std(Y_Data[i]))
		
		plt.figure(figsize=(9,4))
		plt.plot(Total_X, Total_Y, label="Estimations",marker='o', markersize = 4, markerfacecolor = 'none', linewidth = 0)
		plt.plot(X_Mean_data, Y_Mean_data, label="Mean Curve",marker='o', markersize = 4, markerfacecolor = 'none', linewidth = 1)
		plt.xlabel(r'$T_{A4 \to p} (t_{0})$')
		plt.ylabel(r'$T_{Ext \to p} (t_{1})$')
		plt.title("Competing Information Flows : "+r'$T_{A4 \to p} (t_{0})$ vs $T_{Ext \to p} (t_{1})$')
		plt.legend()
		plt.tight_layout()
		plt.show()
		plt.close()
	
if __name__ == "__main__":
	for j in range(10):
		#os.mkdir("./on_Model/015_Boolean_Probability_Update/Temporal_Results/Paper_%03d/"%(j+1))
		for i in range(10):
			print("\n Trial %03d , Case %03d"%(j+1,i))
			TEST = Boolean_Probability_Update(n = 4, beta_Int = 1+ 0.2 * i, beta_Ext = 4)
			TEST.Save_Directory = "./on_Model/015_Boolean_Probability_Update/Temporal_Results/Paper_%03d/Case%03d/"%(j+1,i)
			#os.mkdir(TEST.Save_Directory)
			TEST.Initialize()		
			TEST.Generate_Data()
	TEST = Boolean_Probability_Update()
	TEST.Plot_Data()
		