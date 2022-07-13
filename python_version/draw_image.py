import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import os

from PIL import Image

import generate_beizer_curve


def calculate_fig_size(file_name, multiplier):
    """
    A function that calculates figure's size and set FIGSIZE_X and FIGSIZE_Y
    :param file_name: the files' name to set ratio as. In this program it uses
                      first frame for getting ratio.
    :param multiplier: the multiplier for figsize from ratio
                       (if width:height ratio was 2:1 and multiplier was 10,
                       figsize will be 20, 10)
    """
    im = Image.open(file_name)  # open image using PIL
    width, height = im.size  # get width and height
    width_ratio = float(width) / height  # calculate aspect ratio
    FIGSIZE_X = multiplier * width_ratio  # set multiplier with the ratio
    FIGSIZE_Y = multiplier * 1
    plt.rcParams['figure.figsize'] = (FIGSIZE_X, FIGSIZE_Y)


def generate_picture(file_name, output: str, flag_calculate_fig_size=True,
                     multiplier=10, color='#2464b4', bilateral_filter=False,
                     l2_gradient=False, save=False, fixed_figsize="(10,10)"):
    """
    A simple function that generates images using matplotlib and beizer curves
    :param file_name: the name of image file to generate.
    :param flag_calculate_fig_size: whether or not to automatically calculate
                                    ratio and set figsize.
    :param multiplier: the multiplier for figsize from ratio
                       (if width:height ratio was 2:1 and multiplier was 10,
                       figsize will be 20, 10)
    :param color: a string that represents hex color value of each lines
    :param bilateral_filter: a boolean that decides whether or not to use
                             bilateral filter for generating beizer curves.
    :param l2_gradient: a boolean that decides whether or not to use
                        L2 gradient for generating beizer curves.
    :param save: a boolean that decides whether or not to save the image.
    :param output: a string that represents output file's name.
    """
    print("-----=[ Settings ]=-----")
    print("[+] Auto calculate figsize : " + str(flag_calculate_fig_size))
    print("[+] Line color : " + color)
    if flag_calculate_fig_size:
        print("[+] Figsize multiplier : " + str(multiplier))
    else:
        fixed_figsize = eval(fixed_figsize)
        print("[+] Figsize : " + str(fixed_figsize))
    print("[+] Bilateral Filter : " + str(bilateral_filter))
    print("[+] Use L2 Gradient : " + str(l2_gradient))
    print("[+] Output : " + output)

    print("-----=[ Job Started]=-----")

    curves = generate_beizer_curve.get_curve(file_name,
                                             bilateral_filter, l2_gradient)
    if flag_calculate_fig_size:
        calculate_fig_size(file_name, multiplier)
    else:
        plt.rcParams['figure.figsize'] = (fixed_figsize[0], fixed_figsize[1])

    Path = mpath.Path  # use mpath for drawing bezier curve
    fig, ax = plt.subplots()
    plt.title("Name : " + file_name)  # show title as frames

    save_dir = os.path.join(os.getcwd(), output)

    for curve in curves:  # for all beizer curves, draw it using mpatches
        pp = mpatches.PathPatch(
            Path(curve,
                 [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.CLOSEPOLY]),
            fc="none", transform=ax.transData, color=color)
        ax.add_patch(pp)  # draw all curves and add_patch to ax.
        ax.plot([0], [0])
    if save:  # if save flag was set, save plt figure
        plt.savefig(save_dir)  # save output as the designated filename

    plt.show()
    return fig


if __name__ == "__main__":
    generate_picture(file_name="./img.png", multiplier=15, color="#000000",
                     save=True, output="output.png")
