"""
005_Three_Nodes_GRN/main.py

Three-node gene regulatory motif model with continuous dynamics.

Main Dynamics
-------------
- Ordinary differential equations (ODEs)
- Ensemble of initial conditions
- Noise-robust oscillatory motif

Estimation Method
-----------------
- Post-analysis mode
- KSG k-nearest neighbor estimator
- Supports conditional mutual information

Core Reference
--------------
Qiao, L., Zhang, Z.-B., Zhao, W., Wei, P., & Zhang, L. (2022).
Network design principle for robust oscillatory behaviors
with respect to biological noise.
eLife, 11, e76188.

Outputs
-------
- Ensemble trajectories
- Entropy and transfer entropy estimates
- Conditional information measures

Notes
-----
- High-dimensional conditioning may lead to large variance.
- Ensemble size must be sufficiently large.
- Jitter added for distance degeneracy handling.

Data Attribution
----------------
The file `data_ex.mat` is sourced from the official implementation
associated with:

Qiao et al. (2022), eLife 11:e76188.

It contains motif definitions and parameter sets used in the
original publication. The file is redistributed here for
reproducibility within the present framework.
"""

import random
import numpy
from scipy import io

from on_Model.InfoDyn_lib import Model_Basics
from on_Model.InfoDyn_lib.Estimators import KSG

class Three_Nodes_Model(Model_Basics.Model_Basic):
	def __init__(self, Motif, New_Ensemble = True, Post_Analysis = False):	
		super().__init__()
		
		self.Total_Nodes = 3
		
		self.Simulation_Time_Limit = 10000
		self.Save_Interval = 10
		self.Time_Interval = 0.01		
		
		self.Size_of_Ensemble = 2000
		
		self.Selected_Motif = Motif	#Motif = 1 ~ 5 : Qiao2022 C1,C2,C3,C4,C5
		
		self.Save_Directory = "./on_Model/005_Three_Nodes_GRN/Temporal_Results/"	
		self.Ensemble_Directory = "./on_Model/005_Three_Nodes_GRN/C%d_Ensemble/"%(self.Selected_Motif)
		self.Data_Directory = "./on_Model/005_Three_Nodes_GRN/data_ex.mat"
		self.Set_Dynamic_Parameters()
		
		self.Selected = []
		self.Initialize()	
		if New_Ensemble:
			self.Generate_Data()
		if Post_Analysis:
			self.Post_Analysis()
		
	def Register_Properties(self):
		self.Properties["Model_Name"] = "Three Nodes ODE Model for GRN"
		self.Properties["Estimator"] = "KSG"
		self.Properties["Simulation_Time_Limit"] = str(self.Simulation_Time_Limit)
		self.Properties["Save_Interval"] = str(self.Save_Interval)
		self.Properties["Time_Interval"] = str(self.Time_Interval)
		self.Properties["Size_of_Ensemble"] = str(self.Size_of_Ensemble)
		self.Properties["Selected_Motif"] = str(self.Selected_Motif)
		
		self.Register_Topology()
		
	def Set_Topology(self):
		# Set Topology : Three nodes network
		# Create labels of nodes : node A, B, C
		index_list = ["A","B","C"]
		self.Info_Network.Set_Nodes(index_list)
		
		# Set Link A ~ B
		self.Info_Network.Add_a_Link(("A","B"))
		# Set Link B ~ C
		self.Info_Network.Add_a_Link(("B","C"))
		# Set Link C ~ A
		self.Info_Network.Add_a_Link(("C","A"))
		
	def Set_Estimator(self):
		self.Estimator = KSG.Estimator(self.Size_of_Ensemble)
		self.Estimator.Source.Analysis = "Post_Analysis"	
			
	def Init_State_Space(self):
		for k in self.Info_Network.Nodes:
			initial_value = random.uniform(0,10)
			self.State_Space[k] = initial_value	
		
	def Dynamics_of_States(self):
		A_ODE, B_ODE, C_ODE = self._Hill_fnc_ODE()
		
		self.Update_Buffer["A"] = self.State_Space["A"] + self.Time_Interval * A_ODE
		self.Update_Buffer["B"] = self.State_Space["B"] + self.Time_Interval * B_ODE		
		self.Update_Buffer["C"] = self.State_Space["C"] + self.Time_Interval * C_ODE
		
	def _Hill_fnc_ODE(self):
		States = [self.State_Space["A"],self.State_Space["B"],self.State_Space["C"]]
		Pow3 = [numpy.power(self.State_Space["A"],3), numpy.power(self.State_Space["B"],3), numpy.power(self.State_Space["C"],3)]
		Result = []
		for i in range(3):
			buf1 = 0
			for j in range(3):
				buf1 += self.J_plus[i][j]* self.v[i][j][self.Selected_Motif-1] * Pow3[j] / numpy.power(self.K[i][j][self.Selected_Motif-1],3)
			if buf1 == 0:
				buf1 = self.delta[i][self.Selected_Motif-1]
				
			buf2 = 1
			for j in range(3):
				buf2 += self.J_abs[i][j]* Pow3[j] / numpy.power(self.K[i][j][self.Selected_Motif-1],3)
				
			rst = self.K_basal + buf1/buf2 - self.r[i][self.Selected_Motif-1] * States[i]
			Result.append(rst)
			
		return tuple(Result)
			
	def Set_Dynamic_Parameters(self):
		self.K_basal = 0.01		
		mat_data = io.loadmat(self.Data_Directory)
		self.K = mat_data.get('matrix_K_all')
		self.v = mat_data.get('matrix_v_all')
		self.r = mat_data.get('vector_r_all')
		self.delta = mat_data.get('vector_delta_all')
		J = mat_data.get('J_%d'%(self.Selected_Motif))
		
		self.J_abs = numpy.abs(J)
		self.J_plus = 0.5*(J + self.J_abs)
		
	def Plot_Data(self):
		pass
		
if __name__ == "__main__":
	for i in range(5):
		TEST = Three_Nodes_Model(i+1, New_Ensemble = True, Post_Analysis = False)

	TEST = Three_Nodes_Model(1, New_Ensemble = False, Post_Analysis = True)



