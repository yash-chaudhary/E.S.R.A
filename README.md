# E.S.R.A
E.S.R.A - **E**nhanced **S**ensory **R**ecognition with **A**I. This project includes a physical conveyor belt demonstration as well as web interface that uses the YOLOv8 computer vision model for object detection, recognition and counting.

(This project was completed during the OFS AI Hackathon)

## Demo
This demonstration contains two parts.
* conveyor model
* custom app that does object detection and counting using computer vision on real-time video streams

ADD DEMO VIDEO HERE

### Conveyor model
The purpose of this model is to emulate a typical part of the manufacturing process and to demonstrate the software
in a real-life setting. This setup thus allows us to test the capabilities of different computer vision models by empirical testing
there effective based on changing different parameters seen by the camera. These parameters can include the color, shape and size of 
different objects as well the a color and objects of the background. This is necessary to test the feasibility of computer vision
models in a real-life setting that is plagued by differnet objects in the background, objects blocking the camera and just a wide range
of different objects that may be seen at different stages of the manufacturing process.
* Electrical:
	* Arduino UNO (compute for his project)
	* HC-SR04 Ultrasonic sensor (used to emulate proximity sensor to detect and count objects)
	* LCD (used to track count and production rate of conveyor model)
	* 28BYJ-48 Stepper motor (used to drive conveyor)
	* ULN2003 Stepper driver (used to control stepper motor operation)
	* 10k potentiometer (used for speed control of stepper motor)
	* 9V battery holder (used for providing power directly to stepper motor controller) 
* Software:
	* Single arduino file (.ino) that controls all onboard electronics
* Mechanical:
	* LEGO used to quickly prototype construction of conveyor structure	
	* Use of captive-nut slot for easy assembly/disassembly
	* Laser cut MDF for quick prototyping

![conveyor model](https://github.com/yash-chaudhary/E.S.R.A/blob/main/assets/conveyor_demo.jpeg)

### Application interface
Purpose: To both stream real-time video data using the device's camera (mainly iPhone/iPad) as well as	
to have the ability to upload pre-taken videos. These video streams are then run through
the YOLOv8 computer vision model to detect objects of interest and count when objects pas through a virtual checkpoint. This architecture is used to demonstrate the emulation of a proximity sensor to count objects using computer vision.

* Features:
	* Ability to upload a pre-taken video and run object detection and recognition on it
	* Ability to start real-time streaming via web-interface using device's camera 
	* Ability to select confidence threshold to filter erronous objects detected
	* Ability to select which object classes to detect (see COCO dataset for objects that can be detected)
	* Ability to specify start and endpoints of virtual checkpoint (when objects pass this checkpoint object count tracker is updated)
	* Ability to modify bounding box and checkpoint line features
	
![application interface](https://github.com/yash-chaudhary/E.S.R.A/blob/main/assets/application_interface.png)

### TODO
* Add real-time computer vision on streamlit-webrtc video stream
* Clean up UI to ensure video box is correctly sized with user window
* Add the ability to test different computer vision models
* Add the ability to take a take and label pictures to add to OFS manufactured goods dataset
* Add the ability to save stream with or without labels 			
