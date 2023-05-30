import sys

from robot_interfaces.srv import RobotCommand
import rclpy
from rclpy.node import Node


class RobotClient(Node):

    def __init__(self):
        super().__init__('robot_client')
        self.client = self.create_client(RobotCommand, 'robot_command')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.request = RobotCommand.Request()

    def send_request(self, order):
        self.request.dist = order
        self.future = self.client.call_async(self.request)
        
def main(args=None):
    rclpy.init(args=args)
    robot_client = RobotClient()
    order = input('距離 : ')
    robot_client.send_request(int(order))

    while rclpy.ok():
        rclpy.spin_once(robot_client)
        if robot_client.future.done():
            try:
                response = robot_client.future.result()
            except Exception as e:
                robot_client.get_logger().info(f'Failed {e}')
            else:
                robot_client.get_logger().info(f'\n request : {robot_client.request.dist} -> reponse : {response.done}')
                break
    rclpy.shutdown()


if __name__ == '__main__':
    main()