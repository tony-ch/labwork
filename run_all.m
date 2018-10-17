clear
addpath('mex');
%% set optical flow parameters (see Coarse2FineTwoFrames.m for the definition of the parameters)
alpha = 0.012;
ratio = 0.75;
minWidth = 20;
nOuterFPIterations = 7;
nInnerFPIterations = 1;
nSORIterations = 30;

para = [alpha,ratio,minWidth,nOuterFPIterations,nInnerFPIterations,nSORIterations];

%% set data path
input_dir = './data';
res_dir = './res';
if ~exist(res_dir,'dir')
    mkdir(res_dir)
end

%% main loop
subdir = dir(input_dir);

for i = 1 : length(subdir)
    if( isequal( subdir( i ).name, '.' )||...
        isequal( subdir( i ).name, '..') )
        continue;
    end
    sub_dir = fullfile(input_dir,subdir(i).name);
    save_dir = fullfile(res_dir,subdir(i).name);
    run_subdir(sub_dir, save_dir, para);
end
    



