import glob



filelist = (glob.glob('C:/Users/Lamont/FWD/Aviation/climo/metars/2019/dfwobs/dfwobs.*'))
for filelist in filelist:
    fname = filelist
    exec(open("C:/Users/Lamont/FWD/Aviation/climo/code/convert_mtr.py").read())
    #print(fname)
    #break 