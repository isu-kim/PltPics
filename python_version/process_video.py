import matplotlib.path as mpath
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import os
import threading
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


def process_frame(tmp_dir, curves, frame_name, color):
    """
    A function that generates a pyplot using the bezier curves.
    This function will generate pyplot and save it to tmp_dir
    :param tmp_dir: the temporary directory to store frame pictures into
    :param curves: the paths oof beizer curves
    :param frame_count: the current frame's name to save picture into.
    :param color: a string that represents hex color of each lines
    """
    fig, ax = plt.subplots()
    Path = mpath.Path
    plt.title("Frame : " + str(frame_name))  # show title as frames
    plt.ioff()  # do not show plt
    for curve in curves:  # for all beizer curves, draw it using mpatches
        pp = mpatches.PathPatch(
            Path(curve,
                 [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.CLOSEPOLY]),
            fc="none", transform=ax.transData, color=color)
        ax.add_patch(pp)  # draw all curves and add_patch to ax.
        ax.plot([0], [0])
    # use %03d since we are using ffmpeg
    save_file_name = os.path.join(tmp_dir, "%03d.png" % frame_name)
    try:  # try saving into the directory
        plt.savefig(save_file_name, dpi=80)
        plt.close(fig)  # close fig since we do not want it to be seen
    except FileNotFoundError:  # generate tmp_directory for saving pictures
        os.mkdir(tmp_dir)
        plt.savefig(save_file_name)  # save file
        plt.close(fig)  # close fig since we do not want it to be seen


