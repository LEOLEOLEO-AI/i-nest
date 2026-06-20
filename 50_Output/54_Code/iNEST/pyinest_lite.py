# PyiNEST-Lite SDK - Core API Design
# ===================================
# Target: D:\iNEST\Write\Code\SDI\pyinest_lite\
# Python SDK for iNEST topology generation, simulation, and analysis.
# Serves as the user-facing API layer (L4 in iNEST 4-layer stack).

__version__ = "0.1.0"
__all__ = ["Topology", "Simulator", "Metrics", "Visualizer"]

from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path
import json


# ═══════════════════════════════════════════════════════════════
# Core Data Types
# ═══════════════════════════════════════════════════════════════

@dataclass
class TopologyConfig:
    """Configuration for generating SDI chiplet topologies."""
    n_chiplets: int = 64
    ports_per_chiplet: int = 16
    target_sigma: float = 4.0
    seed: int = 42
    topology_type: str = "watts-strogatz"  # ws | clusters | ring | star
    rewiring_p: float = 0.1
    cluster_size: int = 8
    cluster_density: float = 0.9
    inter_cluster_prob: float = 0.02


@dataclass
class MetricsReport:
    """Standardized metrics output from a topology or simulation."""
    n_nodes: int
    n_edges: int
    avg_degree: float
    clustering_coefficient: float
    avg_shortest_path: float
    global_efficiency: float
    small_world_sigma: float
    structured_efficiency: float  # C * E_glob
    degree_distribution: Dict[int, int] = field(default_factory=dict)
    is_small_world: bool = False  # sigma >= 1.0
    is_superlinear_capable: bool = False  # sigma >= 4.0


@dataclass
class SimulationConfig:
    """Configuration for running a network simulation."""
    duration_ms: float = 100.0
    dt_ms: float = 0.1
    temperature: float = 300.0
    pressure_pa: float = 0.0
    volume_m3: float = 0.0
    learning_rate: float = 1e-6
    evolution_enabled: bool = True
    evolution_threshold: int = 50
    prune_threshold: float = 1e-7
    regen_ratio: float = 0.01
    mutation_prob: float = 0.01
    mutation_sigma: float = 1e-7


@dataclass
class SimulationResult:
    """Results from a single simulation run."""
    efe: float  # Expected Free Energy
    gibbs_free_energy: float
    pv_work: float
    superlinear_slope: float  # alpha
    chaos_sync_error: float  # epsilon
    topology_entropy: float
    clustering: float
    path_length: float
    state: str  # idle | explore | select | stabilize
    evolution_metrics: Dict[str, Any] = field(default_factory=dict)


# ═══════════════════════════════════════════════════════════════
# Topology Module
# ═══════════════════════════════════════════════════════════════

