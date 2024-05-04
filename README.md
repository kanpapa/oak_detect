# oak_detect

## Overview
OAK-D-LITEを使用して、ボトルの方向を向くようにkobukiを回転する実験プログラムです。

## Setup
1. ROS2 humbleでkobukiが動作する環境を用意する。
1. OAK-D-LITEのROSパッケージをインストールする。
    ```
    sudo apt install ros-humble-depthai-ros
    ```
1. OAK-D-LITEのデバイスの設定を行う。
    ```
    echo 'SUBSYSTEM=="usb", ATTRS{idVendor}=="03e7", MODE="0666"' | sudo tee /etc/udev/rules.d/80-movidius.rules
    sudo udevadm control --reload-rules && sudo udevadm trigger
    ```
1. ワークスペースにoak_detectをgit cloneしてbuildする。
    ```
    cd ~/kobuki_ws/src
    git clone https://github.com/kanpapa/oak_detect.git
    cd ~/kobuki_ws
    colcon build --packages-select oak_detect
    ```

## Try
1. kobukiのノードを実行する。
    ```
    ros2 launch kobuki_node kobuki_node-launch.py
    ```
1. OAK-D-LITEのMobileNet SSDノードを実行する。
    ```
    ros2 launch depthai_examples mobile_publisher.launch.py camera_model:=OAK-D-LITE
    ```
1. oak_detectのノードを実行する。
    ```
    ros2 run oak_detect oak_detect
    ```
1. ペットボトルをOAK-D-LITEに向けて左右に動かしてみる。

## Reference
MobileNetはメモリ量が限られている環境でも利用できるCNNです。 

OAK-D-LITEカメラに搭載されているMobileNetは、一般的な物体検出に使用されます。MobileNet v2 SSD (Single Shot Multibox Detector) モデルを使用しており、20種類の一般的なオブジェクトを認識することができます。

        #mobilenet object list
        #0: background
        #1: aeroplane
        #2: bicycle
        #3: bird
        #4: boat
        #5: bottle
        #6: bus
        #7: car
        #8: cat
        #9: chair
        #10: cow
        #11: diningtable
        #12: dog
        #13: horse
        #14: motorbike
        #15: person
        #16: pottedplant
        #17: sheep
        #18: sofa
        #19: train
        #20: tvmonitor