def extract_frames_and_audio(video_name, frame_dir):
    """
    A function that extracts video frames and audio.
    :param video_name: a string that represents video's name
    :param frame_dir: the directory to save frames into
    """
    # extract frames using ffmpeg
    os.system("ffmpeg -i " + video_name + " " + frame_dir + "/frame%03d.png")
    os.system("ffmpeg -i " + video_name + " -vn -acodec copy audio.aac")


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
    :param color: a string that represents hex color value of each lines
    :param bilateral_filter: a boolean that decides whether or not to use
                             bilateral filter for generating beizer curves.
    :param l2_gradient: a boolean that decides whether or not to use
                        L2 gradient for generating beizer curves.
    """
    tmp_dir = kwargs['tmp_dir']
    frame_dir = kwargs['frame_dir']
    files = kwargs['files']
    color = kwargs['color']
    print(color)
    bilateral_filter = kwargs['bilateral_filter']
    l2_gradient = kwargs['l2_gradient']

    for file_name in files:  # for all files, process frame
        file_name = file_name.decode('utf-8').replace(".png", "")
        file_name = file_name.replace("frame", "")
        print("[+] Processing frame : " + file_name)
        cur_file = os.path.join(frame_dir, file_name)
        curves = generate_beizer_curve.get_curve(cur_file, bilateral_filter,
                                                 l2_gradient)
        process_frame(tmp_dir, curves, file_name, color)


def t_generate_pictures(tmp_dir, frame_dir, thread_count,
                        bilateral_filter, l2_gradient, color):
    """
    A function that generates pictures using multiple threads
    :param tmp_dir: the temporary directory to store frame pictures into
    :param frame_dir: the directory to save frames into
    :param thread_count: the count of threads to generate
    :param color: a string that represents hex color value of each lines
    :param bilateral_filter: a boolean that decides whether or not to use
                             bilateral filter for generating beizer curves.
    :param l2_gradient: a boolean that decides whether or not to use
                        L2 gradient for generating beizer curves.
    """
    print("[+] Using " + str(thread_count) + " threads...")
    directory = os.fsencode(frame_dir)

    thread_list = list()
    # split files using split function
    file_list = list(split(os.listdir(directory), thread_count))

    for files in file_list:
        t = threading.Thread(target=t_generate_pictures_segment,
                             kwargs={'tmp_dir': tmp_dir,
                                     'frame_dir': frame_dir,
                                     'files': files,
                                     'color': color,
                                     'bilateral_filter': bilateral_filter,
                                     'l2_gradient': l2_gradient})
        thread_list.append(t)
    for t in thread_list:
        t.start()

    for t in thread_list:
        t.join()


def generate_pictures(tmp_dir, frame_dir, bilateral_filter, l2_gradient,
                      color):
    """
    A function that generate pictures using process_frames and generates
    images using plt.
    :param tmp_dir: the temporary directory to store frame pictures into
    :param frame_dir: the directory to save frames into
    :param color: a string that represents hex color value of each lines
    :param bilateral_filter: a boolean that decides whether or not to use
                             bilateral filter for generating beizer curves.
    :param l2_gradient: a boolean that decides whether or not to use
                        L2 gradient for generating beizer curves.
    """
    directory = os.fsencode(frame_dir)
    files = os.listdir(directory)
    file_count = len(files)

    for i in range(1, file_count, 1):  # iterate over all frames
        print("[+] Processing frame : " + str(i) + " / " + str(file_count))
        cur_file = os.path.join(frame_dir + "/" + "frame%03d.png" % i)
        curves = generate_beizer_curve.get_curve(cur_file, bilateral_filter,
                                                 l2_gradient)
        process_frame(tmp_dir, curves, i, color)


def generate_video(video_name, fixed_figsize="(10,10)", clean_up=True,
                   flag_calculate_fig_size=True, multiplier=10,
                   thread_enabled=False, thread_count=4, color="#2464b4",
                   bilateral_filter=False, l2_gradient=False,
                   output="output.mp4"):
    """
    A function that generates plot video out of a video using plt.
    :param video_name: string that represents video's name
    :param fixed_figsize: a tuple that sets fixed figsize
    :param clean_up: whether or not to clean up tmp_dir and frame_dir
    :param flag_calculate_fig_size: whether or not to automatically calculate
                                    ratio and set figsize.
    :param multiplier: the multiplier for figsize from ratio
                       (if width:height ratio was 2:1 and multiplier was 10,
                       figsize will be 20, 10)
    :param thread_enabled: whether or not to use multiple threads
    :param thread_count: the count of threads to generate
    :param color: a string that represents hex color value of each lines
    :param bilateral_filter: a boolean that decides whether or not to use
                             bilateral filter for generating beizer curves.
    :param l2_gradient: a boolean that decides whether or not to use
                        L2 gradient for generating beizer curves.
    :param output: a string that represent output file's name
    """
    tmp_dir = os.path.join(os.getcwd(), "tmp_pics")
    frame_dir = os.path.join(os.getcwd(), "frames")

    try:  # try making tmp_dir and frame_dir
        os.mkdir(tmp_dir)
    except FileExistsError:
        pass

    try:  # try making tmp_dir and frame_dir
        os.mkdir(frame_dir)
    except FileExistsError:
        pass

    print("-----=[ Settings ]=-----")
    print("[+] Clean up set : " + str(clean_up))
    print("[+] Auto calculate figsize : " + str(flag_calculate_fig_size))
    if flag_calculate_fig_size:
        print("[+] Figsize multiplier : " + str(multiplier))
        print("[+] Multithread : " + str(thread_enabled))
    else:
        fixed_figsize = eval(fixed_figsize)
        print("[+] Figsize : " + str(fixed_figsize))
    if thread_enabled:
        print("[+] Thread count : " + str(thread_count))

    print("[+] Line color : " + color)
    print("[+] Bilateral Filter : " + str(bilateral_filter))
    print("[+] Use L2 Gradient : " + str(l2_gradient))
    print("[+] Output : " + output)

    print("-----=[ Job Started]=-----")
    print("[+] Extracting frames...")
    extract_frames_and_audio(video_name, frame_dir)
    print("[+] Extracting frames done!")

    if flag_calculate_fig_size:  # if automatically set figsize
        calculate_fig_size(frame_dir + "/frame" + "%03d.png" % 1, multiplier)
    else:  # if mannually set figsize
        plt.rcParams['figure.figsize'] = (fixed_figsize[0], fixed_figsize[1])

    print("[+] Processing frames...\n")
    if thread_enabled:
        t_generate_pictures(tmp_dir=tmp_dir, frame_dir=frame_dir,
                            thread_count=thread_count, color=color,
                            bilateral_filter=bilateral_filter,
                            l2_gradient=l2_gradient)
    else:
        generate_pictures(tmp_dir=tmp_dir, frame_dir=frame_dir,
                          bilateral_filter=bilateral_filter,
                          l2_gradient=l2_gradient,
                          color=color)
    print("[+] Generating output.mp4...")
    os.system("ffmpeg -pattern_type glob -i " + tmp_dir +
              "/\"*.png\" tmp_video.mp4 -y")
    os.system("ffmpeg -i audio.aac -i tmp_video.mp4 " + output + " -y")

    if clean_up:
        os.system("rm -rf " + tmp_dir)  # This is OS dependent!
        os.system("rm -rf " + frame_dir)
        os.system("rm tmp_video.mp4")
        print("[+] Cleaned up directories")


if __name__ == "__main__":
    generate_video(video_name="./nootnoot.mp4", clean_up=False,
                   multiplier=10, thread_enabled=False, thread_count=0,
                   color="#000000", output="out.mp4")
