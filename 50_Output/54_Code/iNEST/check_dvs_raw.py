import tonic
import numpy as np

ds = tonic.datasets.DVSGesture(save_to="datasets/DVSGesture_raw", train=True)
print(f"Training set: {len(ds)} samples")

events, target = ds[0]
print(f"Sample 0: target={target}")
print(f"Events dtype names: {events.dtype.names}")
print(f"Events shape: {events.shape}")
print(f"t range: {events['t'].min()} - {events['t'].max()} us")
print(f"Duration: {(events['t'].max() - events['t'].min())/1e3:.1f} ms")
print(f"x: {events['x'].min()}-{events['x'].max()}, y: {events['y'].min()}-{events['y'].max()}")
print(f"Polarities: {np.unique(events['p'])}")

# Check a few samples
for i in [0, 50, 100]:
    e, t = ds[i]
    dur = (e['t'].max() - e['t'].min())/1e3
    print(f"Sample {i}: class={t}, {len(e)} events, {dur:.0f}ms")
