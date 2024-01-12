#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from colored import fg

color = fg('#008000')
color_info = fg('#000080')

def log(iteration, total, suffix='', fill='█'):
    """
    Print
    """
    length = 30
    percent = ('{0:.1f}').format(100 * (iteration / float(total)))
    fillLength = int(length * iteration // total)
    bar = fill * fillLength + '-' * (length - fillLength)
    print(f'{color}\r%s | {color_info}%s%%{color} %s' % (bar, percent, suffix), end='\r')
    if iteration == total:
        print()