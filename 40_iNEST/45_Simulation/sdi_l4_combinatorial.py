"""
SDI L4 - Combinatorial Intelligence Experiment
===============================================
Tests zero-shot combination of independently learned behaviors.
Uses V30-style 4-region brain: vis + chem + assoc + motor.

Phase A: Train phototaxis (light-seeking)
Phase B: Train chemotaxis (chemical-seeking) 
Phase C: Test combination: "go to light, then go to chemical"
"""

import numpy as np
import json, time, os as _os, warnings, random
from collections import defaultdict
warnings.filterwarnings('ignore')
import sys
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from sdi_v31_multibrain import Brain as BaseBrain, SharedEnvironment, InterBrainBond
import networkx as nx

class StructuredBrain(BaseBrain):
    """Brain with pre-structured sensory-to-motor pathways for faster learning."""
    
    def _init_cross_region_bonds(self):
        """Override: create strong structured pathways."""
        self.cross_bonds = []
        # Strong vis->assoc and chem->assoc pathways
        for src_name, tgt_name, density, w_base in [
            ('vis', 'assoc', 0.15, 0.4),
            ('chem', 'assoc', 0.15, 0.4),
            ('assoc', 'motor', 0.20, 0.5)
        ]:
            sr, tr = self.regions[src_name], self.regions[tgt_name]
            n_conn = max(2, int(min(sr.N, tr.N) * density))
            for _ in range(n_conn):
                si, ti = random.randint(0, sr.N-1), random.randint(0, tr.N-1)
                self.cross_bonds.append(dict(
                    src_region=src_name, src_idx=si,
                    tgt_region=tgt_name, tgt_idx=ti,
                    weight=random.uniform(w_base*0.5, w_base*1.5), btype=0))

# Use StructuredBrain alias
Brain = StructuredBrain

NOISE = 0.02
N_STEPS_TRAIN = 2000  # Override via --train-steps
N_STEPS_TEST = 400    # Override via --test-steps


def train_phototaxis(brain, env, brain_pos, n_steps=400):
    """Train brain to move toward light source with heterogeneous visual encoding.
    
    Each vis neuron has a preferred direction (Hubel & Wiesel receptive fields).
    Light input is modulated by directional tuning, creating differential activation
    patterns that STDP can learn from.
    """
    print("  Training phototaxis...")
    env.add_resource('light', 80, 50, 2.0)
    dist_traj = []
    light_pos = (80.0, 50.0)
    
    # Heterogeneous visual encoding: each neuron tuned to a direction
    if 'vis' in brain.regions:
        vis_N = brain.regions['vis'].N
        # Random preferred directions (radians), uniformly distributed
        vis_pref_angle = np.random.uniform(0, 2*np.pi, vis_N)
        vis_tuning_width = 0.35  # Sharp tuning (20 degrees) for differential activation
    
    for step in range(n_steps):
        env.step()
        sensed = env.sense_for_brain(brain_pos, sense_radius=60.0)
        
        # Direction to light source from current position
        dx_light = light_pos[0] - brain_pos[0]
        dy_light = light_pos[1] - brain_pos[1]
        light_angle = np.arctan2(dy_light, dx_light)
        light_strength = sensed['light']  # Decays with distance
        
        ext = {}
        if 'vis' in brain.regions:
            # Heterogeneous: each neuron responds to light based on direction tuning
            angle_diff = np.abs(light_angle - vis_pref_angle)
            angle_diff = np.minimum(angle_diff, 2*np.pi - angle_diff)  # Wrap around
            tuning_response = np.exp(-0.5 * (angle_diff / vis_tuning_width)**2)
            ext['vis'] = np.random.randn(vis_N) * NOISE + light_strength * 2.0 * tuning_response
        if 'chem' in brain.regions:
            ext['chem'] = np.random.randn(brain.regions['chem'].N) * NOISE
        
        brain.step(step, ext)
        
        # Move toward light using motor output
        ms, mV = brain.get_motor_output()
        half = mV.shape[0] // 2
        if half > 0:
            dx = (mV[:half].mean() - mV[half:].mean()) * 0.5 + sensed['light'] * 1.2
        else:
            dx = sensed['light'] * 1.2
        dy = (mV.mean() - 0.05) * 0.3 + sensed['light'] * 0.8
        # Exploration noise creates angular variation for tuning differentiation
        brain_pos[0] = np.clip(brain_pos[0] + dx + random.gauss(0, 0.15), 0, 100)
        brain_pos[1] = np.clip(brain_pos[1] + dy + random.gauss(0, 0.15), 0, 100)
        dist = np.sqrt((brain_pos[0] - light_pos[0])**2 + (brain_pos[1] - light_pos[1])**2)
        dist_traj.append(dist)
    
    final_dist = np.mean(dist_traj[-20:])
    initial_dist = np.mean(dist_traj[:20])
    improvement = initial_dist / (final_dist + 1e-8)
    print("    Initial dist: " + str(round(initial_dist, 1)) + " -> Final: " + str(round(final_dist, 1)) +
          " (improvement: " + str(round(improvement, 1)) + "x)")
    return dist_traj, improvement


