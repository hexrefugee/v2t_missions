;; Auto-generated. Do not edit!


(when (boundp 'test_pkg::CarInfo)
  (if (not (find-package "TEST_PKG"))
    (make-package "TEST_PKG"))
  (shadow 'CarInfo (find-package "TEST_PKG")))
(unless (find-package "TEST_PKG::CARINFO")
  (make-package "TEST_PKG::CARINFO"))

(in-package "ROS")
;;//! \htmlinclude CarInfo.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass test_pkg::CarInfo
  :super ros::object
  :slots (_header _vehicle_id _location ))

(defmethod test_pkg::CarInfo
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:vehicle_id __vehicle_id) 0)
    ((:location __location) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _header __header)
   (setq _vehicle_id (round __vehicle_id))
   (setq _location __location)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:vehicle_id
   (&optional __vehicle_id)
   (if __vehicle_id (setq _vehicle_id __vehicle_id)) _vehicle_id)
  (:location
   (&optional __location)
   (if __location (setq _location __location)) _location)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; int32 _vehicle_id
    4
    ;; float32[] _location
    (* 4    (length _location)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; int32 _vehicle_id
       (write-long _vehicle_id s)
     ;; float32[] _location
     (write-long (length _location) s)
     (dotimes (i (length _location))
       (sys::poke (elt _location i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; int32 _vehicle_id
     (setq _vehicle_id (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; float32[] _location
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _location (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _location i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     ))
   ;;
   self)
  )

(setf (get test_pkg::CarInfo :md5sum-) "98bbad100463b9a4aa2857a0a9b4dacc")
(setf (get test_pkg::CarInfo :datatype-) "test_pkg/CarInfo")
(setf (get test_pkg::CarInfo :definition-)
      "# 该消息用于传递车辆ID和位置信息
# 位置信息包括x、y、z三个坐标值
Header header
int32 vehicle_id
float32[] location
================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

")



(provide :test_pkg/CarInfo "98bbad100463b9a4aa2857a0a9b4dacc")


