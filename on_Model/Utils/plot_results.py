"""
plot_results.py
---------------

Plot time-series outputs produced by on_Model/004_ABN_for_GRN simulations.

Expected files (default directory: ./Temporal_Results/):
  - Simulation_Properties.txt
  - Node_<NODE>.txt                    lines: "TTT:val1|val2|"
  - Link_<U>_<V>.txt                   lines: "TTT:+v| -v| ... |"
  - (optional) any extra variable file lines: "TTT: v|v|v|"

Usage examples:
  python plot_results.py --dir ./Temporal_Results --link B1 A --show
  python plot_results.py --dir ./Temporal_Results --node A --show
  python plot_results.py --dir ./Temporal_Results --link B1 A --keys MI TE1 rTE1 --save link_B1_A.png
"""

import argparse
import os
import re

import matplotlib.pyplot as plt


_TIME_RE = re.compile(r"^\s*(\d+)\s*:\s*(.*)\s*$")


def _parse_pipe_values(payload):
    """
    Parse "v|v|v|" or "+v|-v|..." into floats.
    Empty segments are ignored.
    """
    parts = [p.strip() for p in payload.split("|")]
    vals = []
    for p in parts:
        if not p:
            continue
        vals.append(float(p))  # float() accepts leading '+'
    return vals


def read_timeseries_generic(path):
    """
    Reads a file with lines like:
      "003: +0.123| -0.045| ..."
    Returns:
      times: [3, ...]
      rows:  [[0.123, -0.045, ...], ...]
    """
    times = []
    rows = []

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            m = _TIME_RE.match(line)
            if not m:
                continue
            t = int(m.group(1))
            payload = m.group(2)
            vals = _parse_pipe_values(payload)
            times.append(t)
            rows.append(vals)

    return times, rows


def read_properties(path):
    props = {}
    if not os.path.exists(path):
        return props
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            props[k.strip()] = v.strip()
    return props


def default_link_keys():
    var_keys = ["MI","TE1","rTE1","TE2","rTE2",]
    alpha_keys = ["2","3_1","3_2","4_1","4_2","5","6_1","6_2","3_1_I","3_2_I","4_1_I","4_2_I","5_I","6_1_I","6_2_I"]

    return var_keys + alpha_keys
	
def default_node_keys():
    var_keys = ["H0","H0'"]
    alpha_keys = ["1","1_p1","1_p2","partial1"]
    
    return var_keys + alpha_keys

def link_keys_for_paper(u, v):
    var_keys = [r'$I_{'+u+':'+v+'}$', r'$T_{'+v+r' \to '+u+'}$', r'$rT_{'+v+r' \to '+u+'}$', r'$T_{'+u+r' \to '+v+'}$', r'$rT_{'+u+r' \to '+v+'}$']
    alpha_keys = [r'$\alpha_{2}^{'+u+r' '+v+'}$',r'$\alpha_{3}^{'+v+r' \to '+u+'}$',r'$\alpha_{3}^{'+u+r' \to '+v+'}$',r'$\alpha_{4}^{'+u+'}$',r'$\alpha_{4}^{'+v+'}$',r'$\alpha_{5}^{'+u+' '+v+'}$',r'$\alpha_{6}^{'+v+r' \to '+u+'}$',r'$\alpha_{6}^{'+u+r' \to '+v+'}$',"3_1_I","3_2_I","4_1_I","4_2_I","5_I","6_1_I","6_2_I"]
    return var_keys + alpha_keys

def node_keys_for_paper(node):
    var_keys = [r'$H_{'+node+'}$', "H0'"]
    alpha_keys = [r'$\alpha_{1}^{'+node+'}$',"1_p1","1_p2","partial1"]
    return var_keys + alpha_keys

def load_link_series(directory, u, v, paper, keys=None):
    fname = f"Link_{u}_{v}.txt"
    path = os.path.join(directory, fname)
    t, rows = read_timeseries_generic(path)

    if keys is None:
        keys = default_link_keys()
    if paper:
        keys = link_keys_for_paper(u, v)

    series = {k: [] for k in keys}
    for vals in rows:
        for i, k in enumerate(keys):
            series[k].append(vals[i] if i < len(vals) else float("nan"))

    return t, series


def load_node_series(directory, node, paper, keys=None):
    fname = f"Node_{node}.txt"
    path = os.path.join(directory, fname)
    t, rows = read_timeseries_generic(path)
    if keys is None:
        keys = default_node_keys()
    if paper:
        keys = node_keys_for_paper(node)	
    series = {k: [] for k in keys}
    for vals in rows:
        for i, k in enumerate(keys):
            series[k].append(vals[i] if i < len(vals) else float("nan"))

    fname = f"Node_{node}_E_values.txt"
    path = os.path.join(directory, fname)
    t, rows = read_timeseries_generic(path)
    series[r'$E$'] = []
    for vals in rows:
        series[r'$E$'].append(vals[0])
    return t, series

