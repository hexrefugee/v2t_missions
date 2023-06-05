; Auto-generated. Do not edit!


(cl:in-package test_pkg-msg)


;//! \htmlinclude CarInfo.msg.html

(cl:defclass <CarInfo> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (vehicle_id
    :reader vehicle_id
    :initarg :vehicle_id
    :type cl:integer
    :initform 0)
   (location
    :reader location
    :initarg :location
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass CarInfo (<CarInfo>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <CarInfo>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'CarInfo)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name test_pkg-msg:<CarInfo> is deprecated: use test_pkg-msg:CarInfo instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <CarInfo>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader test_pkg-msg:header-val is deprecated.  Use test_pkg-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'vehicle_id-val :lambda-list '(m))
(cl:defmethod vehicle_id-val ((m <CarInfo>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader test_pkg-msg:vehicle_id-val is deprecated.  Use test_pkg-msg:vehicle_id instead.")
  (vehicle_id m))

(cl:ensure-generic-function 'location-val :lambda-list '(m))
(cl:defmethod location-val ((m <CarInfo>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader test_pkg-msg:location-val is deprecated.  Use test_pkg-msg:location instead.")
  (location m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <CarInfo>) ostream)
  "Serializes a message object of type '<CarInfo>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:let* ((signed (cl:slot-value msg 'vehicle_id)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'location))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'location))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <CarInfo>) istream)
  "Deserializes a message object of type '<CarInfo>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'vehicle_id) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'location) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'location)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<CarInfo>)))
  "Returns string type for a message object of type '<CarInfo>"
  "test_pkg/CarInfo")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'CarInfo)))
  "Returns string type for a message object of type 'CarInfo"
  "test_pkg/CarInfo")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<CarInfo>)))
  "Returns md5sum for a message object of type '<CarInfo>"
  "98bbad100463b9a4aa2857a0a9b4dacc")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'CarInfo)))
  "Returns md5sum for a message object of type 'CarInfo"
  "98bbad100463b9a4aa2857a0a9b4dacc")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<CarInfo>)))
  "Returns full string definition for message of type '<CarInfo>"
  (cl:format cl:nil "# 该消息用于传递车辆ID和位置信息~%# 位置信息包括x、y、z三个坐标值~%Header header~%int32 vehicle_id~%float32[] location~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'CarInfo)))
  "Returns full string definition for message of type 'CarInfo"
  (cl:format cl:nil "# 该消息用于传递车辆ID和位置信息~%# 位置信息包括x、y、z三个坐标值~%Header header~%int32 vehicle_id~%float32[] location~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <CarInfo>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     4
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'location) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <CarInfo>))
  "Converts a ROS message object to a list"
  (cl:list 'CarInfo
    (cl:cons ':header (header msg))
    (cl:cons ':vehicle_id (vehicle_id msg))
    (cl:cons ':location (location msg))
))
