import rclpy
from rclpy.node import Node
from sensor_msgs.msg import FluidPressure
from rov_msgs.msg import RovDepth
from pressure_reader.ms5837 import MS5837_30BA as Bar30
from pressure_reader.ms5837 import DENSITY_FRESHWATER, DENSITY_SALTWATER
from pressure_reader.ms5837 import UNITS_mbar

class Bar30Node(Node):
    def __init__(self):
        super().__init__('imu_node')

        self.declare_parameter('i2c_bus', 6)
        self.declare_parameter('is_saltwater', True)

        i2c_bus = self.get_parameter('i2c_bus').value
        is_saltwater = self.get_parameter('is_saltwater').value

        self.sensor = Bar30(i2c_bus)
        if (is_saltwater):
            self.sensor.setFluidDensity(DENSITY_SALTWATER)
        else:
            self.sensor.setFluidDensity(DENSITY_FRESHWATER)
        self.sensor.init()

        self.depth_publisher = self.create_publisher(RovDepth, "depth", 1)
        self.pressure_publisher = self.create_publisher(FluidPressure, "pressure", 1)
        self.timer = self.create_timer(0.005, self.timer_callback)

    def timer_callback(self):
        self.sensor.read()
        print(self.sensor.pressure())
        pressure_msg = FluidPressure()
        pressure_msg.header.stamp = self.get_clock().now().to_msg()
        pressure_msg.fluid_pressure = self.sensor.pressure(UNITS_mbar)
        self.pressure_publisher.publish(pressure_msg)

        depth_msg = RovDepth()
        depth_msg.header.stamp = self.get_clock().now().to_msg()
        depth_msg.depth = self.sensor.depth()
        self.depth_publisher.publish(depth_msg)


def main(args=None):
    rclpy.init(args=args)
    node = Bar30Node()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
