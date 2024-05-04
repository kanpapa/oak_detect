#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from vision_msgs.msg import Detection2DArray
import math

class OakDetect(Node):

    def __init__(self):
        super().__init__('oak_detect')

        # クラス変数の定義と初期化        
        self.height = 300
        self.width = 300

        #self.roll=0
        #self.pitch=0
        #self.yaw=0
        #self.yaw_increment=0
        #self.pitch_increment=0
        #self.pose = Pose()

        self.angular_increment=0
        self.twist = Twist()

        # publisherを作成
        #self.publisher_ = self.create_publisher(Pose, '/body_pose', 10)
        self.publisher_ = self.create_publisher(Twist, '/commands/velocity', 10)
        
        # Subscriberの作成　トピックがきたらlistener_callbackを呼ぶ
        self.subscription = self.create_subscription(Detection2DArray, '/color/mobilenet_detections', self.listener_callback, 10)
        self.subscription  # prevent unused variable warning 未使用変数の警告を防ぐ

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

        # vision_msgs/Detection2D
        #   std_msgs/Header header
        #   vision_msgs/ObjectHypothesisWithPose[] results
        #   vision_msgs/BoundingBox2D bbox

        # vision_msgs/Detection2DArray
        #   std_msgs/Header header
        #   vision_msgs/Detection2D[] detections

    def toward_obj(self, obj_class, obj_list):
        #self.yaw_increment = 0
        #self.pitch_increment = 0
        self.angular_increment = 0.0
        
        for i in obj_list:
            bb = i.bbox         # BoundingBoxes2D
            #si = i.source_img  # SourceImage
            #r = i.results       # Results
            #rr = r[0] #RealResults
            #print(rr.class_id)
            #print(i.id)
            if(i.id == obj_class):
                print(11111)
                #self.yaw_increment = (self.width/2 - bb.center.position.x)*0.0002       # yaw:   Z方向の回転量
                #self.pitch_increment = -(self.height/2 - bb.center.position.y)*0.0002   # Pitch: Y方向の回転量

                self.angular_increment = (self.width/2 - bb.center.position.x)*0.01   # 左右の回転量
                print(self.angular_increment)

                self.twist.angular.z = self.angular_increment
                self.publisher_.publish(self.twist)      # 計算したangular.zをpublish
            
            #else:
                #yaw_increment=0

    def listener_callback(self, data):
        bounding_boxes = data                   # Detection2DArray
        detections = bounding_boxes.detections  # Detection2D[]
        self.toward_obj('5', detections)        # #5: bottle があったらその方向に向くようにposeを調整
        #toward_obj('cup',a)
        #print(a[0])

def main(args=None):
    print('Hi from oak_detect.')
    rclpy.init(args=args)
    oak_detect = OakDetect()
    rclpy.spin(oak_detect)
    oak_detect.destroy_node()
    rclpy.shutdown()
 
if __name__ == '__main__':
    main()
