
import time

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

from warehouse_interfaces.action import Deliver


class DeliverServer(Node):

    def __init__(self):
        super().__init__('deliver_action_server')

        self._action_server = ActionServer(
            self,
            Deliver,
            'deliver',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            callback_group=ReentrantCallbackGroup()
        )

        self.get_logger().info('Deliver action server started')

    def goal_callback(self, goal_request):

        if (not goal_request.destination.strip()
                or goal_request.distance <= 0.0
                or goal_request.speed <= 0.0):

            self.get_logger().warning('Invalid delivery goal')
            return GoalResponse.REJECT

        self.get_logger().info('Delivery goal accepted')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):

        self.get_logger().info('Cancel request received')
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):

        goal = goal_handle.request

        remaining = goal.distance
        start_time = time.monotonic()

        feedback = Deliver.Feedback()

        while remaining > 0.0:

            if goal_handle.is_cancel_requested:

                goal_handle.canceled()

                result = Deliver.Result()
                result.success = False
                result.time_taken = time.monotonic() - start_time

                self.get_logger().warning('Delivery cancelled')

                return result

            time.sleep(0.5)

            remaining = max(
                0.0,
                remaining - goal.speed * 0.5
            )

            feedback.remaining_distance = float(remaining)

            feedback.percent = (
                (goal.distance - remaining) / goal.distance
            ) * 100.0

            goal_handle.publish_feedback(feedback)

            self.get_logger().info(
                f'Remaining: {remaining:.2f} m, '
                f'Progress: {feedback.percent:.1f}%'
            )

        goal_handle.succeed()

        result = Deliver.Result()
        result.success = True
        result.time_taken = time.monotonic() - start_time

        self.get_logger().info(
            f'Delivery completed at {goal.destination}'
        )

        return result


def main(args=None):

    rclpy.init(args=args)

    node = DeliverServer()

    executor = MultiThreadedExecutor()
    executor.add_node(node)

    try:
        executor.spin()
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

