import dis_wrapper
fc = open("test.py", "r").read()
tmp = dis_wrapper.get_str(fc)

import parse_dis
parsed = parse_dis.parse(tmp)

import pre_process
pre_processed = pre_process.pre_process(parsed)
print(pre_processed)

import output
out_str = output.tups_to_str(pre_processed)
print(out_str)
