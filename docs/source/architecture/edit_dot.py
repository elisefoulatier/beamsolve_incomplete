import re

# ── Configuration ──────────────────────────────────────────────────────────────

INPUT  = "classes_beamsolve.dot"
OUTPUT = f"{INPUT[:-4]}_edited.dot"

# Map: substring in node name → fillcolor
COLOR_MAP = {
    # beam module
    "beam.Beam"                              : "lightblue",
    # FEM module
    "fem_model.FEMModel"                     : "lightblue",
    "solver.FEMSolution"                     : "lightgreen",
    # Analytical module
    "analytical_model.AnalyticalModel"       : "lightblue",
    "analytical_model.AnalyticalSolution"    : "lightgreen",
    # visualisation (both modules)
    "visualisation"                          : "lightyellow",
}

# Clusters: cluster label → list of substrings identifying member nodes
CLUSTERS = {
    "Beam": [
        "beam.Beam",
    ],
    "FEM": [
        "fem_model.FEMModel",
        "solver.FEMSolution",
        "FEM.visualisation",
    ],
    "Analytical": [
        "analytical_model.AnalyticalModel",
        "analytical_model.AnalyticalSolution",
        "Analytical.visualisation",
    ],
}

# ── Read ───────────────────────────────────────────────────────────────────────

with open(INPUT, "r", encoding="utf-8") as f:
    content = f.read()

# ── 1. Fix graph name ──────────────────────────────────────────────────────────

content = re.sub(r'digraph "[^"]*"', 'digraph "classes_beamsolve"', content)

# ── 2. Inject global graph settings ───────────────────────────────────────────

global_settings = """rankdir=BT;
splines="curved";
nodesep=0.5;
ranksep=0.75;
charset="utf-8";
fontname="Courier New";
node [fontname="Courier New"];
edge [fontname="Courier New", color="gray", fontcolor="gray", fontsize=10];"""

content = re.sub(r'rankdir=BT\s*\ncharset="utf-8"', global_settings, content)

# ── 3. Add fillcolor and style="filled" to each node ──────────────────────────

def patch_node(match):
    node_id = match.group(1)
    attrs   = match.group(2)
    color   = "white"   # default
    for key, val in COLOR_MAP.items():
        if key in node_id:
            color = val
            break
    attrs = attrs.replace('style="solid"', f'style="filled", fillcolor="{color}"')
    return f'"{node_id}" [{attrs}]'

content = re.sub(
    r'"([^"]+)"\s*\[([^\]]*(?:\[[^\]]*(?:\[[^\]]*\][^\]]*)*\][^\]]*)*)\](?=;)',
    patch_node,
    content
)

# ── 4. Patch edge styles ───────────────────────────────────────────────────────

def patch_edge(match):
    src    = match.group(1)
    dst    = match.group(2)
    label  = re.search(r'label="([^"]*)"', match.group(3))
    xlabel = f'xlabel="{label.group(1)}"' if label else ''
    return f'"{src}" -> "{dst}" [arrowhead="normal", arrowtail="none", {xlabel}];'

content = re.sub(
    r'"([^"]+)"\s*->\s*"([^"]+)"\s*\[([^\]]+)\];',
    patch_edge,
    content
)

# ── 5. Inject subgraph clusters before closing brace ──────────────────────────

clusters_dot = ""
for label, members in CLUSTERS.items():
    cluster_name = label.lower().replace(" ", "_")
    seen       = set()
    node_lines = []
    for substring in members:
        for n in re.findall(r'"([^"]+)"', content):
            if substring in n and n not in seen:
                seen.add(n)
                node_lines.append(f'"{n}"')
    if node_lines:
        nodes = "\n    ".join(node_lines)
        clusters_dot += f"""
  subgraph cluster_{cluster_name} {{
    label="{label}";
    labelloc="b";
    style="dashed";
    color="gray";
    {nodes}
  }}
"""

content = content.rstrip("}\n") + clusters_dot + "\n}\n"

# ── 6. Truncate long method signatures ────────────────────────────────────────

def truncate_methods(match):
    label = match.group(0)
    def shorten(m):
        method = m.group(0)
        if len(method) > 50:
            name = method.split('(')[0]
            return name + '(...)<br ALIGN="LEFT"/>'
        return method
    return re.sub(r'\w+\([^<]*\)<br ALIGN="LEFT"/>', shorten, label)

content = re.sub(r'<\{[^}]+\}>', truncate_methods, content)

# ── Write ──────────────────────────────────────────────────────────────────────

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Patched {INPUT} → {OUTPUT}")
print(f"Now run:")
print(f"  dot -Tsvg {OUTPUT} -o ../_static/architecture/classes_beamsolve.svg")
