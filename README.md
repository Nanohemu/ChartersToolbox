# ChartersToolbox
基于python的DynaMaker xml谱面操作工具

反正差不多是会用的人不需要，需要的人不会用。CtrlCV的功能没写，判断重复和写节点我嫌麻烦。但是可以通过delay函数先移动了再打开输出xml文件把那一块粘贴回原文件，还可以mirror一下再粘，摸鱼写（画）谱专用。

1.把你的谱面xml文件放到程序所在的文件夹下面

2.用文本编辑器打开main.py，把文件名改了，根据需要的功能改改（注释写的就那样，看不懂可以找我，反正也就我自己用）

3.保存main.py，在程序目录下打开终端`python main.py`，得到输出xml文件

主要功能：

- `delay_node_text(nodelist, d)`：nodelist参考main.py和注释来匹配的节点的某个数值属性（一般也就m_id、m_subId、m_time），然后加上d（d是负数就相当于减小）

- `mirror_node_pos(pos_list, size_list)`：先参考注释把需要镜像的节点的m_position匹配成pos_list，m_width匹配称size_list，然后一起传进去，底面的note会左右镜像，侧面的note会上下镜像

ps:没错，炸药unrank的BPM=RT Hard ∞整活谱就是我写的
