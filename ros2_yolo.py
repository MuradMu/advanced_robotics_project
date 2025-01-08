import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge, CvBridgeError
import cv2
import torch
from models.experimental import attempt_load
from utils.general import non_max_suppression, scale_coords, check_img_size
from utils.plots import plot_one_box
import os

class YOLOv7ROS(Node):
    def __init__(self):
        super().__init__('yolov7_ros')

        # ROS2 parameters
        self.declare_parameter('target_object', 'chair')
        self.declare_parameter('conf_thres', 0.25)
        self.declare_parameter('iou_thres', 0.45)
        self.declare_parameter('image_topic', '/camera/image_raw')

        # Load parameters
        self.target_object = self.get_parameter('target_object').get_parameter_value().string_value
        self.conf_thres = self.get_parameter('conf_thres').get_parameter_value().double_value
        self.iou_thres = self.get_parameter('iou_thres').get_parameter_value().double_value
        self.image_topic = self.get_parameter('image_topic').get_parameter_value().string_value

        # ROS2 subscriber and publisher
        self.subscription = self.create_subscription(
            Image,
            self.image_topic,
            self.image_callback,
            10)
        self.xy_pub = self.create_publisher(Point, 'xy_coordinates', 10)

        # OpenCV bridge
        self.bridge = CvBridge()

        # YOLOv7 setup
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model_path = './yolov7.pt'
        if not os.path.exists(model_path):
            self.get_logger().error(f"Model file {model_path} not found. Please provide a valid YOLOv7 model.")
            raise FileNotFoundError(f"Model file {model_path} not found.")
        
        self.model = attempt_load(model_path, map_location=self.device)  # Load YOLOv7 model
        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        self.img_size = 640  # Adjust image size if needed
        self.half = self.device.type != 'cpu'  # Use half precision if GPU available

        if self.half:
            self.model.half()

        self.get_logger().info("YOLOv7 Node Initialized.")

    def image_callback(self, msg):
        try:
            # Convert ROS2 image to OpenCV format
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError as e:
            self.get_logger().error(f"CVBridge Error: {e}")
            return

        # Preprocess the image
        img = cv2.resize(cv_image, (self.img_size, self.img_size))
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB
        img = img / 255.0  # Normalize
        img = torch.from_numpy(img).to(self.device).float()
        if self.half:
            img = img.half()
        img = img.unsqueeze(0)

        # Run inference
        with torch.no_grad():
            pred = self.model(img, augment=False)[0]

        # Apply NMS
        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres)

        # Process detections
        for i, det in enumerate(pred):
            if len(det):
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], cv_image.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    label = f"{self.names[int(cls)]} {conf:.2f}"
                    self.get_logger().info(f"Detected: {label} at {xyxy}")

                    # Publish coordinates if the detected object matches the target
                    if self.names[int(cls)] == self.target_object:
                        x_center = (xyxy[0] + xyxy[2]) / 2
                        y_center = (xyxy[1] + xyxy[3]) / 2
                        point_msg = Point()
                        point_msg.x = float(x_center)
                        point_msg.y = float(y_center)
                        point_msg.z = 0.0
                        self.xy_pub.publish(point_msg)
                        self.get_logger().info(f"Published Coordinates: ({point_msg.x}, {point_msg.y})")

                    # Draw bounding box on the image
                    plot_one_box(xyxy, cv_image, label=label, color=(255, 0, 0), line_thickness=2)

        # Display the image
        cv2.imshow("YOLOv7 Detection", cv_image)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = YOLOv7ROS()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

