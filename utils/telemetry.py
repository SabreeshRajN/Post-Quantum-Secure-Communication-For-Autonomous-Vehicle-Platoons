"""Benchmark telemetry: RTT + crypto-operation timings, with a matplotlib dashboard.

Every sample is also appended to benchmark/results.csv so a run's raw
numbers survive after the dashboard window is closed.
"""

import csv
import os
import time

import matplotlib.pyplot as plt

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_RESULTS_DIR = os.path.join(_PROJECT_ROOT, "benchmark")
_RESULTS_CSV = os.path.join(_RESULTS_DIR, "results.csv")

_rtts = []
_timings = {"keygen": [], "encapsulation": [], "decapsulation": [], "encryption": [], "decryption": []}


def _append_csv(metric, value_ms):
    os.makedirs(_RESULTS_DIR, exist_ok=True)
    is_new = not os.path.exists(_RESULTS_CSV)
    with open(_RESULTS_CSV, "a", newline="") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["timestamp", "metric", "value_ms"])
        writer.writerow([f"{time.time():.3f}", metric, f"{value_ms:.4f}"])


def record_rtt(rtt_ms):
    _rtts.append(rtt_ms)
    _append_csv("rtt", rtt_ms)


def record_timing(operation, elapsed_ms):
    """Used internally by vehicles.vehicle to log Kyber/AES operation timings."""
    _timings.setdefault(operation, []).append(elapsed_ms)
    _append_csv(operation, elapsed_ms)


def _plot_series(ax, samples, title, ylabel):
    if samples:
        ax.bar(range(1, len(samples) + 1), samples, color="#4c72b0")
    else:
        ax.text(0.5, 0.5, "no samples", ha="center", va="center", transform=ax.transAxes)
    ax.set_title(title)
    ax.set_xlabel("sample #")
    ax.set_ylabel(ylabel)


def show_dashboard():
    """Render the 4-panel benchmark dashboard: Kyber KeyGen / Encapsulation /
    Decapsulation timings, plus command RTT alongside AES-256-GCM timings."""
    if not _rtts and not any(_timings.values()):
        print("[telemetry] no samples recorded -- nothing to plot")
        return

    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    fig.suptitle("Post-Quantum Secure V2V Platoon -- Benchmark Dashboard")

    _plot_series(axes[0][0], _timings["keygen"], "Kyber-768 KeyGen", "ms")
    _plot_series(axes[0][1], _timings["encapsulation"], "Kyber-768 Encapsulation", "ms")
    _plot_series(axes[1][0], _timings["decapsulation"], "Kyber-768 Decapsulation", "ms")

    ax = axes[1][1]
    if _rtts:
        ax.plot(range(1, len(_rtts) + 1), _rtts, marker="o", label="command RTT")
    if _timings["encryption"]:
        ax.plot(range(1, len(_timings["encryption"]) + 1), _timings["encryption"],
                 marker=".", label="AES-GCM encrypt")
    if _timings["decryption"]:
        ax.plot(range(1, len(_timings["decryption"]) + 1), _timings["decryption"],
                 marker=".", label="AES-GCM decrypt")
    ax.set_title("Command RTT + AES-256-GCM timings")
    ax.set_xlabel("sample #")
    ax.set_ylabel("ms")
    if _rtts or _timings["encryption"] or _timings["decryption"]:
        ax.legend()

    fig.tight_layout()
    plt.show()
