<h1 align='center' style="text-align:center; font-weight:bold; font-size:2.0em;letter-spacing:2.0px;"> BadRobot: Manipulating Embodied LLMs in the Physical World </h1>

<p align='center' style="text-align:center;font-size:1.25em;">
<b><em>Anonymous authors</em></b>
</p>

<p align='center';>
ICLR 24 under review <br>
</p>
<!-- <p align='center' style="text-align:center;font-size:2.5 em;">
<b>
    <a href="https://drive.google.com/file/d/1z8G-XWQOw9H5v4iP_2-ccSO1ZdznIOBP/view?usp=sharing" target="_blank" style="text-decoration: none;">[arXiv]</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href="https://embodied-ai-safety.github.io/" target="_blank" style="text-decoration: none;">[Project Page]
    </a> 
</b>
</p> -->


------------

$${\color{red}\text{\textbf{!!! Warning !!!}}}$$

$${\color{red}\text{\textbf{This paper contains potentially harmful}}}$$

$${\color{red}\text{\textbf{AI-generated language and aggressive actions.}}}$$



## Setup Instructions
- Create a conda environment:
```Shell
conda create -n embodied-safety python=3.10
conda activate embodied-safety
```

- Enable audio support:
```Shell
sudo apt-get install portaudio19-dev
```


- See [Instructions](https://github.com/orbbec/pyorbbecsdk) to install Orbbec camera driver (Note: install these inside the created conda environment).

- Install other dependencies:
```Shell
pip install -r requirements.txt
```

- Obtain an [OpenAI API](https://openai.com/blog/openai-api) key, and put it inside the `UR3e Robot manipulator/utils_llm.py`.



## Code Structure

- **`Jailbreak_Prompts.xlsx`**: 100 recent in-the-wild jailbreak prompts targeting LLMs cover disguised intent, role play, structured responses, virtual AI simulation, and hybrid strategies, used to test their effectiveness in embodied LLMs.

- **`Physical_Word_Malicious_Queries.xlsx`**: Our benchmark of queries for malicious actions against embodied LLMs, containing 277 requests covering physical harm, privacy violations, pornography, fraud, illegal activities, hateful conduct, and sabotage.

- **`digital_evaluation`**: Three distinct attack methods implemented for BadRobot, used for validation in the digital world.

### Running Demo in the digital world
Demo code is at `digital_evaluation/main.py`.


We develop a prototype of the minimal embodied LLM system on two robotic arms in the physical world(`ER Mycobot 280 PI` manipulator and `UR3e` manipulator), sharing consistent core code but differing in movement control, tool interface, I/O, and processing units. Specifically, the `ER Mycobot 280 PI` is controlled by a `Raspberry Pi 4` as its processing unit, while the `UR3e` manipulator uses an `NVIDIA Jetson AGX Orin` as its processing unit. That is to say, we’ve provided implementations on two different processing platforms, allowing the community to more easily adapt and reuse the system for further development.


Next, we will analyze the code structure using the `UR3e Robot manipulator` distance.

- **`check`**: Check the functionality of the microphone, RGB-D camera, speakers, and other devices before running.
- **`pyorbbecsdk`**: RGB-D camera Orbbec driver and configuration files; see details at https://github.com/orbbec/pyorbbecsdk.
- **`temp`**: Temporary storage for captured images and recognized audio results.
- **`API_KEY.py`**: APIs for speech recognition (ASR) and text-to-speech (TTS) modules. We use the [Baidu AI Cloud Qianfan Platform's ASR interface](https://intl.cloud.baidu.com/) and [ChatTTS's TTS model](https://github.com/2noise/ChatTTS) for voice interaction within our embodied LLM system.
- **`agent_go.py`**: Entry point for execution, containing the core logic that drives the entire system.
- **`depth_estimate.py`**: depth data from the depth camera.
- **`utils_agent.py`**: System prompts that enable LLM to serve as a robot agent.
- **`utils_asr.py`**: Speech recognition module. `record_auto()` supports automatic pause detection for seamless conversation flow.
- **`utils_camera.py`**: Used to invoke the camera.
- **`utils_llm.py`**: calling various LLM APIs; please enter the correct API KEY.
- **`utils_robot.py`**: Encapsulates the motion commands for the robotic arm (such as `movel()`, `movej()`) and defines some basic atomic actions.
- **`utils_tts.py`**: Convert the robot's response into sound.
- **`utils_vlm.py`**: prompting the MLLM to complete visual localization, returning pixel coordinates that are then converted to spatial coordinates for the robotic arm.
- **`utils_vlm_move.py`**: Visualization of recognition results; if inaccurate, supports re-invoking the model for recognition.
- **`utils_vlm_vqa.py`**: visual question and answer on the visual scene.


### Running Demo in the physical world
 Demo code is at `agent_go.py`.


## Ongoing Commitment 
**We are excitedly working hard to update this repository and enhance the corresponding code😁. All code will be systematically organized and shared with the community. Regardless of the acceptance of our paper, we are committed to raising awareness about the threats posed by embodied LLMs, urging society to consider their potential risks, and inspiring further research in this important area🫡.** 

**Throughout our extensive exploration, we have recognized the challenges in reproducing existing embodied intelligence simulators (e.g., Voxposer). To help the community get started more easily, we also plan to release video tutorials for reproduction these simulators :).**


## Hardware setup
For the `ER Mycobot 280 PI`, we use a Mycobot USB camera flange, a Mycobot vertical suction pump, and a Raspberry Pi 4.

For the `UR3e`, we use an Orbbec Gemini 335L RGB-D camera, a vertical suction pump, an adaptive gripper, and a Jetson AGX Orin with 64GB of memory.


<br><br>




