import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
#from cv2 import aruco
 
class ImagePublisher(Node):
  
  def __init__(self):
    super().__init__('image_publisher')
    self.publisher_ = self.create_publisher(Image, 'video_frames', 10)
    timer_period = 0.1  # seconds
    self.timer = self.create_timer(timer_period, self.timer_callback)
    self.cap = cv2.VideoCapture(0)
    self.br = CvBridge()

    ### --- aruco設定 --- ###
    #self.dict_aruco = aruco.Dictionary_get(aruco.DICT_4X4_50)
    #self.parameters = aruco.DetectorParameters_create()
   
  def timer_callback(self):
    ret, frame = self.cap.read()
          
    if ret == True:
      """
      frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      frame_edge = cv2.Canny(frame_gray, threshold1=100, threshold2=200)"""
      """gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

      corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, self.dict_aruco, parameters=self.parameters)

      frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)"""
      dst = cv2.resize(frame, (160,120))
      self.publisher_.publish(self.br.cv2_to_imgmsg(dst))
 
      self.get_logger().info('Publishing video frame')
  
def main(args=None):
  
  rclpy.init(args=args)
  image_publisher = ImagePublisher()
  rclpy.spin(image_publisher)
  
  image_publisher.destroy_node()
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()
