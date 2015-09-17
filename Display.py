from kivy.app import App
# from kivy.uix.widget import Widget
# from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.uix.label import Label
# from kivy.uix.button import Button
# import random
from DPS_Exceptions import InternalError
from Process_Line import Parse_Line

class InfoForm(BoxLayout):

    def __init__(self, **kwargs):
        super(InfoForm, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.set_up_panes()
        self.members = {}
        self.empties = []

    def add_member(self, name):
        if len(self.members) > 5:
            raise InternalError("More than 5 Party members in group")
        self.members[name] = StatEntry(name, 0)
        for i in self.empties:
            self.player_pane.remove_widget(i)
        del self.empties[:]
        self.player_pane.add_widget(self.members[name])
        for i in range(0, 5 - len(self.members)):
            self.add_empty()

    def remove_member(self, name):
        self.player_pane.remove_widget(self.members[name])
        self.members.pop(name)
        self.add_empty()

    def add_empty(self):
        self.empties.append(Empty_Space())
        self.player_pane.add_widget(self.empties[-1])

    def set_up_panes(self):
        self.player_pane = BoxLayout(orientation='vertical', size_hint=(.7, 1))
        with self.player_pane.canvas.before:
            Color(0, 1, 0, 1)
            self.player_pane.rect = Rectangle(size=self.player_pane.size, pos=self.player_pane.pos)
        self.info_pane = BoxLayout(orientation='vertical', size_hint=(.3, 1))
        with self.info_pane.canvas.before:
            Color(0, 1, 1, 1)
            self.info_pane.rect = Rectangle(size=self.info_pane.size, pos=self.info_pane.pos)
        self.add_widget(self.player_pane)
        self.add_widget(self.info_pane)
        self.player_pane.bind(pos=InfoForm.update_rect, size=InfoForm.update_rect)
        self.info_pane.bind(pos=InfoForm.update_rect, size=InfoForm.update_rect)

    def update_rect(instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size


class StatEntry(BoxLayout):

    def __init__(self, name, dps, **kwargs):
        super(StatEntry, self).__init__(**kwargs)
        # with self.canvas.before:
        #     Color(random.randint(0, 1), random.randint(0, 1), random.randint(0, 2), random.randint(0, 2))
        #     self.rect = Rectangle(size=self.size, pos=self.pos)
        # self.bind(pos=InfoForm.update_rect, size=InfoForm.update_rect)
        self.add_widget(Label(text=name, size_hint=(0.3, 1)))
        self.add_widget(MyProgressBar(value=dps, max=100, size_hint=(0.7, 1)))
        self.padding = (0, 0, 100, 0)


class Empty_Space(BoxLayout):
    def __init__(self, **kwargs):
        super(StatEntry, self).__init__(**kwargs)


class MyProgressBar(ProgressBar):

    def __init__(self, **kwargs):
        super(MyProgressBar, self).__init__(**kwargs)


class StatsCruncherApp(App):

    def __init__(self,  group, lines, **kwargs):
        super(StatsCruncherApp, self).__init__(**kwargs)
        self.group = group
        self.lines = lines
        self.parser = Parse_Line()

    def read(self, dt):
        line = self.lines.readline()
        if line != "":
            print(line)
            # self.parser.parse(line, self.group)

    def build(self):
        Clock.schedule_interval(self.read, .1 / 60.0)
