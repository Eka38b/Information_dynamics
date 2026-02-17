"""
From_Simple_Bin.py
------------------

Minimal utilities for constructing empirical probability distributions from
discrete count histograms ("simple binning").

Role in the pipeline
--------------------
Simulation code produces count tables (histograms) over tuples of discrete
variables. This module provides a lightweight wrapper to:

- Marginalize a histogram by selecting a subset of variables
- Normalize counts to a probability distribution function (PDF)

Key Abstractions
----------------
- Source(Statistics, Variable_Names)
    - Statistics:
        dict mapping an n-tuple (case) -> count
    - Variable_Names:
        sequence of names labeling the tuple coordinates
    - Generate_Desired_PDF(List_of_Mesh_Variables):
        returns a normalized PDF for the marginal distribution over the
        specified variables (in the order provided)

Notes
-----
- If the total count is zero, an exception is raised to prevent invalid PDFs.
- This module is intentionally small and explicit to support reproducibility.
"""

import math

class Source(object):
	def __init__(self, Statistics, Variable_Names):
		self.Statistics = Statistics
		self.Variable_Names = Variable_Names

	def Meshed_for_(self, List_of_Mesh_Variables):
		if List_of_Mesh_Variables == []:
			return self.Statistics

		Mesh_Index = []
		for Mesh_Var in List_of_Mesh_Variables:
			Mesh_Index.append(self.Variable_Names.index(Mesh_Var))

		Meshed_Statistics = {}
		for a_Case in self.Statistics:
			mesh_case = self.Mesh_Tuple(a_Case, Mesh_Index)
			if mesh_case in Meshed_Statistics:
				Meshed_Statistics[mesh_case] += self.Statistics[a_Case]
			else:
				Meshed_Statistics[mesh_case] = self.Statistics[a_Case]
		return Meshed_Statistics

	def Mesh_Tuple(self, Raw_Tuple, Mesh_Index):
		Result = []
		for index in Mesh_Index :
			Result.append(Raw_Tuple[index])
		return tuple(Result)

	def Generate_Probability_Distribution_Function(self, Statistics):
		Total = self.Calculate_Total_Occurance(Statistics)
		PDF = {}
		for a_Case in Statistics:
			PDF[a_Case] = Statistics[a_Case]/Total
		return PDF

	def Generate_Desired_PDF(self, List_of_Mesh_Variables):
		return self.Generate_Probability_Distribution_Function(self.Meshed_for_(List_of_Mesh_Variables))

	def Calculate_Total_Occurance(self, Statistics):
		Total = 0
		for a_Case in Statistics:
			Total += Statistics[a_Case]
		if Total == 0:
			raise ValueError("Zero total occurrence in statistics")
		return Total
	


		

