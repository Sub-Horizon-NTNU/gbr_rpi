import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from smbus2 import SMBus
import time
import json

class IMUNode(Node):
    def __init__(self):
        super().__init__('imu_node')

        self.declare_parameter('imus', '[{"channel":0,"acc_addr":0x18,"gyro_addr":0x68,"topic":"/gbr/imu1","acc_scale":1367.0,"gyro_scale":16.4}, ...]')
        self.declare_parameter('i2c_bus', 6)
        self.declare_parameter('mux_addr', 0x70)

        i2c_bus = self.get_parameter('i2c_bus').value
        self.mux_addr = self.get_parameter('mux_addr').value
        imus_json = self.get_parameter('imus').value

        self.imu_configs = json.loads(imus_json)
        self.bus = SMBus(i2c_bus)

        for cfg in self.imu_configs:
            self.configure_imu(cfg)

        self.imu_publishers = {}
        for cfg in self.imu_configs:
            self.imu_publishers[cfg['topic']] = self.create_publisher(Imu, cfg['topic'], 1)
            time.sleep(0.1)

        self.timer = self.create_timer(0.005, self.timer_callback)

    def write_with_retry(self, addr, reg, value, retries=10):
        for attempt in range(retries):
            try:
                self.bus.write_byte_data(addr, reg, value)
                return True
            except OSError as e:
                if attempt == retries - 1:
                    raise
                time.sleep(0.05)
        return False

    def configure_imu(self, cfg):
        """Initializes IMU"""
        channel = cfg['channel']
        acc_addr = cfg['acc_addr']
        gyro_addr = cfg['gyro_addr']


        self.bus.write_byte(self.mux_addr, 1 << channel)
        time.sleep(0.1)

        # ---- Accelerometer ----
        self.write_with_retry(acc_addr, 0x7E, 0xB6)
        time.sleep(0.1)
        self.write_with_retry(acc_addr, 0x40, 0x28)
        time.sleep(0.1)
        self.write_with_retry(acc_addr, 0x41, 0x03)
        time.sleep(0.1)
        self.write_with_retry(acc_addr, 0x7D, 0x04)
        time.sleep(0.1)
        self.write_with_retry(acc_addr, 0x7C, 0x00)
        time.sleep(0.1)

        # ---- Gyro ----
        self.write_with_retry(gyro_addr, 0x7E, 0xB6)
        time.sleep(0.1)
        self.write_with_retry(gyro_addr, 0x0F, 0x04)
        time.sleep(0.1)

    def _read_accel(self, acc_addr, acc_scale):
        data = self.bus.read_i2c_block_data(acc_addr, 0x12, 6)
        x = (data[1] << 8) | data[0]
        y = (data[3] << 8) | data[2]
        z = (data[5] << 8) | data[4]
        if x >= 32768: x -= 65536
        if y >= 32768: y -= 65536
        if z >= 32768: z -= 65536
        ax = x / acc_scale * 9.80665
        ay = y / acc_scale * 9.80665
        az = z / acc_scale * 9.80665
        return ax, ay, az

    def _read_gyro(self, gyro_addr, gyro_scale):
        data = self.bus.read_i2c_block_data(gyro_addr, 0x02, 6)
        x = (data[1] << 8) | data[0]
        y = (data[3] << 8) | data[2]
        z = (data[5] << 8) | data[4]
        if x >= 32768: x -= 65536
        if y >= 32768: y -= 65536
        if z >= 32768: z -= 65536
        gx = x / gyro_scale * (3.141592653589793 / 180.0)
        gy = y / gyro_scale * (3.141592653589793 / 180.0)
        gz = z / gyro_scale * (3.141592653589793 / 180.0)
        return gx, gy, gz

    def timer_callback(self):
        for cfg in self.imu_configs:
            channel = cfg['channel']
            acc_addr = cfg['acc_addr']
            gyro_addr = cfg['gyro_addr']
            acc_scale = cfg['acc_scale']
            gyro_scale = cfg['gyro_scale']
            topic = cfg['topic']

            self.bus.write_byte(self.mux_addr, 1 << channel)

            ax, ay, az = self._read_accel(acc_addr, acc_scale)
            gx, gy, gz = self._read_gyro(gyro_addr, gyro_scale)

            msg = Imu()
            msg.header.stamp = self.get_clock().now().to_msg()
            msg.header.frame_id = f'imu_{channel}'
            msg.linear_acceleration.x = ax
            msg.linear_acceleration.y = ay
            msg.linear_acceleration.z = az
            msg.angular_velocity.x = gx
            msg.angular_velocity.y = gy
            msg.angular_velocity.z = gz

            self.imu_publishers[topic].publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = IMUNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
