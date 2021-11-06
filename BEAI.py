import speech_recognition as sr
import pyttsx3


class BEAI:
    def __init__(self):
        self.serialNumber = 0
        self.r = sr.Recognizer()
        self.synth = pyttsx3.init()

        self.lastSerial = None
        self.batteries = None

    def say(self, message):
        print(message)
        self.synth.say(message)
        self.synth.runAndWait()
        self.synth.stop()

    def play(self):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source)

            print("Ready!")
            self.synth.say("Ready")
            self.synth.runAndWait()
            self.synth.stop()

            # To do: Get JSON here and check probabilities
            moduleSource = self.r.listen(source)
            module = self.r.recognize_google(moduleSource)
            print("Heard: " + module)
            print(type(module))

            if module == "simple wires":
                self.simple_wire_module()
            elif "button" in module:
                self.button_module(module)

    def simple_wire_module(self):
        self.say("simple wire colors?")

        with sr.Microphone() as source:
            colorsSource = self.r.listen(source)
            colors = self.r.recognize_google(colorsSource)
            wires = colors.split()
            print("Heard: " + colors + " and translated to list: " + str(wires))

            wire_to_cut = self.simple_wire_logic(wires)
            answer = "Cut the " + wire_to_cut

            self.say(answer)

    def simple_wire_logic(self, wires):
        if len(wires) == 3:
            if "red" not in wires:
                return "second wire"
            elif wires[2] == "white":
                return "last wire"
            elif wires.count("blue") > 1:
                return "last wire"
            else:
                return "last wire"
        elif len(wires) == 4:
            self.getLastSerial()
            if wires.count("red") > 1 and self.lastSerial % 2 != 0:
                return "last red wire"
            elif wires[3] == "yellow" and "red" not in wires:
                return "first wire"
            elif wires.count("blue") == 1:
                return "first wire"
            elif wires.count("yellow") > 1:
                return "last wire"
            else:
                "cut the second wire"
        elif len(wires) == 5:
            self.getLastSerial()
            if wires[4] == "black" and self.lastSerial % 2 != 0:
                return "fourth wire"
            elif wires.count("red") == 1 and wires.count("yellow") > 1:
                return "first wire"
            elif "black" not in wires:
                return "second wire"
            else:
                return "first wire"
        elif len(wires) == 6:
            self.getLastSerial()
            if "yellow" not in wires and self.lastSerial % 2 != 0:
                return "third wire"
            elif wires.count("yellow") == 1 and wires.count("white") > 1:
                return "fourth wire"
            elif "red" not in wires:
                return "last wire"
            else:
                return "fourth wire"

    def button_module(self, button):
        words = button.split()
        self.button_logic(words[0], words[1])

    def button_logic(self, color, text):
        if color == 'blue' and text == 'abort':
            self.say("Hold button")
        elif text == 'Detonate' and self.batteries() > 1:
            self.say("Press and release")



    def keypad_module(self):
        pass
        # TODO: Set up input

    def simon_module(self):
        pass
        # TODO: Implement input

    def batteries(self):
        if self.batteries != None:
            return self.batteries

        self.say("How many batteries?")
        with sr.Microphone() as source:
            batteries_src = self.r.listen(source)
            batteries = self.r.recognize_google(batteries_src)
            self.batteries = batteries
            return batteries


    def getLastSerial(self):
        if self.lastSerial != None:
            return self.lastSerial

        print("Last serial digit?")
        self.synth.say("Last serial digit")
        self.synth.runAndWait()
        self.synth.stop()

        with sr.Microphone() as source:
            digitSource = self.r.listen(source)
            digit = self.r.recognize_google(digitSource)
            self.lastSerial = digit
            return digit



beai = BEAI()
beai.play()

