
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

from warehouse_interfaces.action import Deliver


class DeliverClient(Node):

    def __init__(self):
        super().__init__('deliver_action_client')

        self.client = ActionClient(
            self,
            Deliver,
            'deliver'
        )

    def send_goal(self):

        goal = Deliver.Goal()

        goal.destination = 'Warehouse Zone B'
        goal.distance = 10.0
        goal.speed = 1.0

        self.get_logger().info('Waiting for action server...')

        self.client.wait_for_server()

        self.get_logger().info('Sending delivery goal')

        future = self.client.send_goal_async(
            goal,
            feedback_callback=self.feedback_callback
        )

        future.add_done_callback(
            self.goal_response_callback
        )

    def goal_response_callback(self, future):

        self.goal_handle = future.result()

        if not self.goal_handle.accepted:
            self.get_logger().error('Goal rejected')
            rclpy.shutdown()
            return

        self.get_logger().info('Goal accepted')

        result_future = self.goal_handle.get_result_async()

        result_future.add_done_callback(
            self.result_callback
        )

    def feedback_callback(self, feedback_msg):

        feedback = feedback_msg.feedback

        self.get_logger().info(
            f'Remaining distance: '
            f'{feedback.remaining_distance:.2f} m, '
            f'Progress: {feedback.percent:.1f}%'
        )

    def result_callback(self, future):

        result = future.result().result

        self.get_logger().info(
            f'Success: {result.success}, '
            f'Time taken: {result.time_taken:.2f} seconds'
        )

        rclpy.shutdown()


def main(args=None):

    rclpy.init(args=args)

    node = DeliverClient()

    node.send_goal()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        if rclpy.ok():
            rclpy.shutdown()

        node.destroy_node()


if __name__ == '__main__':
    main()
