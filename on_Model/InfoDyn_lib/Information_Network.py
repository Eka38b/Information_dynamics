

class A_Node():
	def __init__(self, Index):
		self.Index = Index
		self.Neighbors = []
		
		self.Var_ = {"H0":0}
		self.Alpha_ = {"1":0, "partial1":0}
		
	def Calculate(self, Estimator):
		self.Var_["H0"] = Estimator.Conditional_Entropy(For = [self.Index])
		self.Alpha_["partial1"] = Estimator.Conditional_Entropy(For = [self.Index+"'"],  Known = [self.Index])
		
		
class A_Link():
	def __init__(self, Index_Tuple):
		self.Index_Tuple = Index_Tuple
		self.Var_ = {"MI":0,"TE1":0,"rTE1":0,"TE2":0,"rTE2":0} # TE1 := T_{B -> A}, TE2 := T_{A -> B}
		self.Alpha_ = {"2":0, "3_1_I":0, "3_2_I":0, "4_1_I":0, "4_2_I":0, "5_I":0, "6_1_I":0, "6_2_I":0}
		# Alpha_3_1_I : Alpha_3_1 (t0) = Alpha_3_1_I (t1)- Alpha_3_1_I (t0)
		
	def Calculate(self, Estimator):
		X_t1 = self.Index_Tuple[0]
		Y_t1 = self.Index_Tuple[1]
		X_t2 = self.Index_Tuple[0]+"'"
		Y_t2 = self.Index_Tuple[1]+"'"
		self.Var_["MI"] = Estimator.Mutual_Information(For = [X_t1,Y_t1])
		self.Var_["TE1"] = Estimator.Mutual_Information(For = [Y_t1,X_t2],  Known = [X_t1])
		self.Var_["rTE1"] = Estimator.Mutual_Information(For = [Y_t2,X_t1],  Known = [X_t2])
		self.Var_["TE2"] = Estimator.Mutual_Information(For = [X_t1,Y_t2],  Known = [Y_t1])
		self.Var_["rTE2"] = Estimator.Mutual_Information(For = [X_t2,Y_t1],  Known = [Y_t2])
		
		self.Alpha_["2"] = Estimator.Mutual_Information(For = [X_t2,Y_t2],  Known = [X_t1,Y_t1]) - Estimator.Mutual_Information(For = [X_t1,Y_t1],  Known = [X_t2,Y_t2])
		self.Alpha_["3_1_I"] = Estimator.Conditional_Entropy(For = [Y_t1],  Known = [X_t1,X_t2])
		self.Alpha_["3_2_I"] = Estimator.Conditional_Entropy(For = [X_t1],  Known = [Y_t1,Y_t2])
		self.Alpha_["4_1_I"] = Estimator.Conditional_Entropy(For = [X_t2]) - Estimator.Conditional_Entropy(For = [X_t1])
		self.Alpha_["4_2_I"] = Estimator.Conditional_Entropy(For = [Y_t2]) - Estimator.Conditional_Entropy(For = [Y_t1])
		self.Alpha_["5_I"] = Estimator.Mutual_Information(For = [Y_t2,X_t2]) - Estimator.Mutual_Information(For = [Y_t1,X_t1])
		self.Alpha_["6_1_I"] = Estimator.Conditional_Entropy(For = [Y_t2],  Known = [X_t1,X_t2])
		self.Alpha_["6_2_I"] = Estimator.Conditional_Entropy(For = [X_t2],  Known = [Y_t1,Y_t2])
		
class A_Network():
	def __init__(self):
		self.Nodes= {}
		self.Links = {}
		
	def Set_Nodes(self, Index_List):
		for k in Index_List:
			a_node = A_Node(k)
			self.Nodes[k] = a_node
	
	def Add_a_Link(self, Index_Tuple):
		a_link = A_Link(Index_Tuple)
		self.Links[Index_Tuple] = a_link
		self.Nodes[Index_Tuple[0]].Neighbors.append(Index_Tuple[1])
		self.Nodes[Index_Tuple[1]].Neighbors.append(Index_Tuple[0])
	
	

	
