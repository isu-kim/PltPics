import argparse
import process_video
import draw_image


def add_arguments(parser):
    """
    A function that adds arguments into the parser
    :param parser: the parser object that this script is using
    """
    required_args.add_argument("--type", required=True,
                               help="Type to convert : video / image")
    required_args.add_argument("-i", "--input", required=True,
                               help="Input file")

    parser.add_argument("-o", "--output", required=False, default="output.mp4",
                        help="Output file")
    parser.add_argument("-c", "--cleanup", required=False, action='store_true',
                        default=False,
                        help="Cleanup files once process was done")
    parser.add_argument("-lc", "--line_color", required=False,
                        default="#2464b4",
                        help="Set linecolor in hex : EX) #2464b4")
    parser.add_argument("-mf", "--manual_figsize", required=False,
                        action='store_false',
                        help="Use manual figsize")
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
    parser.add_argument("-s", "--save", required=False, default=False,
                        action='store_true',
                        help="Save image when it was processed")


def process_args(args):
    if args['type'] in ['video', 'image']:
        if args['type'] == 'video':  # if type was video
            process_video.generate_video(video_name=args['input'],
                                         output=args['output'],
                                         clean_up=args['cleanup'],
                                         color=args['line_color'],
                                         flag_calculate_fig_size=args['manual_figsize'],
                                         multiplier=args['multiplier'],
                                         fixed_figsize=args['fixed_figsize'],
                                         bilateral_filter=args['bilateral_filter'],
                                         l2_gradient=args['L2_gradient'],
                                         thread_enabled=args['threading'],
                                         thread_count=args['thread_count'])
        else:  # if type was image
            draw_image.generate_picture(file_name=args['input'],
                                        output=args['output'],
                                        color=args['line_color'],
                                        flag_calculate_fig_size=args['manual_figsize'],
                                        multiplier=args['multiplier'],
                                        fixed_figsize=args['fixed_figsize'],
                                        bilateral_filter=args['bilateral_filter'],
                                        l2_gradient=args['L2_gradient'],
                                        save=args['save'])
    else:
        print("[-] Unknown type : " + args['type'])


if __name__ == "__main__":
    description_string = """
    PltPics - Draw images and generate videos using Matplotlib.pyplot\n
    https://github.com/gooday2die/PltPics
    """
    parser = argparse.ArgumentParser(description=description_string)
    required_args = parser.add_argument_group('required arguments')
    add_arguments(parser)
    args = vars(parser.parse_args())
    process_args(args)
