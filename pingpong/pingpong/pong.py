import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class Pong(Node):
    def __init__(self):
        super().__init__('pong')
        self.pub = self.create_publisher(String, '/pong', 10)
        self.create_subscription(String, '/ping', self.pub.publish, 10)


def main():
    rclpy.init()
    try:
        rclpy.spin(Pong())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()