function run_subdir(input_dir, save_dir, para)
%RUN_SUBDIR 此处显示有关此函数的摘要
%   此处显示详细说明
if ~exist(save_dir,'dir')
    mkdir(save_dir)
end
fprintf('run in %s\n',input_dir);
imgs = fullfile(input_dir,'*.jpg');
imgs = dir(imgs);
for i = 2 : length(imgs)
    im1_name = imgs(i-1).name;
    im2_name = imgs(i).name;
    flow_name = [im1_name(1:strfind(im1_name,'.')-1) '_' im2_name(1:strfind(im2_name,'.')-1) '_flow.jpg'];
    
    fprintf('run on %d-%d/%d\n',i-1,i, length(imgs));
    fprintf('a: %s\n',im1_name);
    fprintf('b: %s\n', im2_name);
    fprintf('flow: %s\n', fullfile(flow_name));
    
    im1 = im2double(imread(fullfile(input_dir, im1_name)));
    im2 = im2double(imread(fullfile(input_dir, im2_name)));
    tic
    [vx,vy,warpI2] = Coarse2FineTwoFrames(im1,im2,para);
    toc
    %clear flow;
    flow(:,:,1) = vx;
    flow(:,:,2) = vy;
    imflow = flowToColor(flow);
    
    %figure;imshow(im1);
    %figure;imshow(im2);
    %figure;imshow(imflow);
    
    imwrite(imflow,fullfile(save_dir, flow_name),'quality',100);
end % for

end % function

