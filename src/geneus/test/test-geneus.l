#!/usr/bin/env roseus
;;;
;;; euslisp version of ros_tutorials/rospy_tutorials/talker_listener_test.py
;;;

(require :unittest "lib/llib/unittest.l")

(ros::load-ros-manifest "roseus")
;; check if package without msgs is ok
;; ros::eus-error is error
(unless (fboundp 'ros::ros-error-org)
  (setf (symbol-function 'ros::ros-error-org) (symbol-function 'ros::ros-error)))
(defun ros::ros-error (&rest args)
  (apply #'ros::ros-error-org args)
  (error (apply #'format nil args)))

;;;
;;;
(init-unit-test)

(defun check-msg-gen (type &optional method data)
  (let (i o s)
    (if method
        (setq i (instance type :init method data))
      (setq i (instance type :init)))
    (setq o (instance type :init))
    (format *error-output* "~A ~A ~A " (send type :name) method data)
    (setq s (send i :serialize))
    (send o :deserialize s)
    (if method
        (progn
          (format *error-output* "~A~%" (send o method))
          (cond ((floatp data)
                 (assert (eps= (send o method) data)))
                ((float-vector-p data)
                 (assert (eps-v= (send o method) data)))
                (t
                 (assert (equal (send o method) data)))))
      (format *error-output* "~%"))
    ))
;; test codes
;; http://wiki.ros.org/msg#Fields
;; char: deprecated alias for uint8
;; byte: deprecated alias for int8
(deftest test-std-msgs
  (mapcar #'(lambda (x) (apply #'check-msg-gen x))
          (list (list std_msgs::bool :data t)
                (list std_msgs::bool :data nil)
                (list std_msgs::byte :data 1)
                (list std_msgs::byte :data -1)
                (list std_msgs::bytemultiarray :data #i(1 2 3))
                (list std_msgs::bytemultiarray :data #i(-1 -2 -3))
                (list std_msgs::char :data 2)
                (list std_msgs::colorrgba :r 0.1) (list std_msgs::colorrgba :g 0.2) (list std_msgs::colorrgba :b 0.3) (list std_msgs::colorrgba :a 0.4)
                (list std_msgs::duration :data (ros::time 1.234))
                (list std_msgs::empty nil nil)
                (list std_msgs::float32 :data 1.234)
                (list std_msgs::float64 :data 5.678)
                (list std_msgs::header :seq 1234) (list std_msgs::header :stamp (ros::time 1.234)) (list std_msgs::header :frame_id "frame")
                (list std_msgs::int16 :data -1)
                (list std_msgs::int32 :data -2)
                (list std_msgs::int64 :data -3)
                (list std_msgs::int8 :data -4)
                ;;(list std_msgs::multiarraydimension :data #\b)
                ;;(list std_msgs::multiarraylayout :data #\b)
                (list std_msgs::string :data "euslisp")
                (list std_msgs::time :data (ros::time 1.234))
                (list std_msgs::uint16 :data 1)
                (list std_msgs::uint32 :data 2)
                (list std_msgs::uint64 :data 3)
                (list std_msgs::uint8 :data 4)
                (list std_msgs::float32multiarray :data #f(1.234 5.678))
                (list std_msgs::float64multiarray :data #f(1.234 5.678))
                (list std_msgs::int16multiarray :data #i(1 2 3))
                (list std_msgs::int16multiarray :data #i(-1 -2 -3))
                (list std_msgs::int32multiarray :data #i(4 5 6))
                (list std_msgs::int32multiarray :data #i(-4 -5 -6))
                (list std_msgs::int64multiarray :data #i(7 8 9))
                (list std_msgs::int64multiarray :data #i(-7 -8 -9))
                (list std_msgs::int8multiarray :data #i(10 11 12))
                (list std_msgs::int8multiarray :data #i(-10 -11 -12))
                (list std_msgs::uint16multiarray :data #i(1 2 3))
                (list std_msgs::uint32multiarray :data #i(4 5 6))
                (list std_msgs::uint64multiarray :data #i(7 8 9))
                (list std_msgs::uint8multiarray :data (make-array 3
                                                                  :element-type :char
                                                                  :initial-contents "eus"))
                ;; FixedArray
                (list roseus::FixedArray :float32_data #f(1 -2 3))
                (list roseus::FixedArray :float64_data #f(4 -5 6))
                (list roseus::FixedArray :int16_data #i(7 -8 9))
                (list roseus::FixedArray :int32_data #i(10 -11 12))
                (list roseus::FixedArray :int64_data #i(13 -14 15))
                (list roseus::FixedArray :int8_data #i(16 -17 18))
                (list roseus::FixedArray :uint16_data #i(1 2 3))
                (list roseus::FixedArray :uint32_data #i(4 5 6))
                (list roseus::FixedArray :uint64_data #i(7 8 9))
                (list roseus::FixedArray :uint8_data (make-array 17
                                                                     :element-type :char
                                                                     :initial-contents "johosystemkougaku"))
                (list roseus::FixedArray :bool_data (list t nil))
                (list roseus::FixedArray :time_data (list (ros::time 0) (ros::time 1)))
                (list roseus::FixedArray :duration_data (list (ros::time 0) (ros::time 1)))
                (list roseus::FixedArray :string_data (list (instance std_msgs::String :data "ros") (instance std_msgs::String :data "eus")))

                ;; VariableArray (data set is copied from FixedArray)
                (list roseus::VariableArray :float32_data #f(1 -2 3))
                (list roseus::VariableArray :float64_data #f(4 -5 6))
                (list roseus::VariableArray :int16_data #i(7 -8 9))
                (list roseus::VariableArray :int32_data #i(10 -11 12))
                (list roseus::VariableArray :int64_data #i(13 -14 15))
                (list roseus::VariableArray :int8_data #i(16 -17 18))
                (list roseus::VariableArray :uint16_data #i(1 2 3))
                (list roseus::VariableArray :uint32_data #i(4 5 6))
                (list roseus::VariableArray :uint64_data #i(7 8 9))
                (list roseus::VariableArray :uint8_data (make-array 17
                                                                     :element-type :char
                                                                     :initial-contents "johosystemkougaku"))
                (list roseus::VariableArray :bool_data (list t nil))
                (list roseus::VariableArray :time_data (list (ros::time 0) (ros::time 1)))
                (list roseus::VariableArray :duration_data (list (ros::time 0) (ros::time 1)))
                (list roseus::VariableArray :string_data (list (instance std_msgs::String :data "ros") (instance std_msgs::String :data "eus")))
                ))
  )

(defmacro subscribe-and-check-msg (name type method data)
  `(ros::subscribe ,name ,type #'(lambda (x)
                                   (format *error-output* "~A ~A ~A~%" (send ,type :name) ,data (send x ,method))
                                   (cond ((floatp ,data)
                                          (assert (eps= (send x ,method) ,data)))
                                         ((float-vector-p ,data)
                                          (assert (eps-v= (send x ,method) ,data)))
                                         (t
                                          (assert (equal (send x ,method) ,data)))))))
(defun subscribe-and-check-array-msg (x)
  (dolist (o `((:float32_data #f(1 -2 3)) (:float64_data #f(4 -5 6))
               (:int16_data #i(7 -8 9)) (:int32_data #i(10 -11 12)) (:int64_data #i(13 -14 15))
               (:int8_data #i(16 -17 18)) (:uint16_data #i(1 2 3))  (:uint32_data #i(4 5 6))
               (:uint64_data #i(7 8 9))
               (:uint8_data "johosystemkougaku")
               (:bool_data ,(list t nil))
               (:time_data ,(list (ros::time 0) (ros::time 1)))
               (:duration_data ,(list (ros::time 0) (ros::time 1)))
               (:string_data ,(list (instance std_msgs::String :data "ros") (instance std_msgs::String :data "eus")))
               ))
    (let ((method (car o)) (data (cadr o)))
      (format *error-output* "~A ~A ~A~%" method data (send x method))
      (cond ((floatp data)
             (assert (eps= (send x method) data)))
            ((float-vector-p data)
             (assert (eps-v= (send x method) data)))
            (t
             (assert (equal (send x method) data)))))))

(deftest test-send_msgs
  (subscribe-and-check-msg "bool" std_msgs::bool :data t)
  (subscribe-and-check-msg "byte" std_msgs::byte :data 1)
  (subscribe-and-check-msg "bytemultiarray" std_msgs::ByteMultiArray :data #i(-1 2 -3]))
  (subscribe-and-check-msg "char" std_msgs::Char :data 2)
  ;;(subscribe-and-check-msg "colorrgba" std_msgs::ColorRGBA :data ColorRGBA(0.1,0.2,0.3,0.4)),
  (subscribe-and-check-msg "duration" std_msgs::Duration :data (ros::time 1.234))
  ;;(subscribe-and-check-msg "empty" std_msgs::Empty nil nil)
  (subscribe-and-check-msg "float32" std_msgs::Float32 :data 1.234)
  (subscribe-and-check-msg "float64" std_msgs::Float64 :data 5.678)
  ;;(subscribe-and-check-msg "header" std_msgs::Header :data Header(seq=1234,stamp=rospy.Time(1.234),frame_id="frame")
  (subscribe-and-check-msg "int16" std_msgs::Int16 :data -1)
  (subscribe-and-check-msg "int32" std_msgs::Int32 :data -2)
  (subscribe-and-check-msg "int64" std_msgs::Int64 :data -3)
  (subscribe-and-check-msg "int8" std_msgs::Int8 :data -4)
  ;;(subscribe-and-check-msg "multiarraydimension" std_msgs::MultiArrayDimension :data ,
  ;;(subscribe-and-check-msg "multiarraylayout" std_msgs::MultiAarrayLayout :data ,
  (subscribe-and-check-msg "string" std_msgs::String :data "euslisp")
  (subscribe-and-check-msg "time" std_msgs::Time :data (ros::time 1.234))
  (subscribe-and-check-msg "uint16" std_msgs::UInt16 :data 1)
  (subscribe-and-check-msg "uint32" std_msgs::UInt32 :data 2)
  (subscribe-and-check-msg "uint64" std_msgs::UInt64 :data 3)
  (subscribe-and-check-msg "uint8" std_msgs::UInt8 :data 4)
  (subscribe-and-check-msg "float32multiarray" std_msgs::Float32MultiArray :data #f(1.234 5.678))
  (subscribe-and-check-msg "float64multiarray" std_msgs::Float64MultiArray :data #f(1.234 5.678))
  (subscribe-and-check-msg "int16multiarray" std_msgs::Int16MultiArray :data #i(-1 2 -3))
  (subscribe-and-check-msg "int32multiarray" std_msgs::Int32MultiArray :data #i(-4 5 -6))
  (subscribe-and-check-msg "int64multiarray" std_msgs::Int64MultiArray :data #i(-7 8 -9))
  (subscribe-and-check-msg "int8multiarray" std_msgs::Int8MultiArray :data #i(-10 11 -12))
  (subscribe-and-check-msg "uint16multiarray" std_msgs::UInt16MultiArray :data #i(1 2 3))
  (subscribe-and-check-msg "uint32multiarray" std_msgs::UInt32MultiArray :data #i(4 5 6))
  (subscribe-and-check-msg "uint64multiarray" std_msgs::UInt64MultiArray :data #i(7 8 9))
  ;; roseus treats uint8[] data as a string, which is the Euslisp reresentation for byte data.
  ;; see http://wiki.ros.org/msg#Fields
  (subscribe-and-check-msg "uint8multiarray" std_msgs::UInt8MultiArray :data "eus")

  (format *error-output* "fixedarray~%")
  (ros::subscribe "fixedarray" roseus::FixedArray #'subscribe-and-check-array-msg)
  (format *error-output* "variablearray~%")
  (ros::subscribe "variablearray" roseus::VariableArray #'subscribe-and-check-array-msg)


  (ros::rate 10)
  (dotimes (i 25)
    (ros::spin-once)
    (ros::sleep)
    ))

(deftest test-set-bool ;; see https://github.com/jsk-ros-pkg/geneus/pull/56
  (let (a b)
    (setq a (instance std_msgs::bool :data t))
    (assert (eq (send a :data) t))
    (setq a (instance std_msgs::bool :data nil))
    (assert (eq (send a :data) nil))
    (setq a (instance std_msgs::bool))
    (send a :data t)
    (assert (eq (send a :data) t))
    (setq a (instance std_msgs::bool))
    (send a :data nil)
    (assert (eq (send a :data) nil))
    (send a :data t)
    (assert (eq (send a :data) t)) ;; #56
    (send a :data nil)
    (assert (eq (send a :data) nil))

    (setq b (instance std_msgs::int8 :data 8))
    (assert (eq (send b :data) 8))
    (setq b (instance std_msgs::int8 :data 1))
    (assert (eq (send b :data) 1))
    (setq b (instance std_msgs::int8))
    (send b :data 8)
    (assert (eq (send b :data) 8))
    (setq b (instance std_msgs::int8))
    (send b :data 1)
    (assert (eq (send b :data) 1))
    (send b :data 8)
    (assert (eq (send b :data) 8))
    (send b :data 1)
    (assert (eq (send b :data) 1))
    ))

;; locate geneus/test/test.msg
(make-package "GENEUS")
(load "package://geneus/test/test.l")
(deftest test-constant
  (let (tmp)
    (setq tmp geneus::test::*true_flag*)
    (format *error-output* "geneus::test::*true_flag* is ~A~%" tmp)
    (assert (eq tmp t))
    (setq tmp geneus::test::*false_flag*)
    (format *error-output* "geneus::test::*false_flag* is ~A~%" tmp)
    (assert (eq tmp nil))
    (setq tmp geneus::test::*true_flag_symbol*)
    (format *error-output* "geneus::test::*true_flag_symbol* is ~A~%" tmp)
    (assert (eq tmp t))
    (setq tmp geneus::test::*false_flag_symbol*)
    (format *error-output* "geneus::test::*false_flag_symbol* is ~A~%" tmp)
    (assert (eq tmp nil))
    (setq tmp geneus::test::*int_1*)
    (format *error-output* "geneus::test::*int_1* is ~A~%" tmp)
    (assert (= tmp -1))
    (setq tmp geneus::test::*int_8*)
    (format *error-output* "geneus::test::*int_8* is ~A~%" tmp)
    (assert (= tmp 8))
    (setq tmp geneus::test::*float_12*)
    (format *error-output* "geneus::test::*float_12* is ~A~%" tmp)
    (assert (eps= tmp -1.2))
    (setq tmp geneus::test::*float_89*)
    (format *error-output* "geneus::test::*float_89* is ~A~%" tmp)
    (assert (eps= tmp 8.9))
    (setq tmp geneus::test::*string_1*)
    (format *error-output* "geneus::test::*string_1* is ~A~%" tmp)
    (assert (string= tmp "string"))
    (setq tmp geneus::test::*string_2*)
    (format *error-output* "geneus::test::*string_2* is ~A~%" tmp)
    (assert (string= tmp "string"))
    (setq tmp geneus::test::*string_3*)
    (format *error-output* "geneus::test::*string_3* is ~A~%" tmp)
    (assert (string= tmp "string string"))
    (setq tmp geneus::test::*string_4*)
    (format *error-output* "geneus::test::*string_4* is ~A~%" tmp)
#|
http://wiki.ros.org/msg#Constants says
```
string EXAMPLE="#comments" are ignored, and leading and trailing whitespace removed

string constants are assigned the value of everything to the right of the equals sign, with leading and trailing whitespace removed. As such, you cannot leave a comment on a string constant definition.
```

```
$ cat test.msg
bool TRUE_FLAG=1
bool FALSE_FLAG=0
bool TRUE_FLAG_SYMBOL=True
bool FALSE_FLAG_SYMBOL=False
int8 INT_1=-1
int8 INT_8=8
float32 FLOAT_12=-1.2
float32 FLOAT_89=8.9
string STRING_1=string
string STRING_2=  string
string STRING_3=  string string
string STRING_4=  string ## string
string STRING_5=#string
string STRING_6='#string'
string STRING_7="#string"
$ rosrun genpy gen_python.py `rospack find geneus`/test/test.msg -Igeneus:`rospack find geneus`/test -p geneus -o `rospack find geneus`/test
$ ipython
In [1]: import _test                                                                                                                                  In [2]: _test.test.STRING_1
Out[2]: 'string'
In [3]: _test.test.STRING_2
Out[3]: 'string'
In [4]: _test.test.STRING_3
Out[4]: 'string string'
In [5]: _test.test.STRING_4
Out[5]: 'string ## string'
In [6]: _test.test.STRING_5
Out[6]: '#string'
In [7]: _test.test.STRING_6
Out[7]: "'#string'"
In [8]: _test.test.STRING_7
Out[8]: '"#string"'
```
|#
    (assert (string= tmp "string ## string"))
    (setq tmp geneus::test::*string_5*)
    (format *error-output* "geneus::test::*string_5* is ~A~%" tmp)
    (assert (string= tmp "#string"))
    (setq tmp geneus::test::*string_6*)
    (format *error-output* "geneus::test::*string_6* is ~A~%" tmp)
    (assert (string= tmp "'#string'"))
    (setq tmp geneus::test::*string_7*)
    (format *error-output* "geneus::test::*string_7* is ~A~%" tmp)
    (assert (string= tmp "\"#string\""))

    (setq tmp (geneus::test-to-symbol geneus::test::*pending*))
    (format *error-output* "geneus::test-to-symbol geneus::test::*pending* is ~A (~A)~%" geneus::test::*pending* tmp)
    (assert (eq tmp 'geneus::test::*pending*))
    (setq tmp (geneus::test-to-symbol geneus::test::*active*))
    (format *error-output* "geneus::test-to-symbol geneus::test::*active* is ~A (~A)~%" geneus::test::*active* tmp)
    (assert (eq tmp 'geneus::test::*active*))
    (setq tmp (geneus::test-to-symbol geneus::test::*preempted*))
    (format *error-output* "geneus::test-to-symbol geneus::test::*preempted* is ~A (~A)~%" geneus::test::*preempted* tmp)
    (assert (eq tmp 'geneus::test::*preempted*))
    ))

(ros::roseus "test_geneus")
(run-all-tests)
(exit)