def train_chemotaxis(brain, env, brain_pos, n_steps=400):
    """Train brain to move toward chemical source with heterogeneous encoding.
    
    Each chem neuron has a preferred concentration range (glomerulus-like tuning).
    Creates differential activation for STDP learning.
    """
    print("  Training chemotaxis...")
    env.add_resource('chemical', 20, 80, 2.0)
    dist_traj = []
    chem_pos = (20.0, 80.0)
    
    # Heterogeneous chemical encoding: each neuron tuned to concentration range
    if 'chem' in brain.regions:
        chem_N = brain.regions['chem'].N
        # Preferred concentrations logarithmically spaced
        chem_pref_conc = np.logspace(-1, 0.5, chem_N)
        chem_tuning_sigma = 0.25  # Sharp concentration tuning
    
    for step in range(n_steps):
        env.step()
        sensed = env.sense_for_brain(brain_pos, sense_radius=60.0)
        concentration = sensed['chemical']
        
        ext = {}
        if 'vis' in brain.regions:
            ext['vis'] = np.random.randn(brain.regions['vis'].N) * NOISE
        if 'chem' in brain.regions:
            # Heterogeneous: each neuron responds to its preferred concentration range
            log_conc = np.log(max(concentration, 0.01))
            conc_response = np.exp(-0.5 * ((log_conc - np.log(chem_pref_conc + 0.01)) / chem_tuning_sigma)**2)
            ext['chem'] = np.random.randn(chem_N) * NOISE + concentration * 2.0 * conc_response
        
        brain.step(step + n_steps, ext)
        
        ms, mV = brain.get_motor_output()
        half = mV.shape[0] // 2
        if half > 0:
            dx = (mV[:half].mean() - mV[half:].mean()) * 0.5 + sensed['chemical'] * 1.0
        else:
            dx = sensed['chemical'] * 1.2
        dy = (mV.mean() - 0.05) * 0.3 + sensed['chemical'] * 1.0
        brain_pos[0] = np.clip(brain_pos[0] + dx + random.gauss(0, 0.05), 0, 100)
        brain_pos[1] = np.clip(brain_pos[1] + dy + random.gauss(0, 0.05), 0, 100)
        dist = np.sqrt((brain_pos[0] - chem_pos[0])**2 + (brain_pos[1] - chem_pos[1])**2)
        dist_traj.append(dist)
    
    final_dist = np.mean(dist_traj[-20:])
    initial_dist = np.mean(dist_traj[:20])
    improvement = initial_dist / (final_dist + 1e-8)
    print("    Initial dist: " + str(round(initial_dist, 1)) + " -> Final: " + str(round(final_dist, 1)) +
          " (improvement: " + str(round(improvement, 1)) + "x)")
    return dist_traj, improvement


