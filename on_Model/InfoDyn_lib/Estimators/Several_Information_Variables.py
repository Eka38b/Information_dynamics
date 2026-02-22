"""
Several_Information_Variables.py

Composite (multi-variable) information measures built on top of the
base estimator interface. This module defines convenience classes for
computing and storing higher-order information quantities that are
frequently required in information-dynamical decompositions.

Main Idea
---------
Many network information terms (e.g., transfer-entropy–like quantities,
partial information terms, or multi-variable corrections) can be
expressed as combinations of entropies and (conditional) mutual
informations over joint variables.

This module provides a pattern:

1) Define a new "additional information variable" class.
2) Specify which variables are needed (e.g., X, Y, X', Y').
3) Update the underlying estimator's data source (realtime or post-analysis).
4) Compute the target quantity using entropy/MI/CMI identities.
5) Store the resulting time series into `Temporal_Results/`.

Core References
---------------
Cover, T. M., & Thomas, J. A. (2006).
Elements of Information Theory.

McGill, W. J. (1954).
Multivariate information transmission.
Psychometrika, 19, 97–116.
(For interaction information / multi-variable MI concepts.)

Schreiber, T. (2000).
Measuring information transfer.
Physical Review Letters, 85, 461–464.
(For transfer entropy as conditional mutual information.)

Notes on Outputs
----------------
Classes in this module are designed to produce:

- A scalar information value at each time step (or analysis step)
- Saved as a time series, typically in:
      <Model>/Temporal_Results/

Depending on the model workflow:
- Realtime mode writes values during simulation.
- Post-analysis mode computes values from stored ensemble snapshots.

Numerical / Practical Notes
---------------------------
1) Dimensionality growth
   Many composite quantities require joint spaces such as (X, Y, Z, ...).
   For continuous estimators (KSG), variance increases rapidly with the
   total joint dimension. For discrete/binning estimators, memory scales
   as Q^dimension.

2) Conditioning complexity
   Conditional terms like I(X;Y|Z) require neighbor counts (KSG) or
   joint histograms (binning). High-dimensional Z can make the estimate
   unreliable without dimensionality reduction or parent-set truncation.

3) Negative estimates
   kNN-based MI/CMI estimates can be slightly negative due to finite-sample
   bias. This is a known numerical artifact; consider reporting confidence
   intervals, using bias correction, or truncating small negatives to zero
   depending on your reporting policy.

Limitations
-----------
- This module does not implement new estimators; it composes existing
  estimator calls to build derived quantities.
- Reliability depends on the estimator and the effective dimension of
  the joint/conditioning spaces.
- For large networks, full multi-variable quantities may be infeasible;
  consider sparse/parent-set approximations.
"""

from on_Model.InfoDyn_lib.Estimators import Estimator_Basics 
from on_Model.InfoDyn_lib.Estimators import Simple_Binning
#from InfoDyn_lib.Estimators import KSG

class An_Additional_Information_Variable_BIN(Simple_Binning.Estimator):
	def __init__(self, Q, Dimension):
		super().__init__(Q, Dimension)
		self.Source.Analysis = ""
		
		self.Name = ""
		self.Value = {}
		
	def Estimate_the_Variable(self):
		pass
		
	def Save_the_Variable(self, Save_Directory, Simulation_Time):
		if self.Source.Analysis != "Realtime":
			return
		save_file = open(Save_Directory + self.Name + ".txt",'a')
		save_file.write("%03d: "%(Simulation_Time))
		for val in self.Value:
			save_file.write("%0.3f|"%(self.Value[val]))
		save_file.write("\n")
		save_file.close()

class H_XYZ(An_Additional_Information_Variable_BIN):
	def __init__(self, Q, Index_Tuple):
		super().__init__(Q, 3)
		self.Source.Analysis = "Realtime"
		self.Source.Type = "not_Pairwise"
		
		self.Name = "H_%s%s%s"%Index_Tuple
		self.Source.Variable_Names = Index_Tuple
		
	def Estimate_the_Variable(self):	
		self.Value["H"] = self.Conditional_Entropy(For = self.Source.Variable_Names)
		return
		
		
class H_XYZW(An_Additional_Information_Variable_BIN):
	def __init__(self, Q, Index_Tuple):
		super().__init__(Q, 4)
		self.Source.Analysis = "Realtime"
		self.Source.Type = "not_Pairwise"
		
		self.Name = "H_%s%s%s%s"%Index_Tuple
		self.Source.Variable_Names = Index_Tuple
		
	def Estimate_the_Variable(self):	
		self.Value["H"] = self.Conditional_Entropy(For = self.Source.Variable_Names)
		return
		
class T2(An_Additional_Information_Variable_BIN):
	def __init__(self, Q, Index_Tuple): # Index_Tuple = (X, Y, Ext)
		super().__init__(Q, 5)
		self.Source.Analysis = "Realtime"
		self.Source.Type = "not_Pairwise"
		
		self.Name = "Multiple_Transfer_Entropy_%s_%s_%s"%Index_Tuple
		self.Source.Variable_Names = list(Index_Tuple) + [Index_Tuple[0]+"'"] + [Index_Tuple[1]+"'"]
		
	def Estimate_the_Variable(self):	
		X_t1 = self.Source.Variable_Names[0]
		Y_t1 = self.Source.Variable_Names[1]
		Ext_t1 = self.Source.Variable_Names[2]
		X_t2 = self.Source.Variable_Names[3]
		Y_t2 = self.Source.Variable_Names[4]
		# T^2_{%s %s -> %s}
		self.Value["T^2_v1"] = self.Multiple_Mutual_Information(For = [Ext_t1,X_t1,Y_t2],  Known = [Y_t1])
		self.Value["T^2_v2"] = self.Multiple_Mutual_Information(For = [Ext_t1,X_t2,Y_t2],  Known = [X_t1,Y_t1])
		self.Value["T^2_v3"] = self.Multiple_Mutual_Information(For = [Ext_t1,Y_t1,X_t2],  Known = [X_t1])
		return
		

		

