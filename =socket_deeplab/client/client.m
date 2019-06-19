clc
clear

%data_all=[];%用于存储所有的数据
t = tcpip('219.224.168.100', 54377, 'Timeout', 60,'InputBufferSize',10240);%连接这个ip和这个端口的UDP服务器
%t.BytesAvailableFcnMode='byte'

while(1)
    fopen(t);
    fwrite(t,'/home/tony/app/deeplab_socket/data/00001.jpg');%发送一段数据给tcp服务器。服务器好知道matlab的ip和端口
    while(1) %轮询，直到有数据了再fread
        nBytes = get(t,'BytesAvailable');
        if nBytes>0
            break;
        end
    end
    receive = fread(t,nBytes);%读取tcp服务器传来的数据
    %fread(t);
    fclose(t);
    data=char(receive)'; %将ASCII码转换为str
    %data_all=[data_all;data];
    fprintf("%s\n",data);
    pause(1);
    figure;imshow(imread(data));
end

delete(t);