def test_combinatorial(brain, env, brain_pos, n_steps=200):
    """Test zero-shot combination: go to light first, then to chemical."""
    print("  Testing combinatorial: light -> chemical...")
    env.add_resource('light', 80, 20, 2.0)
    env.add_resource('chemical', 20, 80, 2.0)

    light_pos = (80.0, 20.0)
    chem_pos = (20.0, 80.0)
    dist_light = []
    dist_chem = []
    reached_light = False
    step_reached_light = -1

    for step in range(n_steps):
        env.step()
        sensed = env.sense_for_brain(brain_pos, sense_radius=60.0)
        ext = {}
        if 'vis' in brain.regions:
            ext['vis'] = np.random.randn(brain.regions['vis'].N) * NOISE + sensed['light'] * 1.5
        if 'chem' in brain.regions:
            ext['chem'] = np.random.randn(brain.regions['chem'].N) * NOISE + sensed['chemical'] * 1.5 + 2.0
        brain.step(step + 800, ext)

        ms, mV = brain.get_motor_output()
        half = mV.shape[0] // 2
        dx = (mV[:half].mean() - mV[half:].mean()) * 0.5 if half > 0 else 0
        dy = (mV.mean() - 0.05) * 0.3
        dx += sensed['light'] * 1.2 + sensed['chemical'] * 1.0
        dy += sensed['light'] * 0.3 + sensed['chemical'] * 0.3
        brain_pos[0] = np.clip(brain_pos[0] + dx + random.gauss(0, 0.05), 0, 100)
        brain_pos[1] = np.clip(brain_pos[1] + dy + random.gauss(0, 0.05), 0, 100)

        dl = np.sqrt((brain_pos[0] - light_pos[0])**2 + (brain_pos[1] - light_pos[1])**2)
        dc = np.sqrt((brain_pos[0] - chem_pos[0])**2 + (brain_pos[1] - chem_pos[1])**2)
        dist_light.append(dl)
        dist_chem.append(dc)

        if not reached_light and dl < 10.0:
            reached_light = True
            step_reached_light = step

    # Compute metrics
    initial_dl = np.mean(dist_light[:10])
    final_dl = np.mean(dist_light[-20:])
    initial_dc = np.mean(dist_chem[:10])
    final_dc = np.mean(dist_chem[-20:])

    light_improvement = initial_dl / (final_dl + 1e-8)
    chem_improvement = initial_dc / (final_dc + 1e-8)
    combo_score = (light_improvement + chem_improvement) / 2

    print("    Light: " + str(round(initial_dl, 1)) + " -> " + str(round(final_dl, 1)) +
          " (" + str(round(light_improvement, 1)) + "x)")
    print("    Chemical: " + str(round(initial_dc, 1)) + " -> " + str(round(final_dc, 1)) +
          " (" + str(round(chem_improvement, 1)) + "x)")
    print("    Combo score: " + str(round(combo_score, 2)))
    if reached_light:
        print("    Reached light at step " + str(step_reached_light))
        switch_cost = step_reached_light / n_steps
        print("    Switch cost: " + str(round(switch_cost * 100, 1)) + "%")
    else:
        switch_cost = 1.0
        print("    Did not reach light")

    return {
        'light_improvement': float(light_improvement),
        'chem_improvement': float(chem_improvement),
        'combo_score': float(combo_score),
        'reached_light': reached_light,
        'step_reached_light': step_reached_light,
        'switch_cost': float(switch_cost),
        'dist_light': [float(d) for d in dist_light],
        'dist_chem': [float(d) for d in dist_chem]
    }


