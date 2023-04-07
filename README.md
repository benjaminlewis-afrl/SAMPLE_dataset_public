# The public SAMPLE dataset

The SAMPLE dataset (Synthetic and Measured Paired Labeled Experiment) dataset consists of measured SAR imagery from the MSTAR data collect and is paired with simulated synthetic SAR imagery. The public version of this dataset is data with azimuth angles between 10 and 80 degrees. 

For a description of the dataset, please read the paper in this repository, which has the filename "sample_public.pdf". 

verify.py is used internally to verify the composition of the dataset.

Distribution A: Approved for public release. Distribution unlimited. 

PA Approval for paper is #88ABW-2019-1483.

PA Approval for SAMPLE dataset is #88ABW-2019-1300

References

[1] - Benjamin Lewis, Theresa Scarnati, Elizabeth Sudkamp, John Nehrbass, Stephen Rosencrantz, Edmund Zelnio, "A SAR dataset for ATR development: the Synthetic and Measured Paired Labeled Experiment (SAMPLE)," Proc. SPIE 10987, Algorithms for Synthetic Aperture Radar Imagery XXVI, 109870H (14 May 2019); https://doi.org/10.1117/12.2523460

Keywords: SAMPLE Dataset, SAR, Synthetic Aperture Radar, Dataset, Machine Learning dataset, SAR Dataset, Synthetic and Measured

Explanation of normalizations:

    For Decibel, we apply 20 * log_10(x) to each pixel, although a small epsilon is added to x for numerical stability.
    For QPM, we apply sqrt(x) to each pixel. QPM stands for 'quarter power magnitude'. 

After applying the respective normalizations, the resulting images are scaled to unsigned ints between 0 and 255 and saved as PNG files.
