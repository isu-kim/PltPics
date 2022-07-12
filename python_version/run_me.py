import argparse
import process_video
import draw_image


if __name__ == "__main__":
    description_string = """
    PltPics - Draw images and generate videos using Matplotlib.pyplot\n
    https://github.com/gooday2die/PltPics
    """
    parser = argparse.ArgumentParser(description=description_string)
    required_args = parser.add_argument_group('required arguments')

    required_args.add_argument("--type", required=True,
                        help="Type to convert : video / image")
    required_args.add_argument("-i", "--input", required=True,
                        help="Input file")

    parser.add_argument("-o", "--output", required=False, default="output.mp4",
                        help="Output file")
    parser.add_argument("-v", "--verbose", required=False, action='store_true',
                        help="Use verbose mode")
    parser.add_argument("-c", "--cleanup", required=False, action='store_true',
                        help="Cleanup files once process was done")
    parser.add_argument("-lc", "--line_color", required=False,
                        default="#2464b4",
                        help="Set linecolor in hex : EX) #2464b4")
    parser.add_argument("-cf", "--calculate_figsize", required=False,
                        default=True, type=bool,
                        help="Auto calculate figsize of pyplot : True / False")
    parser.add_argument("-m", "--multiplier", required=False,
                        default=10, type=int,
                        help="Multiplier for figsize of pyplot : EX) 10")
    parser.add_argument("-ff", "--fixed_figsize", required=False,
                        default="(10,10)", type=str,
                        help="Set figsize of pyplot : EX) \"(10, 10)\"")
    parser.add_argument("-bf", "--bilateral_filter", required=False,
                        action='store_true',
                        help="Use bilateral filter for generating curves")
    parser.add_argument("-l2", "--L2_gradient", required=False,
                        action='store_true',
                        help="Use L2 Gradient for generating curve")
    parser.add_argument("-t", "--threading", required=False,
                        action='store_true',
                        help="Use multithreading")
    parser.add_argument("-tc", "--thread_count", required=False, default=4,
                        help="Total thread count for multithreading, need -t")

    args = parser.parse_args()
