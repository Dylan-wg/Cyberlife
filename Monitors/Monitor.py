from Elements.Element import Element


class Monitor:

    def __init__(self, target: Element, name=""):
        self.target = target
        self.name = name
        self.text = ""

    def set_text(self):
        self.text = ""
        data = self.target.get_data()
        for t in data:
            self.text += (t + ": " + data[t] + "\n")

    def update(self):
        self.set_text()
        print("======================================================================================================")
        print(self.text)
        print("======================================================================================================")
