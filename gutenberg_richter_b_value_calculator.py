import numpy as np
import matplotlib.pyplot as plt

# ──────────────────────────────────────────────
# Parsing
# ──────────────────────────────────────────────
def parse_magnitudes(text_input=None, file_input=None):
    """
    Parse magnitude values from a text string or an uploaded file object.
    Returns a list of floats.
    """
    values = []
    if file_input is not None:
        # file_input is a temp file path or a file-like object
        content = file_input.decode('utf-8') if isinstance(file_input, bytes) else ""
        # If it's a file path (spaces and newlines)
        # Actually, in Gradio, file_input is a NamedString or BytesIO, we handle both.
        if hasattr(file_input, 'name'):
            with open(file_input.name, 'r') as f:
                content = f.read()
        elif isinstance(file_input, bytes):
            content = file_input.decode('utf-8')
        numbers = _extract_numbers(content)
        values.extend(numbers)
    if text_input and text_input.strip():
        numbers = _extract_numbers(text_input)
        values.extend(numbers)
    if not values:
        raise ValueError("No numeric magnitudes provided.")
    # Validate all are finite positive? allow negative? seismic magnitudes are positive typically, but allow any real.
    values = [float(v) for v in values]
    if any(np.isnan(v) for v in values) or any(np.isinf(v) for v in values):
        raise ValueError("Magnitudes must be finite numbers.")
    return values

def _extract_numbers(text):
    """Extract floats from a string separated by commas, spaces, or newlines."""
    import re
    numbers = re.findall(r"-?\d+\.?\d*", text.replace(",", " "))
    return [float(x) for x in numbers if x]

# ──────────────────────────────────────────────
# b-value (Maximum Likelihood / Aki)
# ──────────────────────────────────────────────
def compute_b_value_mle(magnitudes, mc):
    """
    Compute b-value using Aki's maximum likelihood formula.
    Returns (b, a, std_b).
    """
    mag_above = np.array(magnitudes)
    mean_m = np.mean(mag_above)
    N = len(mag_above)
    if mean_m - mc <= 0:
        raise ValueError("Mean magnitude must be greater than Mc.")
    b = np.log10(np.e) / (mean_m - mc)
    # Standard error (Shi & Bolt, 1982)
    std_b = b / np.sqrt(N)
    # a-value: log10(N_total) + b * Mc
    a = np.log10(N) + b * mc
    return b, a, std_b

# ──────────────────────────────────────────────
# b-value (Least Squares on cumulative distribution)
# ──────────────────────────────────────────────
def compute_b_value_ls(magnitudes, mc, bin_width):
    """
    Compute b-value by least-squares fit to the cumulative frequency-magnitude
    distribution in log-space.
    Returns (b_ls, a_ls).
    """
    mag_above = np.array(magnitudes)
    if len(mag_above) == 0:
        raise ValueError("No magnitudes above Mc.")

    # Bin edges
    min_mag = np.floor(mag_above.min() / bin_width) * bin_width
    max_mag = np.ceil(mag_above.max() / bin_width) * bin_width
    bins = np.arange(min_mag, max_mag + bin_width, bin_width)
    # Bin centres
    bin_centers = bins[:-1] + bin_width / 2

    # Counts (non-cumulative)
    counts, _ = np.histogram(mag_above, bins=bins)
    # Cumulative counts (>= M)
    cum_counts = np.cumsum(counts[::-1])[::-1]   # cumulative from high to low

    # Only bins with at least 1 event (to avoid log10(0))
    valid = cum_counts >= 1
    if np.sum(valid) < 2:
        raise ValueError("Not enough non-zero cumulative bins for fitting.")

    M_fit = bin_centers[valid]
    logN_fit = np.log10(cum_counts[valid])

    # Linear fit: log10(N) = a - b * M  => y = a + c * M,  c = -b
    coeffs = np.polyfit(M_fit, logN_fit, 1)   # [c, a]
    c, a_ls = coeffs
    b_ls = -c
    return b_ls, a_ls

# ──────────────────────────────────────────────
# Plotting
# ──────────────────────────────────────────────
def build_plot(magnitudes, mc, bin_width, b_ml, b_ls, a_ml, a_ls, N_above, std_b):
    """
    Create a matplotlib figure with:
    - Left y-axis: histogram (non‑cumulative counts)
    - Right y-axis: cumulative counts (log10 scale) + fitted G‑R line (LS).
    """
    mag_above = np.array(magnitudes)
    # Compute bin edges for histogram
    min_mag = np.floor(mag_above.min() / bin_width) * bin_width
    max_mag = np.ceil(mag_above.max() / bin_width) * bin_width
    bins = np.arange(min_mag, max_mag + bin_width, bin_width)

    # Histogram counts
    counts, bin_edges = np.histogram(mag_above, bins=bins)
    bin_centers = bin_edges[:-1] + bin_width / 2

    # Cumulative counts
    cum_counts = np.cumsum(counts[::-1])[::-1]   # ≥M

    # Fit line (LS) over the whole magnitude range
    M_line = np.linspace(min_mag, max_mag, 200)
    logN_line = a_ls - b_ls * M_line
    N_line = 10 ** logN_line

    fig, ax1 = plt.subplots(figsize=(9, 6))

    # Histogram on primary y-axis
    ax1.bar(bin_centers, counts, width=bin_width * 0.9, color='steelblue', alpha=0.7, label='Event counts')
    ax1.set_xlabel('Magnitude')
    ax1.set_ylabel('Number of events (linear)', color='steelblue')
    ax1.tick_params(axis='y', labelcolor='steelblue')

    # Secondary y-axis for cumulative (log10)
    ax2 = ax1.twinx()
    # Plot cumulative as points
    valid = cum_counts >= 1
    ax2.scatter(bin_centers[valid], cum_counts[valid], c='red', s=30, label='Cumulative (≥M)', zorder=5)
    # Fitted line
    ax2.plot(M_line, N_line, 'r--', linewidth=2, label=f'G‑R fit (b={b_ls:.2f})')
    ax2.set_ylabel('Cumulative number (log scale)', color='red')
    ax2.set_yscale('log')
    ax2.tick_params(axis='y', labelcolor='red')

    # Add legend combining both axes
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

    # Title
    ax1.set_title(f'Frequency‑Magnitude Distribution\n(Mc = {mc:.2f}, bin = {bin_width:.2f})')

    fig.tight_layout()
    return fig
