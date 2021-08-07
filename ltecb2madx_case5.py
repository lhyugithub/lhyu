from __future__ import print_function
#import pylatt as latt
import numpy as np
import sys
import os


print("sys.argv=", sys.argv)
print('len(sys.argv)=',len(sys.argv))



if len(sys.argv)==2:
        fn=sys.argv[1]
elif len(sys.argv)==1:
        fn="cb2NSLS2CB65pm_cb0_1cell"#.lte"


print('fn=', fn)

#fn="cb2NSLS2CB65pm_cb0_1cell"
def line(le):
    ele=le.split('=')[1]
    return le.split('=')[0]+"="+ele.replace('(','(').replace('&','').replace('MA1,','')

def CSBEND(le):
    ele=le.split(':')[0]+le.split(':')[1].replace(' CSBEND,',':SBEND, ').replace(',  N_KICKS= 40','').replace('\n',';\n')
    return ele

def csbend(le):
    ele=le.split(':')[0]+le.split(':')[1].replace(' csbend,',':SBEND, ').replace(',  N_KICKS= 40','').replace('\n',';\n')
    return ele
    ele=le.split(':')[0]+' = latt.bend("'+le.replace(':','",').replace('csbend,','').replace(',  N_KICKS= 40','').replace('CSBEND,','').replace('\n',',K1=0.0, K2=0.0)\n')
    return ele

def drif(le):
    ele=le.split(':')[0]+le.split(':')[1].replace(' EDRIFT,',':DRIFT,').replace(' drif,',':DRIFT,').replace('\n',';\n')
    return ele

def kick(le):
    ele=le.split(':')[0]+' = latt.kick("'+le.replace(':','",').replace('kick,','').replace('\n',')\n')
    return ele

def moni(le):
    ele=le.split(':')[0]+': HMONITOR,L=0.0;\n'
    #ele=le.split(':')[0]+le.split(':')[1].replace(' moni,',':HMONITOR,').replace('MALIGN,on_pass=0',':HMONITOR,L=0.0').replace('watch, filename="%s.w1", mode ="centroid"',':HMONITOR,L=0.0').replace('\n',';\n')
    return ele

def kquad(le):
    ele=le.split(':')[0]+le.split(':')[1].replace(' KQUAD,',':QUADRUPOLE,').replace(' kquad,',':QUADRUPOLE,').replace(',  N_KICKS= 40','').replace('\n',';\n')
    return ele
 
def kSext(le):
    ele=le.split(':')[0]+le.split(':')[1].replace(' KSEXT,',':SEXTUPOLE,').replace(' kSext,',':SEXTUPOLE,').replace(',  N_KICKS= 40','').replace('\n',';\n')
    return ele
    

for ik in [1]:
    verbose=False
#def txt2latt(fn,verbose=False):
    '''
    read nls2-ii control-system lattice format
    '''
    fid = open(fn+".lte",'r')
    a0 = fid.readlines()
    a1=[]
    fid.close()
    #list '&\n' between lines, and group if they are continuous.
    for i,le in enumerate(a0):
        if verbose:
            print('LN%3d: %s'%(i+3,le))
        ele=le.split(',')
        a1.append(ele)
    lamper=[ i for i,j in enumerate(a1) if '&\n' in j[-1]]
    lamper3=[]
    lampertmp=[lamper[0]]
    for i in range(1,len(lamper)+1):        
        if i<len(lamper) and lamper[i]==lamper[i-1]+1:
            lampertmp.append(lamper[i])
        elif i<len(lamper):
            lampertmp.append(lampertmp[-1]+1)
            lamper3.append(lampertmp)
            lampertmp=[lamper[i]]
            #print "i=",i, "lamper[i]=",lamper[i]
        else:
            lampertmp.append(lampertmp[-1]+1)
            lamper3.append(lampertmp)

    #join lines separated by '&\n' and remove '&\n'
    separator=','
    a2=[ separator.join([ n  for m in [ a1[i] for i in j ] for n in m]).replace('&\n,','') for j in lamper3[:-1]]        
    #a2=[ separator.join(np.sum([ a1[i] for i in j ])).replace('&\n,','') for j in lamper3[:-1]]        

    #inser lines without '&\n' back into list
    a3=[]
    k=0
    for i in range(len(lamper3)-1):
        for n in range(k,lamper3[i][0]): a3.append(separator.join(a1[n]))
        a3.append(a2[i])
        k=lamper3[i][-1]+1
    a4=a3+a0[lamper3[-2][-1]+1:-1]
    spt=''
    a5=[ spt.join(i) for i in a4]

    #text_file = open("junk101", "w")
    #for le in a5:
    #    text_file.write(le)
    #text_file.close()
    a=a5
    a[-1]=a[-1].replace(')',')')
    bl = []
    for i,le in enumerate(a):
        if verbose:
            print('LN%3d: %s'%(i+3,le))
        ele=le.split(':')        
        #if i==8:sys.exit(0)
        if len(ele)>1 and len(ele[1].split(',')[0].split())>0:
            #print "i=",i, "le=",le, "a[i]=",a[i]
            ele = le.split(':')[1].split(',')[0].split()[0]
            #print "ele=", ele
            if le.split()[0][0]=='!':
                le=le.replace('!','//',1)
            if ele =="csbend":
                t = csbend(le)
            elif 'CSBEND' in ele:
                t = CSBEND(le)
            elif ele == 'drif' or ele =='EDRIFT':
                t= drif(le)
            elif ele == 'kick':
                t= kick(le)
            elif ele == 'moni':
                t= moni(le)
            elif ele=='MALIGN':
                t= moni(le)
            elif ele=='watch':
                t= moni(le)
            elif ele=='WATCH':
                t= moni(le)
            elif ele == 'kquad' or ele =='KQUAD':
                t= kquad(le)
            elif ele == 'kSext' or ele =='KSEXT':
                t= kSext(le)
            elif ele == 'LINE':
                t= line(le)
            else:
                #print('unknown element type!')
                t=[]
            if t!=[]: bl.append(t)            
        else:
            print ("2. i=",i, "le=",le, "a[i]=",a[i])
            if len(le.split())>0:
                #print "2.1 le.split()=",le.split(),'\n',le
                if le.split()[0][0]=='!':
                    le=le.replace('!','//',1)
                #print "le.split(',')=",le.split(',')
                if le.split(',')[-1]==' &\n':
                    #print "2.2 le.split(',')=",le.split(',')
                    le= le.replace('&','')
                if ')' in le.split(',')[-1]  and '\n' in le.split(',')[-1] :
                        le= le.replace(')',');')
                        #print "2.3 le=",le, 'le.split(',')[-1][-2:]=',le.split(',')[-1][-2:]
                t=le
            else:
                t=le
            bl.append(t)
    #bl=np.insert(bl,0,'import pylatt as latt\n\n')


    #bl=np.insert(bl,-2,word_list)
    text_file = open(fn+".madx", "w")
    for i,le in enumerate(bl):
        text_file.write(le)
    text_file.close()
    print('madx file saved as '+fn+'.madx')
    
os.system('cat  madx_case5_tail >>'+' '+fn+'.madx')    
