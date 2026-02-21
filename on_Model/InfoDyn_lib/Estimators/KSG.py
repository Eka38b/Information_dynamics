
import numpy
from scipy.special import digamma
from sklearn.neighbors import NearestNeighbors

from on_Model.InfoDyn_lib.Estimators import Estimator_Basics

class Source(Estimator_Basics.Source):
	def __init__(self, Ensemble_Size):
		self.Analysis = "Post_Analysis"
		self.Ensemble_Size = Ensemble_Size
		
		self.Variable_Names = []
		self.Ensemble = []
		
	def Init_Source_Realtime(self, Simulation_Nodes):
		if self.Analysis != "Realtime":
			return
		self.Variable_Names = []
		for X in Simulation_Nodes:
			self.Variable_Names.append(X)
			self.Variable_Names.append(X+"'")
		self.Ensemble = []
		
	def Update_Source_Realtime(self, State_Space, Update_Buffer):
		if self.Analysis != "Realtime":
			return
		state_value_list = []
		for Name in self.Variable_Names:
			if Name[-1] == "'":
				state_value_list.append(Update_Buffer[Name[:-1]])
			else:
				state_value_list.append(State_Space[Name])
		self.Ensemble.append(state_value_list)
		
	def Init_Source_Post_Analysis(self, Nodes, Ensemble_Data_File):
		self.Variable_Names = []
		for X in Nodes:
			self.Variable_Names.append(X)
			self.Variable_Names.append(X+"'")
			
		self.Ensemble = []
		Data_File = open(Ensemble_Data_File, 'r')
		for f in range(self.Ensemble_Size):
			data_line = Data_File.readline()
			data_list = []
			for d in data_line.split("|"):
				data_list.append(float(d))
			self.Ensemble.append(data_list)
		self.Ensemble = numpy.asarray(self.Ensemble)
		Data_File.close()
		if self.Ensemble.shape[1] != len(self.Variable_Names):
			raise ValueError("Check ensemble shape :" + str(self.Ensemble.shape))
			
class Estimator(Estimator_Basics.Estimator):
	def __init__(self, Ensemble_Size):
		self.Name = "KSG_estimator"
		
		self.k = 10
		self.jitter = 1e-10
		
		self.RNG = numpy.random.default_rng(0)
		
		self.Source = Source(Ensemble_Size)
		
	def Entropy(self, For = []):
		self.Source.Ensemble = self._as_2D(self.Source.Ensemble)
		Variables = []
		for Name in For:
			Var = self.Source.Ensemble[:,self.Source.Variable_Names.index(Name)]
			Var = self._Add_Jitter(self._Standardize(self._as_2D(Var)))
			Variables.append(Var)
			
		N = Variables[0].shape[0]
		d = len(Variables)
		epsilon = self._Calculate_kNN_Epsilon(Variables, k = self.k)
		H = digamma(N) - digamma(self.k) + d* numpy.log(2.0) + (d/N) * numpy.sum(numpy.log(epsilon + 1e-300))
		return float(H)
		
	def Conditional_Entropy(self, For = [], Known = []):
		self.Source.Ensemble = self._as_2D(self.Source.Ensemble)
		if len(Known) == 0 :
			Value = self.Entropy(For)
		else:
			Value = self.Entropy(For) - self.Mutual_Information(For = For+Known)
		return Value
		
	def Mutual_Information(self, For = [], Known = []):
		self.Source.Ensemble = self._as_2D(self.Source.Ensemble)
		X = self.Source.Ensemble[:,self.Source.Variable_Names.index(For[0])]
		Y = self.Source.Ensemble[:,self.Source.Variable_Names.index(For[1])]
		
		X = self._Add_Jitter(self._Standardize(self._as_2D(X)))
		Y = self._Add_Jitter(self._Standardize(self._as_2D(Y)))		
		
		if len(Known) != 0:
			known_list = []
			for k in Known:
				array_buf = self.Source.Ensemble[:,self.Source.Variable_Names.index(k)]
				known_list.append(self._as_2D(array_buf))
			Z = numpy.concatenate(known_list, axis = 1)
			Z = self._Add_Jitter(self._Standardize(self._as_2D(Z)))
			
			epsilon = self._Calculate_kNN_Epsilon([X,Y,Z], k = self.k)
			nxz = self._Count_within_Epsilon([X,Z], epsilon)
			nyz = self._Count_within_Epsilon([Y,Z], epsilon)
			nz = self._Count_within_Epsilon([Z], epsilon)
			
			MI = digamma(self.k) - numpy.mean(digamma(nxz + 1) + digamma(nyz + 1) - digamma(nz + 1))
			
		else:
			epsilon = self._Calculate_kNN_Epsilon([X,Y], k = self.k)
			nx = self._Count_within_Epsilon([X], epsilon)
			ny = self._Count_within_Epsilon([Y], epsilon)
			n = X.shape[0]
			
			MI = digamma(self.k) + digamma(n) - numpy.mean(digamma(nx + 1) + digamma(ny + 1))
		return float(MI)
	
	
	def Multiple_Mutual_Information(self, For = [], Known = []):
		pass
		
	
	def _as_2D(self, array_A):
		buf_A = numpy.asarray(array_A)
		if buf_A.ndim == 1:
			return buf_A.reshape(-1,1)	
		if buf_A.ndim != 2:
			raise ValueError("Check the array.ndim")
		return buf_A
		
	def _Standardize(self, array_A):
		Avg = numpy.mean(array_A, axis = 0, keepdims = True)
		Std = numpy.std(array_A, axis = 0, keepdims = True)
		return (array_A - Avg) / (Std + 1e-12)
	
	def _Add_Jitter(self, array_A):
		scale = self.jitter * (numpy.std(array_A,axis=0,keepdims=True) + 1e-12)
		return array_A + self.RNG.normal(0.0,1.0, size=array_A.shape) * scale
	
	def _Calculate_kNN_Epsilon(self, Variables, k):
		array_A = numpy.concatenate(Variables, axis = 1)
		
		n = array_A.shape[0]
		NN = NearestNeighbors(metric = "chebyshev", algorithm = "auto")
		NN.fit(array_A)
		dists, _ = NN.kneighbors(array_A, n_neighbors = k + 1)
		epsilon = dists[:,-1]
		return epsilon
	
	def _Count_within_Epsilon(self, Variables, epsilon):
		array_A = numpy.concatenate(Variables, axis = 1)
		
		NN = NearestNeighbors(metric = "chebyshev", algorithm = "auto")
		NN.fit(array_A)
		counts = numpy.empty(array_A.shape[0], dtype = int)
		for i, e in enumerate(epsilon):
			r = numpy.nextafter(e, -numpy.inf)
			neighbors = NN.radius_neighbors(array_A[i:i+1], radius=r, return_distance = False)[0]
			counts[i] = max(len(neighbors) - 1 , 0)
		return counts

	
