
from InfoDyn_lib import From_Simple_Bin
from InfoDyn_lib import Entropy

class A_Node():
	def __init__(self):
		self.Neighbors = []
		
		self.Var_ = {"H0":0}
		self.Alpha_ = {"1":0, "partial1":0}
		
	def Calculate(self, Statistics, Node_Index):
		Bin_Stat = From_Simple_Bin.Source(Statistics, ("X","Y","X'","Y'"))
		if Node_Index == 0:
			var_name = "X"
		else:
			var_name = "Y"
		self.Var_["H0"] = Entropy.Conditional_Entropy(Bin_Stat, For = [var_name]).Value
		self.Alpha_["partial1"] = Entropy.Conditional_Entropy(Bin_Stat, For = [var_name+"'"],  Known = [var_name]).Value
		
		
class A_Link():
	def __init__(self):
		self.Var_ = {"MI":0,"TE1":0,"rTE1":0,"TE2":0,"rTE2":0} # TE1 := T_{B -> A}, TE2 := T_{A -> B}
		self.Alpha_ = {"2":0, "3_1_I":0, "3_2_I":0, "4_1_I":0, "4_2_I":0, "5_I":0, "6_1_I":0, "6_2_I":0}
		# Alpha_3_1_I : Alpha_3_1 (t0) = Alpha_3_1_I (t1)- Alpha_3_1_I (t0)
		
	def Set_from_List(self, Data_List):
		if len(Data_List) != (len(self.Var_)+len(self.Alpha_)):
			print("ERROR : DATA LIST LENGTH")
			return
			
		list_ind = 0
		for v in self.Var_:
			self.Var_[v] = Data_List[list_ind]
			list_ind += 1
		for a in self.Alpha_:
			self.Alpha_[a] = Data_List[list_ind]
			list_ind += 1
		return
		
	def Calculate(self, Statistics):
		Bin_Stat = From_Simple_Bin.Source(Statistics, ("X","Y","X'","Y'"))
		
		self.Var_["MI"] = Entropy.Mutual_Information(Bin_Stat, For = ["X","Y"]).Value
		self.Var_["TE1"] = Entropy.Mutual_Information(Bin_Stat, For = ["Y","X'"],  Known = ["X"]).Value
		self.Var_["rTE1"] = Entropy.Mutual_Information(Bin_Stat, For = ["Y'","X"],  Known = ["X'"]).Value
		self.Var_["TE2"] = Entropy.Mutual_Information(Bin_Stat, For = ["X","Y'"],  Known = ["Y"]).Value
		self.Var_["rTE2"] = Entropy.Mutual_Information(Bin_Stat, For = ["X'","Y"],  Known = ["Y'"]).Value
		
		self.Alpha_["2"] = Entropy.Mutual_Information(Bin_Stat, For = ["X'","Y'"],  Known = ["X","Y"]).Value - Entropy.Mutual_Information(Bin_Stat, For = ["X","Y"],  Known = ["X'","Y'"]).Value
		self.Alpha_["3_1_I"] = Entropy.Conditional_Entropy(Bin_Stat, For = ["Y"],  Known = ["X","X'"]).Value
		self.Alpha_["3_2_I"] = Entropy.Conditional_Entropy(Bin_Stat, For = ["X"],  Known = ["Y","Y'"]).Value
		self.Alpha_["4_1_I"] = Entropy.Conditional_Entropy(Bin_Stat, For = ["X'"]).Value - Entropy.Conditional_Entropy(Bin_Stat, For = ["X"]).Value
		self.Alpha_["4_2_I"] = Entropy.Conditional_Entropy(Bin_Stat, For = ["Y'"]).Value - Entropy.Conditional_Entropy(Bin_Stat, For = ["Y"]).Value
		self.Alpha_["5_I"] = Entropy.Mutual_Information(Bin_Stat, For = ["Y'","X'"]).Value - Entropy.Mutual_Information(Bin_Stat, For = ["Y","X"]).Value
		self.Alpha_["6_1_I"] = Entropy.Conditional_Entropy(Bin_Stat, For = ["Y'"],  Known = ["X","X'"]).Value
		self.Alpha_["6_2_I"] = Entropy.Conditional_Entropy(Bin_Stat, For = ["X'"],  Known = ["Y","Y'"]).Value
		
class A_Network():
	def __init__(self):
		self.Nodes= {}
		self.Links = {}
		
	def Set_Nodes(self, Index_List):
		for k in Index_List:
			a_node = A_Node()
			self.Nodes[k] = a_node
	
	def Add_a_Link(self, Index_Pair):
		a_link = A_Link()
		self.Links[Index_Pair] = a_link
		self.Nodes[Index_Pair[0]].Neighbors.append(Index_Pair[1])
		self.Nodes[Index_Pair[1]].Neighbors.append(Index_Pair[0])
	
	
	