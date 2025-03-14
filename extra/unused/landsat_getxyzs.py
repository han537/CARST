#import matplotlib;
import numpy;
import os;
import pylab;
import scipy;
import scipy.linalg;
import subprocess;
import sys;

PIXEL_SIZE=15;

name=sys.argv[1];
step=int(sys.argv[2]);
width0=int(sys.argv[3]);
length0=int(sys.argv[4]);
ul_lon=float(sys.argv[5]);
ul_lat=float(sys.argv[6]);

cmd="\nsed -e '/\*/d' "+name+" > temp\nmv "+name+" "+name+".old\nmv temp "+name+"\n";
subprocess.call(cmd,shell=True);
indat=scipy.loadtxt(name);

rwin=step;
awin=step;
wsamp=1;

da_e=PIXEL_SIZE*100;	#az pixel size at earth surface, cm    
dr_g=PIXEL_SIZE*100;	#ground pixel size in range direction, cm

x1ind=scipy.matrix([indat[:,0]],scipy.int32).conj().transpose();
dx=scipy.matrix([indat[:,1]]).conj().transpose();
y1ind=scipy.matrix([indat[:,2]],scipy.int32).conj().transpose();
dy=scipy.matrix([indat[:,3]]).conj().transpose();
snr=scipy.matrix([indat[:,4]]).conj().transpose();
c11=scipy.matrix([scipy.sqrt(indat[:,5])]).conj().transpose() #1 sigma drng
c22=scipy.matrix([scipy.sqrt(indat[:,6])]).conj().transpose() #1 sigma dazo

x1=x1ind * dr_g;
dx=dx * dr_g;
y1=y1ind * da_e;
dy=dy * da_e;
c11=c11 * dr_g; #1 sigma drng
c22=c22 * da_e; #1 sigma dazo
x2=x1+dx;
y2=y1+dy;

rlooks=rwin/wsamp;
alooks=awin/wsamp;

width1=scipy.floor(width0/rlooks);
length1=scipy.floor(length0/alooks);
[xg,yg]=scipy.meshgrid(scipy.arange(1,width1+1,1),scipy.arange(1,length1+1,1));
xg=xg*dr_g*rlooks/1e5;	#convert from pix to km
yg=yg*da_e*alooks/1e5;	#convert from pix to km

sigy_thresh=scipy.inf;	#cm
sigx_thresh=scipy.inf;	#cm
snr_thresh=0;		#(not log10)
mag_threshx=scipy.inf;	#cm
mag_threshy=scipy.inf;	#cm

#initial mask
c22good=scipy.matrix(pylab.find(c22<sigy_thresh)).conj().transpose();
c11good=scipy.matrix(pylab.find(c11<sigx_thresh)).conj().transpose();
snrgood=scipy.matrix(pylab.find(snr>snr_thresh)).conj().transpose();

good=scipy.matrix(scipy.unique(scipy.array(scipy.vstack((snrgood,c11good,c22good))))).conj().transpose();

x1good=x1[good].reshape(-1,1);
x1goodind=x1ind[good].reshape(-1,1);
y1good=y1[good].reshape(-1,1);
y1goodind=y1ind[good].reshape(-1,1);
x2good=x2[good].reshape(-1,1);
y2good=y2[good].reshape(-1,1);

#get and remove affine fit
good2=scipy.matrix(pylab.find(good<300000)).conj().transpose();

x1good=x1[good2].reshape(-1,1);
y1good=y1[good2].reshape(-1,1);
x2good=x2[good2].reshape(-1,1);
y2good=y2[good2].reshape(-1,1);

c0=scipy.matrix(scipy.zeros((scipy.size(good2)))).reshape(-1,1);
c1=scipy.matrix(scipy.ones((scipy.size(good2)))).reshape(-1,1);
n=c1.shape[0];

A=scipy.vstack((scipy.hstack((x1good,y1good,c0,c0,c1,c0)),scipy.hstack((c0,c0,x1good,y1good,c0,c1))));

b=scipy.vstack((x2good,y2good));

M=scipy.linalg.lstsq(A,b)[0];

pred=A*M;
res=pred-b;

# std() in python defaults to 0 degrees of freedom
resdev=res.std(axis=0,ddof=1);
q=pylab.find(abs(res)<1.5*resdev);
A1=A[q,];
b1=b[q];
M=scipy.linalg.lstsq(A1,b1)[0];
pred=A*M;

x1good=x1[good].reshape(-1,1);
x1goodind=x1ind[good].reshape(-1,1);
y1good=y1[good].reshape(-1,1);
y1goodind=y1ind[good].reshape(-1,1);
x2good=x2[good].reshape(-1,1);
y2good=y2[good].reshape(-1,1);

c0=scipy.matrix(scipy.zeros((scipy.size(good)))).reshape(-1,1);
c1=scipy.matrix(scipy.ones((scipy.size(good)))).reshape(-1,1);
n=c1.shape[0];

