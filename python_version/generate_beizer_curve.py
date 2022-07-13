"""
The main code that turns image into bezier curves was from
https://github.com/kevinjycui/DesmosBezierRenderer
Huge and special thanks to https://github.com/kevinjycui for this fun project.
"""


import numpy as np
import potrace
import cv2


def get_trace(data):
    for i in range(len(data)):
        data[i][data[i] > 1] = 1
    bmp = potrace.Bitmap(data)
    path = bmp.trace(2, potrace.TURNPOLICY_MINORITY, 1.0, 1, .5)
    return path


def get_curve(filename, bilateral_filter=False, l2_gradient=False):
    path = get_trace(get_contours(filename))
    curves_list = list()
    for curve in path.curves:
        segments = curve.segments
        start = curve.start_point
        for segment in segments:
            x0, y0 = start
            if segment.is_corner:
                x1, y1 = segment.c
                x2, y2 = segment.end_point
                # Append those points as list
                curves_list.append(((x0, y0), (x1, y1), (x2, y2), (x0, y0)))

            else:
                x1, y1 = segment.c1
                x2, y2 = segment.c2
                x3, y3 = segment.end_point
                curves_list.append(((x0, y0), (x1, y1), (x2, y2), (x3, y3)))
            start = segment.end_point
    return curves_list


def get_contours(image, nudge=.33, bilateral_filter=False, l2_gradient=False):
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if bilateral_filter:
        median = max(10, min(245, np.median(gray)))
        lower = int(max(0, (1 - nudge) * median))
        upper = int(min(255, (1 + nudge) * median))
        filtered = cv2.bilateralFilter(gray, 5, 50, 50)
        edged = cv2.Canny(filtered, lower, upper, L2gradient=l2_gradient)
    else:
        edged = cv2.Canny(gray, 30, 200)

    return edged[::-1]
