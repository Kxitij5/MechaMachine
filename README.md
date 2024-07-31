# MechaMachine
## A real-time face tracking turret inspired by KillJoy, a character in the video game called Valorant.

A face tracking turret which tracks the faces of the people and aims for headshot. There are 2 versions of this project, one which uses open-cv and a python package built upon it, known as cvzone; the other one is a custom trained YOLOv5 model which differentiates between friend and enemy before shooting.


## Table Of Content
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)


## Installation
Follow the sreps given below to setup this project on your machine/system.

### Prerequisites 
Ensure the following tools and hardware and software requirements:

#### Hardware
- 3D Print the printables given in the cad design directory.
- Arduino Uno R3 (or any other Microcontroller).
- Webcam with atleast 640*480 resolution.
- 2 130 DC motors rated 9v and above.
- 3 SG90s or MG90 Servo Motors. 
- LM2596 DC-DC Step Down Module.
- KY008 Laser Module.
- P30N06 N Channel MOSFET.
- 330ohm Resistor.
- FR107 Rectifier Diode.
- DC barrel jack.
- A few M-M, F-M, M-F Jumper Wires. 
- 12v 2amps DC Power Adaptor.

#### Tools and Fabrication Materials:
- Soldering Iron and wire.
- Heat Shrink Tubings.
- Screw Driver.
- M2, M2.5, M5 screws.
- Digital Multimeter.
- 3D Printer.

#### Software Requirements:
- Preferred Choice of Code Editor.
- Arduino IDE.
- Git.
- Python 3.7+.

### Clone the Repository 
Clone the repository to your local machine:
```bash
git clone https://github.com/Kxitij5/MechaMachine.git
cd MechaMachine
```
### Install Dependencies 
To install the python packages:
```bash
cd /MechaMachine_code
pip install -r requirements.txt
```

## Usage
The instructions to use the MechaMachine project:
### Hardware Connections and Schematics:
Refer the link to the [Hackster Project Website](have to give the link yet) to get the schematics and connections.

### Running the MechaMachine:
Connect the Arduino to the Host PC and change the com port in the code.
#### Uploading the Arduino Code:
- Go to MechaMachine_code directory.
- Open the Arduino_Code in the Arduino IDE.
- Upload the code to appropriate board.
#### To run the real-time version:
```bash
cd MechaMachine_code/
python MechaMachine.py
```
#### To run the trained version:
- Train your desired custom [YOLOv5 Model](https://colab.research.google.com/github/ultralytics/yolov5/blob/master/tutorial.ipynb).
- Download the model.
- Load it in the Trained_MechaMachine.py line number 6.
- Then do the following:
```bash
cd MechaMachine_code/
python Trained_MechaMachine.py
```

## Contributing
Follow these steps to contribute to [MechaMachine](https://github.com/Kxitij5/MechaMachine).

### Fork the Repository
Fork the repository on GitHub and clone your fork:
```bash
git clone https://github.com/your-username/MechaMachine.git
cd MechaMachine
```

### Create a Branch
Create a new branch for your feature or bugfix:
```bash
git checkout -b feature-branch
```

### Commit Changes 
Commit your changes with a descriptive commit message:
```bash
git commit -m "Add new feature"
```
### Push to the Branch
Push your changes to your fork:
```bash
git push origin feature-branch
```
### Open a Pull Request
Open a pull request on GitHub to merge your changes into the [MechaMachine](https://github.com/Kxitij5/MechaMachine) Repository.






































