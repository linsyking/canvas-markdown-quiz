from . import generate as cg
from . import initialize
import sys

def main():
    if len(sys.argv) != 2:
        print("usage: cvs-makequiz <md filepath>")
        exit(0)
    url, key, cid, opt = initialize.init()
    qm = cg.quiz_maker(url, key, opt)
    qm.set_courseid(cid)
    qm.init_by_file_path(sys.argv[1])
    qm.create_quiz()
