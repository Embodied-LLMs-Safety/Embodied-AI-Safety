import time
import os
import sys
import termios
import tty
import threading
import json

from pymycobot.mycobot import MyCobot
from pymycobot import PI_PORT, PI_BAUD

mc = MyCobot(PI_PORT, PI_BAUD, debug=False)

class Raw(object):
    """Set raw input mode for device"""

    def __init__(self, stream):
        self.stream = stream
        self.fd = self.stream.fileno()

    def __enter__(self):
        self.original_stty = termios.tcgetattr(self.stream)
        tty.setcbreak(self.stream)

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(self.stream, termios.TCSANOW, self.original_stty)


class Helper(object):
    def __init__(self) -> None:
        self.w, self.h = os.get_terminal_size()

    def echo(self, msg):
        print("\r{}".format(" " * self.w), end="")
        print("\r{}".format(msg), end="")


class TeachingTest(Helper):
    def __init__(self, mycobot) -> None:
        super().__init__()
        self.mc = mycobot
        self.recording = False
        self.playing = False
        self.record_list = []
        self.record_t = None
        self.play_t = None

    def record(self):
        self.record_list = []
        self.recording = True
        self.mc.set_fresh_mode(0)
        def _record():
            start_t = time.time()

            while self.recording:
                angles = self.mc.get_encoders()
                if angles:
                    self.record_list.append(angles)
                    time.sleep(0.1)
                    print("\r {}".format(time.time() - start_t), end="")

        self.echo("Start recording actions.")
        self.record_t = threading.Thread(target=_record, daemon=True)
        self.record_t.start()

    def stop_record(self):
        if self.recording:
            self.recording = False
            self.record_t.join()
            self.echo("Stop recording actions.")

    def play(self):
        self.echo("Start replaying actions.")
        for angles in self.record_list:
            # print(angles)
            self.mc.set_encoders(angles, 80)
            time.sleep(0.1)
        self.echo("Playback ended.\n")

    def loop_play(self):
        self.playing = True

        def _loop():
            len_ = len(self.record_list)
            i = 0
            while self.playing:
                idx_ = i % len_
                i += 1
                self.mc.set_encoders(self.record_list[idx_], 80)
                time.sleep(0.1)

        self.echo("Start loop playback.")
        self.play_t = threading.Thread(target=_loop, daemon=True)
        self.play_t.start()

    def stop_loop_play(self):
        if self.playing:
            self.playing = False
            self.play_t.join()
            self.echo("End loop playback.")

    def save_to_local(self):
        if not self.record_list:
            self.echo("No data should save.")
            return

        save_path = os.path.dirname(__file__) + "/temp/record.txt"
        with open(save_path, "w") as f:
            json.dump(self.record_list, f, indent=2)
            self.echo("Export playback actions to:  {}".format(save_path))

    def load_from_local(self):

        with open(os.path.dirname(__file__) + "/temp/record.txt", "r") as f:
            try:
                data = json.load(f)
                self.record_list = data
                self.echo("Successfully loaded local action data.")
            except Exception:
                self.echo("Error: invalid data.")

    def print_menu(self):
        print(
            """\
        \r Drag and teach
        \r q: Quit
        \r r: Start recording
        \r c: Stop recording
        \r p: Playback
        \r P: Loop playback / Stop loop playback
        \r s: Save the recorded actions locally
        \r l: Read the recorded actions from local storage
        \r f: Relax the robotic arm
        \r----------------------------------
            """
        )

    def start(self):
        self.print_menu()

        while not False:
            with Raw(sys.stdin):
                key = sys.stdin.read(1)
                if key == "q":
                    break
                elif key == "r":  # recorder
                    self.record()
                elif key == "c":  # stop recorder
                    self.stop_record()
                elif key == "p":  # play
                    self.play()
                elif key == "P":  # loop play
                    if not self.playing:
                        self.loop_play()
                    else:
                        self.stop_loop_play()
                elif key == "s":  # save to local
                    self.save_to_local()
                elif key == "l":  # load from local
                    self.load_from_local()
                elif key == "f":  # free move
                    self.mc.release_all_servos()
                    self.echo("Released")
                else:
                    print(key)
                    continue

def drag_teach():
    
    print('Reset the robotic arm to zero position.')
    mc.send_angles([0, 0, 0, 0, 0, 0], 40)
    time.sleep(3)
    
    recorder = TeachingTest(mc)
    recorder.start()

    print('Reset the robotic arm to zero position.')
    mc.send_angles([0, 0, 0, 0, 0, 0], 40)
    time.sleep(3)
