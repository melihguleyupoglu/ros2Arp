#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
from geometry_msgs.msg import Twist
import heapq


class PathPlanningNode(Node):
    def __init__(self):
        super().__init__('path_planning_node')
        self.subscription = self.create_subscription(
            OccupancyGrid,
            'map',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.get_logger().info('s.a')
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        path = self.a_star_algorithm(msg, tuple([0, 0]), tuple(
            [10, 10]))  # listeyi tuple'a dönüştür
        self.get_logger().info('Path: "%s"' % path)
        self.follow_path(path)

    def heuristic(self, a, b):
        return abs(b[0] - a[0]) + abs(b[1] - a[1])

    def a_star_algorithm(self, occupancy_grid, start, goal):
        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0),
                     (1, 1), (1, -1), (-1, 1), (-1, -1)]
        close_set = set()
        came_from = {}
        gscore = {start: 0}
        fscore = {start: self.heuristic(start, goal)}
        oheap = []

        heapq.heappush(oheap, (fscore[start], start))

        while oheap:
            current = heapq.heappop(oheap)[1]

            if current == goal:
                data = []
                while current in came_from:
                    data.append(current)
                    current = came_from[current]
                return data

            close_set.add(current)
            for i, j in neighbors:
                neighbor = current[0] + i, current[1] + j
                tentative_g_score = gscore[current] + \
                    self.heuristic(current, neighbor)
                if 0 <= neighbor[0] < occupancy_grid.info.width:
                    if 0 <= neighbor[1] < occupancy_grid.info.height:
                        # Değişiklik burada
                        if occupancy_grid.data[neighbor[0] * occupancy_grid.info.width + neighbor[1]] == 1:
                            continue
                    else:
                        # grid bound y walls
                        continue
                else:
                    # grid bound x walls
                    continue

                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue

                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + \
                        self.heuristic(neighbor, goal)
                    heapq.heappush(oheap, (fscore[neighbor], neighbor))

        return False

    def follow_path(self, path):
        for i in range(len(path) - 1):
            twist = Twist()
            dx = path[i+1][0] - path[i][0]  # x yönündeki değişim
            dy = path[i+1][1] - path[i][1]  # y yönündeki değişim

            # Hızı, hedef noktaya olan mesafeye göre ayarla
            twist.linear.x = float(dx)
            twist.linear.y = float(dy)

            self.publisher.publish(twist)


def main(args=None):
    rclpy.init(args=args)

    path_planning_node = PathPlanningNode()

    rclpy.spin(path_planning_node)

    path_planning_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
