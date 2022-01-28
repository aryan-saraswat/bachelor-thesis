from vdb_interface import VdbInterface
from lsf_interface import LsfInterface
from pprint import pprint

vdb = VdbInterface()
lsf = LsfInterface()
lecture_name = "Mathematics I1"
# lecture_name = "Fundamentals of Computer Engineering 1"

vdb_fce = vdb.find_lecture_by_name(lecture_name)
lsf_fce = lsf.find_lecture_by_name(lecture_name)

pprint(lsf_fce)
print('\n')
pprint(vdb_fce)