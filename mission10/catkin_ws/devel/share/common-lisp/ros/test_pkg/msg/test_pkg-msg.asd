
(cl:in-package :asdf)

(defsystem "test_pkg-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "CarInfo" :depends-on ("_package_CarInfo"))
    (:file "_package_CarInfo" :depends-on ("_package"))
  ))