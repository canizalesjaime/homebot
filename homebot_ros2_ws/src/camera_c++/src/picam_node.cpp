#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/image.hpp>
#include <std_srvs/srv/trigger.hpp>
#include <cv_bridge/cv_bridge.hpp>
#include <opencv2/opencv.hpp>
#include <chrono>
#include <string>

using namespace std::chrono_literals;

class PicamNode : public rclcpp::Node {
public:
    PicamNode() : Node("picam_node") {
        // OpenCV VideoCapture assumes PiCamera is accessible at /dev/video0
        cap_.open(0);
        if (!cap_.isOpened()) {
            RCLCPP_ERROR(this->get_logger(), "Failed to open camera.");
            rclcpp::shutdown();
            return;
        }

        cap_.set(cv::CAP_PROP_FRAME_WIDTH, 640);
        cap_.set(cv::CAP_PROP_FRAME_HEIGHT, 480);

        publisher_ = this->create_publisher<sensor_msgs::msg::Image>("camera/image_raw", 10);
        timer_ = this->create_wall_timer(100ms, std::bind(&PicamNode::publish_frame, this));
        srv_ = this->create_service<std_srvs::srv::Trigger>(
            "capture_image", std::bind(&PicamNode::capture_image_callback, this, std::placeholders::_1, std::placeholders::_2));

        RCLCPP_INFO(this->get_logger(), "Picamera2 C++ node started.");
    }

    ~PicamNode() {
        cap_.release();
    }

private:
    void publish_frame() {
        cv::Mat frame;
        cap_ >> frame;

        if (frame.empty()) {
            RCLCPP_WARN(this->get_logger(), "Captured empty frame.");
            return;
        }

        auto msg = cv_bridge::CvImage(std_msgs::msg::Header(), "bgr8", frame).toImageMsg();
        publisher_->publish(*msg);
    }

    void capture_image_callback(
        const std::shared_ptr<std_srvs::srv::Trigger::Request> request,
        std::shared_ptr<std_srvs::srv::Trigger::Response> response)
    {
        cv::Mat frame;
        cap_ >> frame;

        if (frame.empty()) {
            response->success = false;
            response->message = "Failed to capture image.";
            RCLCPP_WARN(this->get_logger(), response->message.c_str());
            return;
        }

        std::string filename = "/tmp/snapshot_" + std::to_string(std::time(nullptr)) + ".jpg";
        if (cv::imwrite(filename, frame)) {
            response->success = true;
            response->message = "Image saved to " + filename;
            RCLCPP_INFO(this->get_logger(), response->message.c_str());
        } else {
            response->success = false;
            response->message = "Failed to save image.";
            RCLCPP_ERROR(this->get_logger(), response->message.c_str());
        }
    }

    cv::VideoCapture cap_;
    rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Service<std_srvs::srv::Trigger>::SharedPtr srv_;
};

int main(int argc, char *argv[]) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<PicamNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
