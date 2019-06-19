# Minor change
add run_all.m and run_subdir.m to handle image datasets.
cloned from https://github.com/donglaiw/TSP/tree/master/optical_flow_celiu

# Original Readme
The C++ package has been successfully compiled in the x64 Windows and x64 Linux. The compiler I used in Windows is Visual Studio, and the compiler in Linux is g++. 

Before compiling, please check project.h file in subfolder "mex". You don't have to do anything if you use Windows. If you use Mac Os or Linux, please uncomment the line 
#define _LINUX_MAC
and you should be good to go. The precompiled dll's for win 64 and Mac Os 10 Lion are included.

In Matlab, after you configure mex appropriately, change directory to "mex" and run the following command:
 
mex Coarse2FineTwoFrames.cpp OpticalFlow.cpp GaussianPyramid.cpp

Now you should be able to have the dll that is compatible with your OS. Have fun!

Ce Liu
Microsoft Research New England
