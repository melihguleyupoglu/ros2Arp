import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
import time


class MapPublisherNode(Node):
    def __init__(self):
        super().__init__('map_publisher_node')
        self.publisher = self.create_publisher(OccupancyGrid, 'map', 10)
        self.timer = self.create_timer(0.5, self.publish_map)

    def publish_map(self):
        msg = OccupancyGrid()

        # Header bilgilerini doldurun
        # Şimdiki zamanı saniye cinsinden al
        msg.header.stamp.sec = int(time.time())
        msg.header.stamp.nanosec = 0  # Nanosaniyeleri 0 olarak ayarla
        msg.header.frame_id = "map"  # Çerçeve kimliğini 'map' olarak ayarla

        # Info alanını doldurun
        # Haritanın yüklendiği zamanı belirtin
        msg.info.map_load_time.sec = int(time.time())
        msg.info.map_load_time.nanosec = 0
        msg.info.resolution = 1.0
        msg.info.width = 100
        msg.info.height = 100

        # Haritanın orijinini belirtin (örneğin, (0, 0, 0))
        msg.info.origin.position.x = 0.0
        msg.info.origin.position.y = 0.0
        msg.info.origin.position.z = 0.0
        msg.info.origin.orientation.x = 0.0
        msg.info.origin.orientation.y = 0.0
        msg.info.origin.orientation.z = 0.0
        msg.info.origin.orientation.w = 1.0

        # Harita verisini doldurun
        msg.data = [0] * (msg.info.width * msg.info.height)

        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    map_publisher_node = MapPublisherNode()
    map_publisher_node.publish_map()

    rclpy.spin(map_publisher_node)

    map_publisher_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
