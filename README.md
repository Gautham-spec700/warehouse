# Warehouse Delivery Robot Interfaces

**Assignment 1 – ROS 2 Jazzy**

## 1. Project Overview

This project implements custom ROS 2 interfaces for an autonomous warehouse delivery robot using ROS 2 Jazzy and Python.

The system allows a warehouse robot to publish its status, accept packages based on weight and capacity restrictions, and perform delivery tasks with continuous feedback and cancellation support.

## 2. Technologies Used

- ROS 2 Jazzy
- Ubuntu Linux
- Python 3
- CMake
- colcon
- Git and GitHub

## 3. Project Structure

```text
warehouse_ws/
└── src/
    ├── warehouse_interfaces/
    │   ├── msg/
    │   │   └── DeliveryStatus.msg
    │   ├── srv/
    │   │   └── LoadPackage.srv
    │   ├── action/
    │   │   └── Deliver.action
    │   ├── CMakeLists.txt
    │   └── package.xml
    │
    └── warehouse_nodes/
        ├── resource/
        ├── warehouse_nodes/
        │   ├── __init__.py
        │   ├── status_service_node.py
        │   ├── deliver_action_server.py
        │   ├── deliver_action_client.py
        │   └── cancel_test.py
        ├── setup.py
        ├── setup.cfg
        └── package.xml
```

## 4. ROS 2 Packages

### Package 1: warehouse_interfaces

**Build Type:** `ament_cmake`

This package contains three custom ROS 2 interfaces.

#### A. DeliveryStatus.msg

Publishes robot information.

| Field | Data Type | Description |
|---|---|---|
| robot_id | string | Robot identification |
| package_count | uint8 | Number of loaded packages |
| battery | float32 | Battery percentage |
| state | uint8 | Current robot state |

Robot states:

- STATE_IDLE = 0
- STATE_MOVING = 1
- STATE_DELIVERING = 2

#### B. LoadPackage.srv

Handles package loading requests.

**Request:**
- package_id (string)
- weight (float32)

**Response:**
- accepted (bool)
- message (string)
- total_packages (uint8)

Validation rules:
- Maximum package weight: 10 kg.
- Maximum package capacity: 5 packages.
- Invalid packages are rejected with a reason.

#### C. Deliver.action

Handles warehouse delivery operations.

**Goal:**
- destination (string)
- distance (float32)
- speed (float32)

**Result:**
- success (bool)
- time_taken (float32)

**Feedback:**
- remaining_distance (float32)
- percent (float32)

### Package 2: warehouse_nodes

**Build Type:** `ament_python`

This package contains the Python ROS 2 nodes.

| Python File | Function |
|---|---|
| status_service_node.py | Publishes robot status and handles package loading |
| deliver_action_server.py | Executes delivery goals and sends feedback |
| deliver_action_client.py | Sends delivery goals and receives results |
| cancel_test.py | Tests delivery cancellation |

## 5. Main Features

1. Publishes robot status every 1 second.
2. Provides a package loading service.
3. Accepts packages weighing up to 10 kg.
4. Limits package capacity to 5.
5. Rejects invalid delivery goals.
6. Provides delivery feedback every 0.5 seconds.
7. Calculates remaining distance and completion percentage.
8. Supports action cancellation.
9. Returns delivery success and execution time.

## 6. Dependencies

Required ROS 2 packages:

- rclpy
- rosidl_default_generators
- rosidl_default_runtime
- warehouse_interfaces

Install dependencies:

```bash
cd ~/warehouse_ws

rosdep install --from-paths src --ignore-src -r -y
```

## 7. Build Instructions

Source ROS 2 Jazzy:

```bash
source /opt/ros/jazzy/setup.bash
```

Navigate to the workspace:

```bash
cd ~/warehouse_ws
```

Build the packages:

```bash
colcon build
```

Source the workspace:

```bash
source install/setup.bash
```

## 8. How to Run

### A. Run Status Publisher and Package Service

```bash
ros2 run warehouse_nodes status_service
```

### B. Run Delivery Action Server

```bash
ros2 run warehouse_nodes deliver_server
```

### C. Run Delivery Action Client

```bash
ros2 run warehouse_nodes deliver_client
```

Run the server and client in separate terminals.

## 9. Testing Commands

### Check Custom Interfaces

```bash
ros2 interface show warehouse_interfaces/msg/DeliveryStatus

ros2 interface show warehouse_interfaces/srv/LoadPackage

ros2 interface show warehouse_interfaces/action/Deliver
```

### Monitor Robot Status

```bash
ros2 topic echo /delivery_status
```

### Test Package Loading

```bash
ros2 service call /load_package warehouse_interfaces/srv/LoadPackage "{package_id: 'PKG001', weight: 5.0}"
```

### Test Package Rejection

```bash
ros2 service call /load_package warehouse_interfaces/srv/LoadPackage "{package_id: 'PKG002', weight: 15.0}"
```

### Test Delivery Action

```bash
ros2 action send_goal /deliver warehouse_interfaces/action/Deliver "{destination: 'Zone A', distance: 10.0, speed: 1.0}" --feedback
```

### Test Cancellation

Run the delivery action server, then execute:

```bash
python3 ~/warehouse_ws/src/warehouse_nodes/warehouse_nodes/cancel_test.py
```

## 10. Expected Results

- Robot status is published every second.
- Valid packages are accepted.
- Packages exceeding 10 kg are rejected.
- Packages beyond the five-package capacity are rejected.
- Valid delivery goals are accepted.
- Invalid delivery goals are rejected.
- Delivery feedback is published every 0.5 seconds.
- Successful deliveries return a result.
- Cancellation requests stop an active delivery.

## 11. Learning Outcomes

Through this assignment, the following ROS 2 concepts are implemented:

- Creating custom ROS 2 message interfaces.
- Creating custom service interfaces.
- Creating custom action interfaces.
- Developing Python ROS 2 nodes.
- Publisher and subscriber communication.
- Service client and server communication.
- Action client and server communication.
- Action feedback, results and cancellation.
- Building and managing ROS 2 workspaces using colcon.

## 12. Author

**Project:** Warehouse Delivery Robot Interfaces  
**Framework:** ROS 2 Jazzy  
**Language:** Python  
**Assignment:** 1 – Warehouse Delivery Robot Interfaces

---

*This project was developed as part of ROS 2 robotics and automation learning.*
