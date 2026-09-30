![NORA logo](https://i.ibb.co/0VJCC9Gf/IMG-20260114-WA0008.jpg)
 
# Gutenberg-Richter b-Value Calculator
 
*For seismologists and hazard analysts: enter a list of earthquake magnitudes to instantly compute the b-value, a-value, and Gutenberg-Richter frequency-magnitude distribution plot.*
 
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
 

## Overview
 
**Industry:** Seismology
 
Inputs: (1) A text box or file upload for earthquake magnitudes (comma-, space-, or line-separated numbers, at least 10 values). The tool will parse the values and display the count. (2) A number input for the minimum completeness magnitude Mc (default: 2.5, range 0–10, step 0.1). (3) An optional bin width slider (default 0.1, range 0.01–0.5). Core logic: (a) Filter magnitudes ≥ Mc. (b) Compute the magnitude bins: from floor(min(filtered)/bin_width)*bin_width to ceil(max(filtered)/bin_width)*bin_width. (c) Count events per bin. (d) Compute cumulative counts (≥M) per bin. (e) For bins with at least one event, fit the Gutenberg-Richter law log10(N) = a - b*M using least-squares regression on the cumulative counts (fitted in log space). (f) Also compute b-value using Aki's maximum likelihood formula: b = log10(e) / (mean(M) - Mc), where mean is of filtered magnitudes. (g) Compute a-value as log10(total events above Mc) + b*Mc. (h) Output: the b-value (ML method), the b-value (LS fit), the a-value, the total number of events above Mc, the magnitude of completeness Mc, and the standard deviation of b (for ML: std = b / sqrt(N)). Also compute the predicted number of events per year if a time interval is provided? Keep simple: no time needed, just counts. But the tool could optionally ask for a time period (years) to convert a-value to annual rate? Let's keep it simpler: just plot the histogram and the fitted line. Output: A matplotlib figure showing the frequency-magnitude histogram (bars for binned counts) and the fitted G-R line (log10 cumulative vs magnitude) with legends. Also display numerical results as text. Layout: Gradio interface with input components: (a) Textbox for magnitudes (label 'Input magnitudes (comma/space/newline separated)'), (b) File upload for .txt or .csv (if uploaded, parse column of magnitudes), (c) Number input for Mc, (d) Slider for bin width. Outputs: (a) A plot component, (b) A text component showing calculated parameters. No AI/ML component.
 
## Run it
 
```bash
docker build -t gutenberg-richter-b-value-calculator .
docker run -p 7860:7860 gutenberg-richter-b-value-calculator
```
 
Then open http://localhost:7860 in your browser.
 
## About
 
This tool was generated and published automatically by the **NORA Earth Intelligence**
tool factory, an autonomous pipeline maintained by **NORA Research Lab** that turns
one idea per run into a small, working geoscience tool — end to end, with an
LLM writing and Docker-testing the code, and another model generating the
banner above.
 
- Platform: [https://noraearth.xyz](https://noraearth.xyz)
- Parent lab: [https://noraresearchlab.site](https://noraresearchlab.site)
 
Built 2026-09-30.
 
---
 
### Maintainer
 
**NORA Research Lab**
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