A=scipy.vstack((scipy.hstack((x1good,y1good,c0,c0,c1,c0)),scipy.hstack((c0,c0,x1good,y1good,c0,c1))));

b=scipy.vstack((x2good,y2good));

pred=A*M;

n=c1.shape[0];

res=pred-b;
resdx=res[0:n];
resdy=res[(n):(2*n)];

#remap into
newx=scipy.matrix(scipy.ceil(x1goodind / rlooks),scipy.int32);
newy=scipy.matrix(scipy.floor(y1goodind / alooks),scipy.int32);

vind=scipy.asarray((newy-1)*width1+newx,scipy.int32).reshape(-1);

temp=scipy.matrix(0*(scipy.arange(1,length1*width1+1,1))).conj().transpose();
temp[vind]=resdy;
dyg=temp.reshape(length1,width1);

temp=scipy.matrix(0*(scipy.arange(1,length1*width1+1,1))).conj().transpose();
temp[vind]=resdx;
dxg=temp.reshape(length1,width1);

#setup mask indicies
newx=scipy.matrix(scipy.ceil(x1ind/rlooks),scipy.int32);
newy=scipy.matrix(scipy.floor(y1ind/alooks),scipy.int32);
vind=scipy.asarray((newy-1)*width1+newx,scipy.int32).reshape(-1);
temp=scipy.NaN*scipy.matrix(scipy.arange(0,length1*width1,1)).conj().transpose();

#sigma_y mask
temp[vind]=c22;
sigyg=temp.reshape(length1,width1);
mask_sigy=scipy.zeros(dyg.shape);
mask_sigy[(sigyg>sigy_thresh)]=scipy.NaN;

#sigma_x mask
temp=scipy.NaN*scipy.matrix(scipy.arange(0,length1*width1,1)).conj().transpose();
temp[vind]=c11;
sigxg=temp.reshape(length1,width1);
mask_sigx=scipy.zeros(dxg.shape);
mask_sigx[(sigxg>sigx_thresh)]=scipy.NaN;

#SNR mask
temp=scipy.NaN*scipy.matrix(scipy.arange(0,length1*width1,1)).conj().transpose();
temp[vind]=snr;
snrg=temp.reshape(length1,width1);
mask_snr=scipy.zeros(dyg.shape);
mask_snr[(snrg<snr_thresh)]=scipy.NaN;

#mag mask y
mask_magy=scipy.zeros(dyg.shape);
mask_magy[abs(dyg)>mag_threshy]=scipy.NaN;

#mag mask x
mask_magx=scipy.zeros(dxg.shape);
mask_magx[abs(dxg)>mag_threshx]=scipy.NaN;

#final mask
mask_total=mask_snr+mask_sigy+mask_magy;
bad=scipy.isnan(mask_total);
dyg[bad]=scipy.NaN;

mask_total=mask_snr+mask_sigx+mask_magx;
bad=scipy.isnan(mask_total);
dxg[bad]=scipy.NaN;

x_step=PIXEL_SIZE*step;
y_step=-PIXEL_SIZE*step;

columns=scipy.arange(0,width1,1);
rows=scipy.arange(0,length1,1);

vect_utm_n=ul_lat+rows*y_step;
vect_utm_e=ul_long+columns*x_step;

[map_utm_e,map_utm_n]=scipy.meshgrid(vect_utm_e,vect_utm_n);
map_utm_n=scipy.flipud(map_utm_n);

cdir=os.getcwd();
cdir=cdir[cdir.rfind("/")+1:].strip();

column_utm_n=map_utm_n.reshape(scipy.size(map_utm_n,0)*scipy.size(map_utm_n,1),1);
column_utm_e=map_utm_e.reshape(scipy.size(map_utm_e,0)*scipy.size(map_utm_e,1),1);
column_dyg=scipy.flipud(dyg).reshape(scipy.size(dyg,0)*scipy.size(dyg,1),1);
column_dxg=scipy.flipud(dxg).reshape(scipy.size(dxg,0)*scipy.size(dxg,1),1);
column_snr=scipy.flipud(snrg).reshape(scipy.size(snrg,0)*scipy.size(snrg,1),1);
ampcor_optical_azimuth=scipy.concatenate((column_utm_e,column_utm_n,column_dyg,column_snr),axis=1);
ampcor_optical_range=scipy.concatenate((column_utm_e,column_utm_n,column_dxg,column_snr),axis=1);
scipy.savetxt("landsat_northxyz.txt",ampcor_optical_azimuth,delimiter=" ",fmt="%.1f");
scipy.savetxt("landsat_eastxyz.txt",ampcor_optical_range,delimiter=" ",fmt="%.1f");

#matplotlib.pyplot.imshow(scipy.array(dxg),interpolation='nearest',origin='lower');
#matplotlib.pyplot.show();
