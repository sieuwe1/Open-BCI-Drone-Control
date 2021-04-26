# Open-BCI-Drone-Control

- [ ] Parse and select training data from recorded data
- [ ] Create fft out of training data
- [ ] Create image out of fft data
- [ ] Parse target data
- [ ] Create training `.py` file that uses the image and target data

## Parse and select training data

Need to filter out the (probably) start and end, as that may not be usable, sync the data to the visualizations.

## Create fft out training data

Have to experiment with the length of the fft sample to get meaningful data points.

## Create image out of fft data

Have to find the fastest way of constructing an image out of fft data points.
