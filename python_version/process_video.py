import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import os
import threading
from pathlib import Path
from PIL import Image

import generate_beizer_curve

COLOUR = '#2464b4'  # Hex value of colour for graph output
FIGSIZE_X = 20
FIGSIZE_Y = 20
DPI = 80


def calculate_fig_size(file_name, multiplier):
    """
    A function that calculates figure's size and set FIGSIZE_X and FIGSIZE_Y
    :param file_name: the files' name to set ratio as. In this program it uses
                      first frame for getting ratio.
    :param multiplier: the multiplier for figsize from ratio
                       (if width:height ratio was 2:1 and multiplier was 10,
                       figsize will be 20, 10)
    """
    im = Image.open(file_name)
    width, height = im.size
    global FIGSIZE_X
    global FIGSIZE_Y
    width_ratio = float(width) / height
    FIGSIZE_X = multiplier * width_ratio
    FIGSIZE_Y = multiplier * 1


def set_fig_size():
    """
    A function that sets figsize using pylab
    """
    plt.rcParams['figure.figsize'] = (FIGSIZE_X, FIGSIZE_Y)


def process_frame(tmp_dir, curves, frame_name):
    """
    A function that generates a pyplot using the bezier curves.
    This function will generate pyplot and save it to tmp_dir
    :param tmp_dir: the temporary directory to store frame pictures into
    :param curves: the paths oof beizer curves
    :param frame_count: the current frame's name to save picture into.
    """
    Path = mpath.Path  # use mpath for drawing bezier curve
    fig, ax = plt.subplots()
    plt.title("Frame : " + str(frame_name))  # show title as frames
    plt.ioff()  # do not show plt
    for curve in curves:
        pp = mpatches.PathPatch(
            Path(curve,
                 [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.CLOSEPOLY]),
            fc="none", transform=ax.transData, color=COLOUR)
        ax.add_patch(pp)  # draw all curves and add_patch to ax.
        ax.plot([0], [0])
    # use %03d since we are using ffmpeg
    save_file_name = os.path.join(tmp_dir, "%03d.png" % frame_name)
    try:  # try saving into the directory
        plt.savefig(save_file_name, dpi=80)
        plt.close(fig)  # close fig since we do not want it to be seen
    except FileNotFoundError:  # generate tmp_directory for saving pictures
        os.mkdir(tmp_dir)
        plt.savefig(save_file_name)
        plt.close(fig)  # close fig since we do not want it to be seen


def extract_frames(video_name, frame_dir):
    """
    A function that extracts video frames into frame directory
    :param video_name: a string that represents video's name
    :param frame_dir: the directory to save frames into
    """
    # extract frames using ffmpeg
    os.system("ffmpeg -i " + video_name + " " + frame_dir + "/frame%03d.png")


"""
Experimental feature!
Using threads for generating pictures faster!
"""


def split(a, n):
    """
    From https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
    """
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))


def t_generate_pictures_segment(**kwargs):
    """
    A function that generates pictures secgment.
    This function is meant to be called by thread
    :param tmp_dir: the temporary directory to store frame pictures into
    :param frame_dir: the directory to save frames into
    :param files: the list that includes file's names
    """
    tmp_dir = kwargs['tmp_dir']
    frame_dir = kwargs['frame_dir']
    files = kwargs['files']
    for file in files:
        file = file.decode('utf-8').replace(".png", "")
        file = file.replace("frame", "")
        print("[+] Processing frame : " + file)
        cur_file = os.path.join(frame_dir, file)
        curves = generate_beizer_curve.get_curve(cur_file)
        process_frame(tmp_dir, curves, file)


def t_generate_pictures(tmp_dir, frame_dir, thread_count):
    """
    A function that generates pictures using multiple threads
    :param tmp_dir: the temporary directory to store frame pictures into
    :param frame_dir: the directory to save frames into
    :param thread_count: the count of threads to generate
    """
    print("[+] Using " + str(thread_count) + " threads...")
    directory = os.fsencode(frame_dir)

    thread_list = list()
    file_list = list(split(os.listdir(directory), thread_count))

    for files in file_list:
        t = threading.Thread(target=t_generate_pictures_segment,
                             kwargs={'tmp_dir': tmp_dir,
                                     'frame_dir': frame_dir,
                                     'files': files})
        thread_list.append(t)
    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()


def generate_pictures(tmp_dir, frame_dir):
    """
    A function that generate pictures using process_frames and generates
    images using plt.
    :param tmp_dir: the temporary directory to store frame pictures into
    :param frame_dir: the directory to save frames into
    """
    directory = os.fsencode(frame_dir)
    files = os.listdir(directory)
    file_count = len(files)

    for i in range(1, file_count, 1):
        print("[+] Processing frame : " + str(i) + " / " + str(file_count))
        cur_file = os.path.join(frame_dir + "/" + "frame%03d.png" % i)
        curves = generate_beizer_curve.get_curve(cur_file)
        process_frame(tmp_dir, curves, i)


def generate_video(video_name, tmp_dir, frame_dir, clean_up=True,
                   flag_calculate_fig_size=True, multiplier=10,
                   thread_enabled=False, thread_count=4):
    """
    A function that generates plot video out of a video using plt.
    :param video_name: string that represents video's name
    :param tmp_dir: the temporary directory to store frame pictures into
    :param frame_dir: the directory to save frames into
    :param clean_up: whether or not to clean up tmp_dir and frame_dir
    :param flag_calculate_fig_size: whether or not to automatically calculate
                                    ratio and set figsize.
    :param multiplier: the multiplier for figsize from ratio
                       (if width:height ratio was 2:1 and multiplier was 10,
                       figsize will be 20, 10)
    :param thread_enabled: whether or not to use multiple threads
    :param thread_count: the count of threads to generate
    """

    try:  # try making tmp_dir and frame_dir
        os.mkdir(tmp_dir)
    except FileExistsError:
        pass

    try:  # try making tmp_dir and frame_dir
        os.mkdir(frame_dir)
    except FileExistsError:
        pass

    print("[+] Extracting frames...")
    extract_frames(video_name, frame_dir)
    print("[+] Extracting frames done!")

    if calculate_fig_size:
        calculate_fig_size(frame_dir + "/frame" + "%03d.png" % 1, multiplier)

    set_fig_size()

    print("[+] Processing frames...\n")
    if thread_enabled:
        t_generate_pictures(tmp_dir, frame_dir, thread_count)
    else:
        generate_pictures(tmp_dir, frame_dir)
    print("[+] Generating output.mp4...")
    os.system("ffmpeg -pattern_type glob -i " + tmp_dir +
              "/\"*.png\" output.mp4 -y")

    if clean_up:
        os.system("rm -rf " + tmp_dir)  # This is OS dependent!
        os.system("rm -rf " + frame_dir)
        print("[+] Cleaned up directories")


if __name__ == "__main__":
    tmp_dir = os.path.join(os.getcwd(), "tmp_pics")
    frame_dir = os.path.join(os.getcwd(), "frames")
    print(frame_dir)
    generate_video("./nootnoot.mp4", tmp_dir, frame_dir, clean_up=False,
                   multiplier=10, thread_enabled=False, thread_count=0)