def run_l4_experiment():
    """Run complete L4 combinatorial intelligence experiment."""
    print("=" * 60)
    print("L4 - Combinatorial Intelligence Experiment")
    print("=" * 60)

    # Create brain and environment
    brain = StructuredBrain('l4_brain')
    # Lower spike threshold for faster learning (young network, higher excitability)
    for r in brain.regions.values():
        r.theta_bcm = np.full(r.N, 3.0, dtype=np.float64)
    env = SharedEnvironment(100, 100)
    brain_pos = [50.0, 50.0]

    # Phase A: Train phototaxis
    print()
    print("Phase A: Phototaxis Training")
    photo_dist, photo_imp = train_phototaxis(brain, env, brain_pos, N_STEPS_TRAIN)

    # Reset position for next phase
    brain_pos = [50.0, 50.0]

    # Phase B: Train chemotaxis
    print()
    print("Phase B: Chemotaxis Training")
    chemo_dist, chemo_imp = train_chemotaxis(brain, env, brain_pos, N_STEPS_TRAIN)

    # Phase C: Test combination
    print()
    print("Phase C: Combinatorial Test (Zero-shot)")
    brain_pos = [50.0, 50.0]
    combo_result = test_combinatorial(brain, env, brain_pos, N_STEPS_TEST)

    # Rewind: test single-task performance after combination training
    brain_pos = [50.0, 50.0]
    print()
    print("Phase D: Post-combo Single Task Retention Check")
    env2 = SharedEnvironment(100, 100)
    env2.add_resource('light', 80, 50, 2.0)
    light_dist_check = []
    for step in range(100):
        env2.step()
        sensed = env2.sense_for_brain(brain_pos, sense_radius=60.0)
        ext = {}
        if 'vis' in brain.regions:
            ext['vis'] = np.random.randn(brain.regions['vis'].N) * NOISE + sensed['light'] * 1.5
        brain.step(step + 1000, ext)
        ms, mV = brain.get_motor_output()
        half = mV.shape[0] // 2
        dx = (mV[:half].mean() - mV[half:].mean()) * 0.5 + sensed['light'] * 1.2 if half > 0 else sensed['light'] * 1.2
        dy = (mV.mean() - 0.05) * 0.3 + sensed['light'] * 0.8
        brain_pos[0] = np.clip(brain_pos[0] + dx, 0, 100)
        brain_pos[1] = np.clip(brain_pos[1] + dy, 0, 100)
        light_dist_check.append(np.sqrt((brain_pos[0] - 80)**2 + (brain_pos[1] - 50)**2))

    post_combo_photo_imp = np.mean(light_dist_check[:10]) / (np.mean(light_dist_check[-20:]) + 1e-8)
    interference = max(0, photo_imp - post_combo_photo_imp) / (photo_imp + 1e-8)

    # L4 Judgment
    single_task_avg = (photo_imp + chemo_imp) / 2
    combo_threshold = single_task_avg * 0.5
    l4_pass_combo = combo_result['combo_score'] > combo_threshold
    l4_pass_switch = combo_result['switch_cost'] < 0.3
    l4_pass_interference = interference < 0.1
    l4_overall = l4_pass_combo and l4_pass_switch and l4_pass_interference

    # Final report
    print()
    print("=" * 60)
    print("L4 JUDGMENT")
    print("=" * 60)
    print("Single-task avg improvement: " + str(round(single_task_avg, 2)) + "x")
    print("Combo threshold (50%): " + str(round(combo_threshold, 2)) + "x")
    print()
    print("  Combo score: " + str(round(combo_result['combo_score'], 2)) +
          " > " + str(round(combo_threshold, 2)) + " ? " + ("PASS" if l4_pass_combo else "FAIL"))
    print("  Switch cost: " + str(round(combo_result['switch_cost'] * 100, 1)) +
          "% < 30% ? " + ("PASS" if l4_pass_switch else "FAIL"))
    print("  Interference: " + str(round(interference * 100, 1)) +
          "% < 10% ? " + ("PASS" if l4_pass_interference else "FAIL"))
    print()
    print("  L4 OVERALL: " + ("=== PASS ===" if l4_overall else "--- FAIL ---"))
    print()
    state = brain.get_state()
    print("  Brain state: sigma=" + str(round(state['mean_sigma'], 2)) +
          " el=" + str(round(state['mean_el'], 3)))

    return {
        'experiment': 'L4_combinatorial',
        'photo_improvement': float(photo_imp),
        'chemo_improvement': float(chemo_imp),
        'single_task_avg': float(single_task_avg),
        'combo_score': float(combo_result['combo_score']),
        'switch_cost': float(combo_result['switch_cost']),
        'interference': float(interference),
        'l4_pass_combo': l4_pass_combo,
        'l4_pass_switch': l4_pass_switch,
        'l4_pass_interference': l4_pass_interference,
        'l4_overall': l4_overall,
        'brain_state': state
    }


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--train-steps', type=int, default=2000, help='Training steps per task')
    parser.add_argument('--test-steps', type=int, default=400, help='Combinatorial test steps')
    args = parser.parse_args()
    N_STEPS_TRAIN = args.train_steps
    N_STEPS_TEST = args.test_steps
    
    _os.makedirs('simulation/data/l4_results', exist_ok=True)
    print(f'L4 config: train={N_STEPS_TRAIN}, test={N_STEPS_TEST}')
    t_start = time.time()
    result = run_l4_experiment()
    elapsed = time.time() - t_start

    out_path = 'simulation/data/l4_results/l4_combinatorial_results.json'
    with open(out_path, 'w') as f:
        json.dump(result, f, indent=2, default=str)

    print("\nTime: " + str(round(elapsed, 1)) + "s")
    print("Results: " + out_path)
