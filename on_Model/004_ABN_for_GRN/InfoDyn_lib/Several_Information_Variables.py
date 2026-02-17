
from InfoDyn_lib import From_Simple_Bin
from InfoDyn_lib import Entropy

class An_Information_Variable():
	def __init__(self):
		self.Name = ""
		
		self.Statistics = {}
		self.Value = 0
		self.Dimension = 0
		
	def Initialize_Statistics(self, Size):
		Size_List = []
		Index = []
		for i in range(self.Dimension):
			Size_List.append(Size)
			Index.append(0)
		self.Recurr_Initialize_Statistics(Size_List, Index)
		
	def Recurr_Initialize_Statistics(self, Size_List, Index):
		dl = len(Index)
		l = len(Size_List)
		if l == 0:
			self.Statistics[tuple(Index)] = 0
			return
		for i in range(Size_List[0]):
			Index[dl-l] = i
			self.Recurr_Initialize_Statistics(Size_List[1:], Index)
			
	def Update_Statistics(self, State_Space, Update_Buffer):
		pass
		
	def Estimate_the_Variable(self):
		pass
		
	def Save_the_Variable(self, Save_Directory, Simulation_Time):
		pass

class H_XYZ(An_Information_Variable):
	def __init__(self, Index_Tuple):
		super().__init__()
		self.Index_Tuple = Index_Tuple
		self.Name = "H_%s%s%s"%Index_Tuple
		self.Dimension = 3
		
	def Update_Statistics(self, State_Space, Update_Buffer):
		self.Statistics[(State_Space[self.Index_Tuple[0]],State_Space[self.Index_Tuple[1]],State_Space[self.Index_Tuple[2]])] += 1
		
	def Estimate_the_Variable(self):	
		Bin_Stat = From_Simple_Bin.Source(self.Statistics,["X","Y","Z"])
		
		Estimated_H_XYZ = Entropy.Conditional_Entropy(Bin_Stat, For = ["X","Y","Z"]).Value
		
		H_X = Entropy.Conditional_Entropy(Bin_Stat, For = ["X"]).Value
		H_Y = Entropy.Conditional_Entropy(Bin_Stat, For = ["Y"]).Value
		H_Z = Entropy.Conditional_Entropy(Bin_Stat, For = ["Z"]).Value
		MI_XY = Entropy.Mutual_Information(Bin_Stat, For = ["X","Y"]).Value
		MI_YZ = Entropy.Mutual_Information(Bin_Stat, For = ["Y","Z"]).Value
		MI_ZX = Entropy.Mutual_Information(Bin_Stat, For = ["Z","X"]).Value
		MI_XYZ = Entropy.Mutual_Information(Bin_Stat, For = ["X","Y"]).Value - Entropy.Mutual_Information(Bin_Stat, For = ["X","Y"],  Known = ["Z"]).Value					
		Calculated_H_XYZ = H_X + H_Y + H_Z - MI_XY - MI_YZ - MI_ZX + MI_XYZ
		#print("H_XYZ = %0.3f = %0.3f = %0.3f + %0.3f + %0.3f - %0.3f - %0.3f - %0.3f + %0.3f"%(Estimated_H_XYZ,Calculated_H_XYZ,H_X,H_Y,H_Z,MI_XY,MI_YZ,MI_ZX,MI_XYZ))
		self.Value = Estimated_H_XYZ
		return
		
	def Save_the_Variable(self, Save_Directory, Simulation_Time):
		save_file = open(Save_Directory + self.Name + ".txt",'a')
		save_file.write("%03d: %0.3f|\n"%(Simulation_Time,self.Value))
		save_file.close()

class H_XYZW(An_Information_Variable):
	def __init__(self, Index_Tuple):
		super().__init__()
		self.Index_Tuple = Index_Tuple		
		self.Name = "H_%s%s%s%s"%Index_Tuple
		self.Dimension = 4
		
	def Update_Statistics(self, State_Space, Update_Buffer):
		self.Statistics[(State_Space[self.Index_Tuple[0]],State_Space[self.Index_Tuple[1]],State_Space[self.Index_Tuple[2]],State_Space[self.Index_Tuple[3]])] += 1

	def Estimate_the_Variable(self):	
		Bin_Stat = From_Simple_Bin.Source(self.Statistics,["X","Y","Z","W"])
		self.Value = Entropy.Conditional_Entropy(Bin_Stat, For = ["X","Y","Z","W"]).Value
		return
	
	def Save_the_Variable(self, Save_Directory, Simulation_Time):
		save_file = open(Save_Directory + self.Name + ".txt",'a')
		save_file.write("%03d: %0.3f|\n"%(Simulation_Time,self.Value))
		save_file.close()
		
class T2(An_Information_Variable):
	def __init__(self, Index_Tuple):	# (X, Y, Ext)
		super().__init__()
		self.Index_Tuple = Index_Tuple		
		self.Name = "Multiple_Transfer_Entropy_order_2"
		self.Value = {"T^2_{%s %s -> %s}"%(Index_Tuple[2],Index_Tuple[0],Index_Tuple[1]):0,"T^2_{%s -> %s %s}"%(Index_Tuple[2],Index_Tuple[0],Index_Tuple[1]):0, "T^2_{%s %s -> %s}"%(Index_Tuple[2],Index_Tuple[1],Index_Tuple[0]):0}
		self.Dimension = 5
		
	def Update_Statistics(self, State_Space, Update_Buffer):
		self.Statistics[(State_Space[self.Index_Tuple[0]],State_Space[self.Index_Tuple[1]],State_Space[self.Index_Tuple[2]],Update_Buffer[self.Index_Tuple[0]],Update_Buffer[self.Index_Tuple[1]])] += 1
		
	def Estimate_the_Variable(self):	
		Bin_Stat = From_Simple_Bin.Source(self.Statistics,["X","Y","Ext","X'","Y'"])
		
		self.Value["T^2_{%s %s -> %s}"%(self.Index_Tuple[2],self.Index_Tuple[0],self.Index_Tuple[1])] = Entropy.Multiple_Mutual_Information(Bin_Stat, For = ["Ext","X","Y'"],  Known = ["Y"]).Value
		self.Value["T^2_{%s -> %s %s}"%(self.Index_Tuple[2],self.Index_Tuple[0],self.Index_Tuple[1])] = Entropy.Multiple_Mutual_Information(Bin_Stat, For = ["Ext","X'","Y'"],  Known = ["X","Y"]).Value
		self.Value["T^2_{%s %s -> %s}"%(self.Index_Tuple[2],self.Index_Tuple[1],self.Index_Tuple[0])] = Entropy.Multiple_Mutual_Information(Bin_Stat, For = ["Ext","Y","X'"],  Known = ["X"]).Value
		
		return
		
	def Save_the_Variable(self, Save_Directory, Simulation_Time):
		save_file = open(Save_Directory + self.Name + ".txt",'a')
		save_file.write("%03d: "%(Simulation_Time))
		for val in self.Value:
			save_file.write("%0.3f|"%(self.Value[val]))
		save_file.write("\n")
		save_file.close()

		