def plot_multi_series(t, ys, title, ylabel, save=None, show=False):
    plt.figure(figsize=(9,4))
    #plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.tab20.colors)
    i = 0
    markers = ['x', 'o', '^', '*', '+']
    for name, y in ys.items():
        plt.plot(t, y, label=name, marker=markers[i%(len(markers))], markersize = 10, markerfacecolor = 'none', linewidth = 1)
        i += 1
    plt.xlabel("time (steps)")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    if save:
        plt.savefig(save, dpi=200)
    if show:
        plt.show()
    plt.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="./Temporal_Results", help="results directory")
    ap.add_argument("--node", default=None, help="node name, e.g. A or B1")
    ap.add_argument("--link", nargs=2, default=None, metavar=("U", "V"),
                    help="link endpoints, e.g. --link B1 A")
    ap.add_argument("--keys", nargs="*", default=None,
                    help="which series keys to plot (default: all available)")
    ap.add_argument("--save", default=None, help="save figure to this path (png/pdf)")
    ap.add_argument("--show", action="store_true", help="show plot window")
    ap.add_argument("--paper", action="store_true", help="save paper figures to this path (png/pdf)")
    args = ap.parse_args()

    props = read_properties(os.path.join(args.dir, "Simulation_Properties.txt"))
    model_name = props.get("Model_Name", "Simulation results")

    if args.node and args.link:
        raise SystemExit("Choose either --node or --link, not both.")
    if not args.node and not args.link:
        raise SystemExit("Provide --node NODE or --link U V.")

    if args.node:
        t, series = load_node_series(args.dir, args.node, args.paper)
        if args.paper:
            keys = [r'$H_{'+args.node+'}$']
            ys = {k: series[k] for k in keys if k in series}
            title = f"Figure 3 : {model_name} | Node {args.node}"
            plot_multi_series(t, ys, title=title, ylabel="value (nats)", save="Figure3(c).png", show=args.show)

            keys = [r'$\alpha_{1}^{'+args.node+'}$',r'$E$']
            ys = {k: series[k] for k in keys if k in series}
            title = f"Figure 3 : {model_name} | Node {args.node}"
            plot_multi_series(t, ys, title=title, ylabel="value (nats)", save="Figure3(d).png", show=args.show)

        keys = args.keys or list(series.keys())
        ys = {k: series[k] for k in keys if k in series}
        title = f"{model_name} | Node {args.node}"
        plot_multi_series(t, ys, title=title, ylabel="value (nats)", save=args.save, show=args.show)
        return

    u, v = args.link
    t, series = load_link_series(args.dir, u, v, args.paper)
    if args.paper:
        keys = [r'$I_{'+u+':'+v+'}$', r'$T_{'+v+r' \to '+u+'}$', r'$rT_{'+v+r' \to '+u+'}$', r'$T_{'+u+r' \to '+v+'}$', r'$rT_{'+u+r' \to '+v+'}$']
        ys = {k: series[k] for k in keys if k in series}
        title = f"Figure 3 : {model_name} | Link {u}–{v}"
        plot_multi_series(t, ys, title=title, ylabel="value (nats)", save="Figure3(a).png", show=args.show)

        keys = [r'$\alpha_{2}^{'+u+r' '+v+'}$',r'$\alpha_{3}^{'+v+r' \to '+u+'}$',r'$\alpha_{3}^{'+u+r' \to '+v+'}$',r'$\alpha_{4}^{'+u+'}$',r'$\alpha_{4}^{'+v+'}$',r'$\alpha_{5}^{'+u+' '+v+'}$',r'$\alpha_{6}^{'+v+r' \to '+u+'}$',r'$\alpha_{6}^{'+u+r' \to '+v+'}$']
        ys = {k: series[k] for k in keys if k in series}
        title = f"Figure 3 : {model_name} | Link {u}–{v}"
        plot_multi_series(t, ys, title=title, ylabel="value (nats)", save="Figure3(b).png", show=args.show)

    keys = args.keys or list(series.keys())
    ys = {k: series[k] for k in keys if k in series}
    title = f"{model_name} | Link {u}–{v}"
    plot_multi_series(t, ys, title=title, ylabel="value (nats)", save=args.save, show=args.show)


if __name__ == "__main__":
    main()
