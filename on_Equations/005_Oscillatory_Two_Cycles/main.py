
import matplotlib.pyplot as plt

from Core import Information_Dynamic_Equation


class ID_of_Two_Cycles(Information_Dynamic_Equation.Information_Dynamics):
    def __init__(self, sim_time=400, kappa=0.001, clip_E=0.006):
        super().__init__()
        
        self.Simulation_Time_Limit = sim_time
        self.kappa = kappa
        self.clip_E = clip_E
        
        self.Save_Directory = "./on_Equations/005_Oscillatory_Two_Cycles/Temporal_Results/"
        
        self.Initialize()
        self.Generate_Data()

    def Register_Properties(self):
        self.Properties["Simulation_Time_Limit"] = str(self.Simulation_Time_Limit)
        self.Properties["kappa"] = str(self.kappa)
        self.Properties["clip_E"] = str(self.clip_E)
        self.Register_Topology()

    def Set_Topology(self):
        self.Info_Network.Set_Nodes(["A1", "A2", "A3", "A4", "B1", "B2", "B3", "B4"])
        for link in [
            ("A1","A2"), ("A2","A3"), ("A3","A4"), ("A4","A1"),
            ("B1","B2"), ("B2","B3"), ("B3","B4"), ("B4","B1"),
            ("A2","B2"), ("B4","A4")
        ]:
            self.Info_Network.Add_a_Link(link)

    def Set_Blocking_Flows_Condition(self):
        self.Blocked_Flows = [
            ("A2","A1"), ("A3","A2"), ("A4","A3"), ("A1","A4"),
            ("B2","B1"), ("B3","B2"), ("B4","B3"), ("B1","B4"),
            ("B2","A2"), ("A4","B4")
        ]

    def Set_Initial_Conditions(self):
        for node in self.Info_Network.Nodes:
            self.Info_Network.Nodes[node].Var_["H0"][0] = 0.60

        amplitudes = {
            ("A1","A2"): 0.112,
            ("A2","A3"): 0.112,
            ("A3","A4"): 0.112,
            ("A4","A1"): 0.112,
            ("B1","B2"): 0.108,
            ("B2","B3"): 0.108,
            ("B3","B4"): 0.108,
            ("B4","B1"): 0.108,
            ("A2","B2"): 0.018,
            ("B4","A4"): 0.018,
        }

        for link in self.Info_Network.Links:
            L = self.Info_Network.Links[link]
            L.Var_["MI"][0] = 0.46
            L.Var_["TE1"][0] = 0.0
            L.Var_["rTE2"][0] = 0.0
            L.Var_["TE2"][0] = amplitudes[link]
            L.Var_["rTE1"][0] = amplitudes[link]

    def Set_Overall_Alphas_and_E(self):
        for t in range(self.Simulation_Time_Limit + 1):
            for link in self.Info_Network.Links:
                self.Info_Network.Links[link].Alpha_["2"][t] = 0.0
                self.Info_Network.Links[link].Alpha_["3_1"][t] = 0.0
                self.Info_Network.Links[link].Alpha_["3_2"][t] = 0.0
                self.Info_Network.Links[link].Alpha_["6_1"][t] = 0.0
                self.Info_Network.Links[link].Alpha_["6_2"][t] = 0.0
            for node in self.Info_Network.Nodes:
                self.Info_Network.Nodes[node].Alpha_["1"][t] = 0.0
                self.Info_Network.Nodes[node].Var_["E"][t] = 0.0

    def Set_Realtime_Alphas_and_E(self, t):
        A_cycle = [("A1","A2"), ("A2","A3"), ("A3","A4"), ("A4","A1")]
        B_cycle = [("B1","B2"), ("B2","B3"), ("B3","B4"), ("B4","B1")]

        A_te = sum(self.Info_Network.Links[l].Var_["TE2"][t] for l in A_cycle) / len(A_cycle)
        B_te = sum(self.Info_Network.Links[l].Var_["TE2"][t] for l in B_cycle) / len(B_cycle)
        A_rte = sum(self.Info_Network.Links[l].Var_["rTE1"][t] for l in A_cycle) / len(A_cycle)
        B_rte = sum(self.Info_Network.Links[l].Var_["rTE1"][t] for l in B_cycle) / len(B_cycle)

        delta = 0.5 * ((A_te + A_rte) - (B_te + B_rte))
        g = max(-self.clip_E, min(self.clip_E, self.kappa * delta))

        self.Info_Network.Nodes["B2"].Var_["E"][t] =  g
        self.Info_Network.Nodes["A2"].Var_["E"][t] = -g
        self.Info_Network.Nodes["B4"].Var_["E"][t] =  g
        self.Info_Network.Nodes["A4"].Var_["E"][t] = -g


def cycle_df(model, cycle_links):
    cycle_avg = {"time":[],"MI":[],"TE":[],"rTE":[],"E":[]}
    for t in range(model.Simulation_Time_Limit + 1):
        cycle_avg["time"].append(t)
        cycle_avg["MI"].append(sum(model.Info_Network.Links[l].Var_["MI"][t] for l in cycle_links) / len(cycle_links))
        cycle_avg["TE"].append(sum(model.Info_Network.Links[l].Var_["TE2"][t] for l in cycle_links) / len(cycle_links))
        cycle_avg["rTE"].append(sum(model.Info_Network.Links[l].Var_["rTE1"][t] for l in cycle_links) / len(cycle_links))
        cycle_avg["E"].append(model.Info_Network.Nodes["B2"].Var_["E"][t])

    return cycle_avg

if __name__ == "__main__":
    TEST = ID_of_Two_Cycles()
    A_cycle = [("A1","A2"), ("A2","A3"), ("A3","A4"), ("A4","A1")]
    B_cycle = [("B1","B2"), ("B2","B3"), ("B3","B4"), ("B4","B1")]
    A_df = cycle_df(TEST, A_cycle)
    B_df = cycle_df(TEST, B_cycle)
    
    plt.figure(figsize=(9,5.5))
    plt.plot(A_df["time"], A_df["TE"], label="Cycle A mean TE")
    plt.plot(B_df["time"], B_df["TE"], label="Cycle B mean TE")
    plt.plot(A_df["time"], A_df["rTE"], label="Cycle A mean rTE")
    plt.plot(B_df["time"], B_df["rTE"], label="Cycle B mean rTE")
    plt.xlabel("time"); plt.ylabel("TE, rTE")
    plt.title(f"Cycle-average paired feedback E: TE and rTE (kappa={TEST.kappa}, clip={TEST.clip_E})")
    plt.legend(); plt.tight_layout()
    plt.savefig(TEST.Save_Directory+"TE_rTE.png")
    plt.close()


    plt.figure(figsize=(9,5.5))
    plt.plot(A_df["time"], A_df["MI"], label="Cycle A mean MI")
    plt.plot(B_df["time"], B_df["MI"], label="Cycle B mean MI")
    plt.xlabel("time"); plt.ylabel("MI")
    plt.title(f"Cycle-average paired feedback E: MI (kappa={TEST.kappa}, clip={TEST.clip_E})")
    plt.legend(); plt.tight_layout()
    plt.savefig(TEST.Save_Directory+"MI.png")
    plt.close()
    
    
    plt.figure(figsize=(9,5.5))
    plt.plot(A_df["time"], A_df["E"], label="E(B2)")
    plt.xlabel("time"); plt.ylabel("E")
    plt.title(f"Cycle-average paired feedback E: E (kappa={TEST.kappa}, clip={TEST.clip_E})")
    plt.legend(); plt.tight_layout()
    plt.savefig(TEST.Save_Directory+"E.png")
    plt.close()

