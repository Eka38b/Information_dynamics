

class A_Node():
	def __init__(self, Index):
		self.Index = Index
		self.Neighbors = []
		
		self.Var_ = {"H0":[], "H0'":[]}
		self.Alpha_ = {"1":[], "1_p1":[], "1_p2":[], "partial1":[]}
		
	def Calculate(self, Estimator):
		value = Estimator.Conditional_Entropy(For = [self.Index])
		self.Var_["H0"].append(value)
		
		value = Estimator.Conditional_Entropy(For = [self.Index+"'"])
		self.Var_["H0'"].append(value)
		
		Previous_variables = [self.Index] + self.Neighbors
		value = Estimator.Conditional_Entropy(For = [self.Index+"'"],  Known = Previous_variables)
		self.Alpha_["1_p1"].append(value)
		
		Future_variables = []
		for pv in Previous_variables:
			Future_variables.append(pv + "'")
		value = Estimator.Conditional_Entropy(For = [self.Index],  Known = Future_variables)
		self.Alpha_["1_p2"].append(value)
		
		self.Alpha_["1"].append(self.Alpha_["1_p1"][-1] - self.Alpha_["1_p2"][-1])
		
		value = Estimator.Conditional_Entropy(For = [self.Index+"'"],  Known = [self.Index])
		self.Alpha_["partial1"].append(value)
		
class A_Link():
	def __init__(self, Index_Tuple):
		self.Index_Tuple = Index_Tuple
		self.Var_ = {"MI":[],"TE1":[],"rTE1":[],"TE2":[],"rTE2":[]} # TE1 := T_{B -> A}, TE2 := T_{A -> B}
		self.Alpha_ = {"2":[], "3_1":[], "3_2":[], "4_1":[], "4_2":[], "5":[], "6_1":[], "6_2":[], "3_1_I":[], "3_2_I":[], "4_1_I":[], "4_2_I":[], "5_I":[], "6_1_I":[], "6_2_I":[]}
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
		
	def Calculate(self, Estimator):
		X_t1 = self.Index_Tuple[0]
		Y_t1 = self.Index_Tuple[1]
		X_t2 = self.Index_Tuple[0]+"'"
		Y_t2 = self.Index_Tuple[1]+"'"
		self.Var_["MI"].append(Estimator.Mutual_Information(For = [X_t1,Y_t1]))
		self.Var_["TE1"].append(Estimator.Mutual_Information(For = [Y_t1,X_t2],  Known = [X_t1]))
		self.Var_["rTE1"].append(Estimator.Mutual_Information(For = [Y_t2,X_t1],  Known = [X_t2]))
		self.Var_["TE2"].append(Estimator.Mutual_Information(For = [X_t1,Y_t2],  Known = [Y_t1]))
		self.Var_["rTE2"].append(Estimator.Mutual_Information(For = [X_t2,Y_t1],  Known = [Y_t2]))
		
		self.Alpha_["2"].append(Estimator.Mutual_Information(For = [X_t2,Y_t2],  Known = [X_t1,Y_t1]) - Estimator.Mutual_Information(For = [X_t1,Y_t1],  Known = [X_t2,Y_t2]))
		self.Alpha_["3_1_I"].append(Estimator.Conditional_Entropy(For = [Y_t1],  Known = [X_t1,X_t2]))
		self.Alpha_["3_2_I"].append(Estimator.Conditional_Entropy(For = [X_t1],  Known = [Y_t1,Y_t2]))
		self.Alpha_["4_1_I"].append(Estimator.Conditional_Entropy(For = [X_t2]) - Estimator.Conditional_Entropy(For = [X_t1]))
		self.Alpha_["4_2_I"].append(Estimator.Conditional_Entropy(For = [Y_t2]) - Estimator.Conditional_Entropy(For = [Y_t1]))
		self.Alpha_["5_I"].append(Estimator.Mutual_Information(For = [Y_t2,X_t2]) - Estimator.Mutual_Information(For = [Y_t1,X_t1]))
		self.Alpha_["6_1_I"].append(Estimator.Conditional_Entropy(For = [Y_t2],  Known = [X_t1,X_t2]))
		self.Alpha_["6_2_I"].append(Estimator.Conditional_Entropy(For = [X_t2],  Known = [Y_t1,Y_t2]))
		
		if len(self.Alpha_["3_1_I"]) > 1:
			self.Alpha_["3_1"].append(self.Alpha_["3_1_I"][-1] - self.Alpha_["3_1_I"][-2])
			self.Alpha_["3_2"].append(self.Alpha_["3_2_I"][-1] - self.Alpha_["3_2_I"][-2])
			self.Alpha_["4_1"].append(self.Alpha_["4_1_I"][-1] - self.Alpha_["4_1_I"][-2])
			self.Alpha_["4_2"].append(self.Alpha_["4_2_I"][-1] - self.Alpha_["4_2_I"][-2])
			self.Alpha_["5"].append(self.Alpha_["5_I"][-1] - self.Alpha_["5_I"][-2])
			self.Alpha_["6_1"].append(self.Alpha_["6_1_I"][-1] - self.Alpha_["6_1_I"][-2])
			self.Alpha_["6_2"].append(self.Alpha_["6_2_I"][-1] - self.Alpha_["6_2_I"][-2])
		
		
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
	
	
	