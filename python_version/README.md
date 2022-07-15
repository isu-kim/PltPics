# PltPics
## Command Line Interface
PltPics support CLI interface alongside with `ipynb` support. Execute `run_me.py` for CLI.

### Help
```
usage: run_me.py [-h] --type TYPE -i INPUT [-o OUTPUT] [-c] [-lc LINE_COLOR]
                 [-mf] [-m MULTIPLIER] [-ff FIXED_FIGSIZE] [-bf] [-l2] [-t]
                 [-tc THREAD_COUNT] [-s]

PltPics - Draw images and generate videos using Matplotlib.pyplot
https://github.com/gooday2die/PltPics

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file
  -c, --cleanup         Cleanup files once process was done
  -lc LINE_COLOR, --line_color LINE_COLOR
                        Set linecolor in hex : EX) #2464b4
  -mf, --manual_figsize
                        Use manual figsize
  -m MULTIPLIER, --multiplier MULTIPLIER
                        Multiplier for figsize of pyplot : EX) 10
  -ff FIXED_FIGSIZE, --fixed_figsize FIXED_FIGSIZE
                        Set figsize of pyplot : EX) "(10, 10)"
  -bf, --bilateral_filter
                        Use bilateral filter for generating curves
  -l2, --L2_gradient    Use L2 Gradient for generating curve
  -t, --threading       Use multithreading
  -tc THREAD_COUNT, --thread_count THREAD_COUNT
                        Total thread count for multithreading, need -t
  -s, --save            Save image when it was processed

required arguments:
  --type TYPE           Type to convert : video / image
  -i INPUT, --input INPUT
                        Input file

```

### Required Arguments
- `--type TYPE` : The media type to convert, there are `video` and `image` options available. Example would be `--type video` (for videos).
- ` -i INPUT, --input INPUT` : The input file to convert. 

### Optional Arguments
- `-h, --help` : Prints out the help message

- `-o OUTPUT, --output OUTPUT` : Set output file's name. For `image` types, unless `-s, --save` option is set, the image will **NOT** be saved.

- `-s, --save`: Save image when it was done processing. This is for `image` types **ONLY**.

- `-c, --cleanup` : Cleans up tmp files from directory after video was processed. This is for `video` types **ONLY**. `video` generates `./frames` and `./tmp_pics` directory when processing video. If this option was set, it will delete both two directories.

- `-lc LINE_COLOR, --line_color LINE_COLOR`: Set line color value of `matplotlib.pyplot`. Example would be `-lc #000000` (for black).

- `-mf, --manual_figsize`: Manually set `matplotlib.pyplot`'s `figsize`.

- `-m MULTIPLIER, --multiplier MULTIPLIER`: Set automatically calculated `figsize`'s value with this multiplier. For example, if the image has `2:1` ratio of width and height and `-m 10` was set, this will set `plt.figsize` as `[20,10]`. This will **NOT** work when `--manual_figsize` is on.

- `-ff FIXED_FIGSIZE, --fixed_figsize FIXED_FIGSIZE`: Set `plt.figsize` as provided value. Example would be `-ff "(10,10)"`. This will **ONLY** work when `--manual_figsize` is on.

- `-bf, --bilateral_filter`: Enable bilateral filter when generating bezier curves.

- `-l2, --L2_gradient`: Use L2 gradient when generating bezier curves.

- `-t, --threading`: Use multithreading when generating video. This is for `video` types **ONLY**. (Kind of buggy, so will be fixing this in the future)

- `-tc THREAD_COUNT, --thread_count THREAD_COUNT`: Set thread count for mulithreading. Example would be `-tc 4` (will use 4 threads). This is for `video` types **ONLY**. (Kind of buggy, so will be fixing this in the future). This will work **ONLY** when `--threading` option is on.

## Example commands
### Images
-  `python3 run_me.py -i img.png -o imgout.png --type image -s` 

This will convert an image input of `img.png` and will `save` the `matplotlib.pyplot`'s image output to `imgout.png`.

- `python3 run_me.py --type image -i img.png -mf -ff "(10,10)" -s -o imgout.png -lc "#000000" -l2`

This will convert image input of `img.png` and will `save` the `matplotlib.pyplot`'s image output to `imgout.png`. The image will have `line color` of `#000000` and will be using `L2 Gradient` feature with `manually fixed` figsize of `(10,10)`. 

### Videos
- `python3 run_me.py -i nootnoot.mp4 -o out.mp4 --type video -c`

This will convert a video named `nootnoot.mp4` into `out.mp4` and `cleans up` the workspace after the process was done.

- `python3 run_me.py -i nootnoot.mp4 -o out.mp4 --type video -mf -ff "(10,10)" -lc "#000000" -c`

This will convert a video named `nootnoot.mp4` into `out.mp4`. Each frames will be `manually fixed` figsize of `(10,10)` and will have `line color` of `#000000`. After the process was done, it will `clean up` the workspace.
