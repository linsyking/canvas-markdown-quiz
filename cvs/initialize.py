#!/usr/bin/env python3
'''
@Author: King
@Date: 2022-09-01 11-33-47
@Email: linsy_king@sjtu.edu.cn
@Url: https://yydbxx.cn
'''

import yaml
import os
from os import listdir
from os.path import isfile, join
from pick import pick
from canvasapi import Canvas
from getpass import getpass


def create_conf(rcpaths):
    # First ask for confirm
    o_opt_rcpath = rcpaths[:3] + ["Customize"]
    o_rcpath, _ = pick(
        o_opt_rcpath, 'Where do you want to save your config file?')
    if o_rcpath == "Customize":
        op = input("Please enter your preferred directory:")
        if not os.path.exists(op):
            print("Not a directory, aborting...")
            exit(0)
        o_rrc = join(op, ".cvsrc")
    else:
        o_rrc = join(o_rcpath, ".cvsrc")

    # Write conf
    print("\nNow I want to save your canvas API_URL and API_KEY.")

    print("API_URL is a url link like https://xxxcanvas.com.")

    print("API_KEY is a token which can be generated on your canvas website settings.\n")

    api_url = input("Canvs API URL:")
    api_key = getpass("Canvs API KEY:")
    canvas = Canvas(api_url, api_key)

    alc_ta = canvas.get_courses(enrollment_type="ta")
    alc_tea = canvas.get_courses(enrollment_type="teacher")
    alc = []
    alc_id = []

    for course in alc_ta:
        alc.append(course.name)
        alc_id.append(course.id)

    for course in alc_tea:
        alc.append(course.name)
        alc_id.append(course.id)

    _, t_course_id = pick(
        alc, 'Which course do you want to use to submit quizzes?')

    c_id = alc_id[t_course_id]

    y_obj = {
        "api_url": api_url,
        "api_key": api_key,
        "course_id": c_id
    }

    with open(o_rrc, "w") as f:
        yaml.safe_dump(y_obj, f)

    return o_rrc


def find_config_file():
    cur_path = os.getcwd()
    rcpath = ""
    all_rcpaths = []
    while cur_path != os.path.dirname(cur_path):
        all_rcpaths.append(cur_path)
        onlyfiles = [f for f in listdir(cur_path) if isfile(join(cur_path, f))]
        if ".cvsrc" in onlyfiles:
            rcpath = join(cur_path, ".cvsrc")
            break
        cur_path = os.path.dirname(cur_path)
    if rcpath == "":
        print("No config file(.cvsrc) found, initializing...")
        return create_conf(all_rcpaths)
    else:
        return rcpath


def init():
    rcpath = find_config_file()
    with open(rcpath, "r") as f:
        m_f_c = yaml.safe_load(f)
    if "api_url" in m_f_c and "api_key" in m_f_c and "course_id" in m_f_c:
        opt = {}
        if "options" in m_f_c:
            opt = m_f_c["options"]
        return m_f_c["api_url"], m_f_c["api_key"], m_f_c["course_id"], opt
    else:
        raise RuntimeError("Config file is not correct.")

