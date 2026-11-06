import time
import rclpy
from rclpy.node import Node
from rclpy.executors import ExternalShutdownException
from std_msgs.msg import String

N = 200  # 몇 번 보낼까


class Ping(Node):
    def __init__(self):
        super().__init__('ping')
        self.pub = self.create_publisher(String, '/ping', 10)
        self.create_subscription(String, '/pong', self.on_pong, 10)
        self.create_timer(0.1, self.send)  # 초당 10번
        self.seq, self.rtts = 0, {}

    def send(self):
        if self.seq >= N:
            return
        self.pub.publish(String(data=f"{self.seq},{time.monotonic()}"))
        self.seq += 1
        if self.seq == N:
            self.create_timer(2.0, self.report)

    def on_pong(self, msg):
        seq, t0 = msg.data.split(",")
        self.rtts[int(seq)] = (time.monotonic() - float(t0)) * 1000

    def report(self):
        v = sorted(self.rtts.values())
        if v:
            p95 = v[int(0.95 * (len(v) - 1))]
            print(f"loss {100*(N-len(v))/N:.1f}% mean {sum(v)/len(v):.1f}ms p95 {p95:.1f}ms")
        else:
            print("no reply")
        rclpy.shutdown()


def main():
    rclpy.init()
    try:
        rclpy.spin(Ping())
    except (ExternalShutdownException, KeyboardInterrupt):
        pass


if __name__ == '__main__':
    main()