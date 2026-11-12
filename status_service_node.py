
import rclpy
from rclpy.node import Node

from warehouse_interfaces.msg import DeliveryStatus
from warehouse_interfaces.srv import LoadPackage


class WarehouseNode(Node):

    def __init__(self):
        super().__init__('warehouse_node')

        self.package_count = 0

        self.publisher = self.create_publisher(
            DeliveryStatus,
            '/delivery_status',
            10
        )

        self.service = self.create_service(
            LoadPackage,
            '/load_package',
            self.load_package_callback
        )

        self.timer = self.create_timer(1.0, self.publish_status)

        self.get_logger().info('Warehouse node started')

    def publish_status(self):

        msg = DeliveryStatus()

        msg.robot_id = 'ROBOT_01'
        msg.package_count = self.package_count
        msg.battery = 100.0
        msg.state = DeliveryStatus.STATE_IDLE

        self.publisher.publish(msg)

        self.get_logger().info(
            f'Robot: {msg.robot_id}, '
            f'Packages: {msg.package_count}, '
            f'Battery: {msg.battery}%'
        )

    def load_package_callback(self, request, response):

        if request.weight > 10.0:
            response.accepted = False
            response.message = 'Rejected: Package weight exceeds 10 kg'

        elif self.package_count >= 5:
            response.accepted = False
            response.message = 'Rejected: Maximum package limit reached'

        else:
            self.package_count += 1
            response.accepted = True
            response.message = 'Package accepted successfully'

        response.total_packages = self.package_count

        self.get_logger().info(response.message)

        return response


def main(args=None):

    rclpy.init(args=args)

    node = WarehouseNode()

    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
