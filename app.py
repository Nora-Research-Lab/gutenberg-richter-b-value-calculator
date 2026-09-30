import gradio as gr
import matplotlib
matplotlib.use('Agg')  # non-interactive backend for Docker
from gutenberg_richter_b_value_calculator import (
    parse_magnitudes,
    compute_b_value_mle,
    compute_b_value_ls,
    build_plot
)
import io

def process_inputs(mag_text, mag_file, mc, bin_width):
    try:
        magnitudes = parse_magnitudes(mag_text, mag_file)
    except (ValueError, TypeError) as e:
        return None, f"Error parsing magnitudes: {e}"

    if len(magnitudes) < 10:
        return None, f"Need at least 10 magnitudes, got {len(magnitudes)}."

    if mc < 0 or mc > 10:
        return None, "Mc must be between 0 and 10."

    filtered = [m for m in magnitudes if m >= mc]
    if len(filtered) == 0:
        return None, "No magnitudes above the chosen Mc."

    b_ml, a_ml, std_b = compute_b_value_mle(filtered, mc)
    b_ls, a_ls = compute_b_value_ls(filtered, mc, bin_width)
    N = len(filtered)

    fig = build_plot(filtered, mc, bin_width, b_ml, b_ls, a_ml, a_ls, N, std_b)

    result_text = (
        f"Number of events (M ≥ {mc:.2f}): {N}\n"
        f"b (MLE) = {b_ml:.4f}   ± {std_b:.4f}\n"
        f"b (LSF) = {b_ls:.4f}\n"
        f"a (using MLE b) = {a_ml:.4f}\n"
        f"Magnitude of completeness Mc = {mc}"
    )
    return fig, result_text

with gr.Blocks(title="Gutenberg‑Richter b‑Value Calculator") as demo:
    gr.Markdown("# Gutenberg‑Richter b‑Value Calculator")
    with gr.Row():
        with gr.Column():
            mag_text = gr.Textbox(
                label="Input magnitudes (comma/space/newline separated)",
                placeholder="e.g. 3.2 4.1 5.0 2.9 ...",
                lines=5
            )
            mag_file = gr.File(label="Or upload a .txt / .csv file (one column)")
            mc = gr.Number(label="Minimum completeness magnitude Mc", value=2.5, minimum=0, maximum=10, step=0.1)
            bin_width = gr.Slider(label="Bin width", minimum=0.01, maximum=0.5, value=0.1, step=0.01)
            submit_btn = gr.Button("Compute")
        with gr.Column():
            plot_out = gr.Plot(label="Frequency‑Magnitude Distribution")
            text_out = gr.Textbox(label="Results", lines=8)
    submit_btn.click(fn=process_inputs, inputs=[mag_text, mag_file, mc, bin_width], outputs=[plot_out, text_out])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