class Topology:
    """Generate and analyze SDI network topologies.

    Usage:
        topo = Topology(TopologyConfig(n_chiplets=128))
        adj, metrics = topo.generate()
        print(f"sigma={metrics.small_world_sigma:.2f}")
    """

    def __init__(self, config: TopologyConfig = None):
        self.config = config or TopologyConfig()

    def generate(self) -> Tuple[List[List[int]], MetricsReport]:
        """Generate topology and compute metrics."""
        cfg = self.config
        adj = self._generate_topology(cfg)
        metrics = self._compute_metrics(adj)
        return adj, metrics

    def scan_sigma(self, p_range: List[float] = None) -> List[Dict]:
        """Scan rewiring probability p to map sigma landscape."""
        if p_range is None:
            p_range = [0.001, 0.005, 0.01, 0.02, 0.03, 0.05, 0.08, 0.10,
                       0.12, 0.15, 0.18, 0.20, 0.25, 0.30, 0.40, 0.50]
        results = []
        for p in p_range:
            cfg = TopologyConfig(**{**self.config.__dict__, "rewiring_p": p})
            adj = self._generate_topology(cfg)
            m = self._compute_metrics(adj)
            results.append({"p": p, "sigma": m.small_world_sigma,
                           "C": m.clustering_coefficient,
                           "L": m.avg_shortest_path,
                           "S_eff": m.structured_efficiency})
        return results

    def find_minimum_scale(self, sigma_target: float = 4.0,
                           n_range: List[int] = None) -> int:
        """Find minimum N achieving target sigma."""
        if n_range is None:
            n_range = [16, 32, 48, 64, 96, 128, 192, 256, 384, 512, 768, 1024]
        for N in n_range:
            cfg = TopologyConfig(**{**self.config.__dict__, "n_chiplets": N})
            adj = self._generate_topology(cfg)
            m = self._compute_metrics(adj)
            if m.small_world_sigma >= sigma_target:
                return N
        return n_range[-1]

    def _generate_topology(self, cfg: TopologyConfig) -> List[List[int]]:
        # Delegate to topology engine (from sdi_sim.topology)
        from sdi_sim.topology import watts_strogatz, functional_clusters, build_sdi_topology
        if cfg.topology_type == "clusters":
            return functional_clusters(cfg.n_chiplets, cfg.cluster_size,
                                       cfg.cluster_density, cfg.inter_cluster_prob,
                                       cfg.seed)
        elif cfg.topology_type == "ws":
            return watts_strogatz(cfg.n_chiplets, cfg.ports_per_chiplet,
                                  cfg.rewiring_p, cfg.seed)
        else:
            adj, _ = build_sdi_topology(cfg.n_chiplets, cfg.target_sigma,
                                        cfg.ports_per_chiplet, cfg.seed)
            return adj

    def _compute_metrics(self, adj: List[List[int]]) -> MetricsReport:
        from sdi_sim.topology import (clustering_coefficient, avg_shortest_path,
                                       global_efficiency, small_world_sigma,
                                       degree_distribution)
        n = len(adj)
        edges = sum(len(s) for s in adj) // 2
        C = clustering_coefficient(adj)
        L = avg_shortest_path(adj)
        E = global_efficiency(adj)
        sigma = small_world_sigma(adj, n_rand=n, k_rand=edges * 2 // n)
        se = C * E
        dd = degree_distribution(adj)

        return MetricsReport(
            n_nodes=n, n_edges=edges, avg_degree=edges * 2 / n,
            clustering_coefficient=C, avg_shortest_path=L,
            global_efficiency=E, small_world_sigma=sigma,
            structured_efficiency=se, degree_distribution=dd,
            is_small_world=(sigma >= 1.0),
            is_superlinear_capable=(sigma >= 4.0),
        )


# ═══════════════════════════════════════════════════════════════
# Simulator Module
# ═══════════════════════════════════════════════════════════════

class Simulator:
    """Run FEP-based memristor network simulations.

    Usage:
        sim = Simulator(SimulationConfig(duration_ms=100))
        result = sim.run(adjacency_list)
    """

    def __init__(self, config: SimulationConfig = None):
        self.config = config or SimulationConfig()

    def run(self, adj: List[List[int]]) -> SimulationResult:
        """Run one simulation on the given topology."""
        # This delegates to memai.run.simulate()
        cfg_dict = {
            "rows": len(adj), "cols": len(adj),
            "bits": 4, "temperature": self.config.temperature,
            "pressure_pa": self.config.pressure_pa,
            "volume_m3": self.config.volume_m3,
            "fail_threshold": self.config.evolution_threshold,
            "prune_threshold": self.config.prune_threshold,
            "regen_ratio": self.config.regen_ratio,
            "mutation_prob": self.config.mutation_prob,
            "mutation_sigma": self.config.mutation_sigma,
        }
        # Placeholder: integrate with memai.run
        return SimulationResult(
            efe=0.0, gibbs_free_energy=0.0, pv_work=0.0,
            superlinear_slope=0.0, chaos_sync_error=0.0,
            topology_entropy=0.0, clustering=0.0, path_length=0.0,
            state="idle",
        )

    def scan_phase(self, adj: List[List[int]],
                   temperature_range: List[float] = None) -> List[Dict]:
        """Scan temperature to find phase transition."""
        if temperature_range is None:
            temperature_range = [100, 150, 200, 250, 280, 290, 300, 310, 320, 350, 400, 500]
        results = []
        for T in temperature_range:
            cfg = SimulationConfig(**{**self.config.__dict__, "temperature": T})
            sim = Simulator(cfg)
            r = sim.run(adj)
            results.append({"T": T, "EFE": r.efe, "G": r.gibbs_free_energy,
                           "alpha": r.superlinear_slope, "epsilon": r.chaos_sync_error})
        return results


# ═══════════════════════════════════════════════════════════════
# Visualizer Module (stub)
# ═══════════════════════════════════════════════════════════════

class Visualizer:
    """Visualize topologies and simulation results.

    Usage:
        viz = Visualizer()
        viz.plot_sigma_scan(scan_results)
        viz.save("output.png")
    """

    def __init__(self):
        self.figures = []

    def plot_sigma_scan(self, results: List[Dict],
                        title: str = "Sigma vs Rewiring Probability") -> Any:
        """Plot sigma landscape."""
        # Requires matplotlib
        try:
            import matplotlib.pyplot as plt
            ps = [r["p"] for r in results]
            sigmas = [r["sigma"] for r in results]
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(ps, sigmas, "b-", linewidth=2, label="sigma")
            ax.axhline(y=4.0, color="r", linestyle="--", label="sigma=4.0 target")
            ax.set_xlabel("Rewiring probability p")
            ax.set_ylabel("Small-world coefficient sigma")
            ax.set_title(title)
            ax.legend()
            ax.grid(True, alpha=0.3)
            self.figures.append(fig)
            return fig
        except ImportError:
            return None

    def save(self, path: str) -> None:
        """Save the last figure."""
        if self.figures:
            self.figures[-1].savefig(path, dpi=150, bbox_inches="tight")


# ═══════════════════════════════════════════════════════════════
# Quick Start
# ═══════════════════════════════════════════════════════════════

def quick_start():
    """Minimal example demonstrating the full PyiNEST-Lite pipeline."""
    print("PyiNEST-Lite v" + __version__)
    print("=" * 60)

    # Step 1: Generate topology
    config = TopologyConfig(n_chiplets=128, target_sigma=4.0)
    topo = Topology(config)

    print(f"Generating topology: N={config.n_chiplets}, target sigma={config.target_sigma}")
    adj, metrics = topo.generate()
    print(f"  sigma={metrics.small_world_sigma:.2f}, C={metrics.clustering_coefficient:.4f}, "
          f"L={metrics.avg_shortest_path:.2f}")
    print(f"  structured_eff={metrics.structured_efficiency:.4f}, "
          f"superlinear_capable={metrics.is_superlinear_capable}")

    # Step 2: Find minimum scale
    min_n = topo.find_minimum_scale(sigma_target=4.0)
    print(f"Minimum scale for sigma>=4.0: N={min_n}")

    # Step 3: Scan sigma landscape
    scan = topo.scan_sigma()
    peak = max(scan, key=lambda r: r["sigma"])
    print(f"Sigma landscape: range=[{scan[0]['sigma']:.2f}, {scan[-1]['sigma']:.2f}], "
          f"peak={peak['sigma']:.2f} at p={peak['p']:.3f}")

    print("Done.")
    return adj, metrics, scan


if __name__ == "__main__":
    adj, metrics, scan = quick_start()
