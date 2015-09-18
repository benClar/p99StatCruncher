from kivy.app import App
# from kivy.uix.widget import Widget
# from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.uix.label import Label
# from kivy.uix.actionbar import ActionBar, ActionItem
from kivy.uix.button import Button
# import random
from DPS_Exceptions import InternalError
from Process_Line import Parse_Line
import time


class MainWindow(BoxLayout):
    pass

class InfoForm(BoxLayout):

    def __init__(self, group, **kwargs):
        super(InfoForm, self).__init__(**kwargs)  # You'll see these throughout.  This calls the superclass' constructor for this kivy component.
        # self.set_up_act_bar()
        self.set_up_panes()
        self.members = {}
        self.empties = []
        self.group = group

    # def set_up_act_bar(self):
    #     self.add_widget(self.act_bar)

    def add_member(self, name):
        """Adds group member from display

        Args:
            name: Name of member.  Used as key in GUI for layout refering to
            that member.
        """
        if len(self.members) > 5:
            raise InternalError("More than 5 Party members in group")
        self.members[name] = StatEntry(name, 0, self.group)
        #  Removing all dummy layouts to avoid newly added members
        #  Having gaps between them
        for i in self.empties:
            self.player_pane.remove_widget(i)
        del self.empties[:]
        self.player_pane.add_widget(self.members[name])
        # Adding empty dummy layouts back in under all real layouts
        for i in range(0, 5 - len(self.members)):
            self.add_empty()

    def remove_member(self, name):
        """Removes group member from display"""
        self.player_pane.remove_widget(self.members[name])
        self.members.pop(name)
        self.add_empty()

    def add_empty(self):
        self.empties.append(Empty_Space())
        self.player_pane.add_widget(self.empties[-1])

    def set_up_panes(self):
        """Sets up left and right panes that display group members and <undecided> information, respectively"""
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
        """Ensures background rectangles stay correct size"""
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def update_stats(self, grp):
        """recieves group data and updates GUI.

        Args:
            grp: Group() object contains various dictionaries with scraped
            data"""
        # iterate over key, value pair in group member dictionary
        for member in self.members:
            self.members[member].ids.stat_prog.ids.DPS_lab.text = str(grp.DPS(member))
            self.members[member].ids.stat_prog.value = grp.percentage_damage(member)

class StatEntry(BoxLayout):

    def __init__(self, name, dps, group, **kwargs):
        super(StatEntry, self).__init__(**kwargs)
        self.ids.stat_name.text = name
        self.ids.reset_timer.bind(on_press=self.reset)
        self.group = group
        # self.ids.stat_prog.value =  #  Todo: show percentage

    def reset(self, dt):
        self.group.reset(self.ids.stat_name.text)
        # with self.canvas.before:
        #     Color(random.randint(0, 1), random.randint(0, 1), random.randint(0, 2), random.randint(0, 2))
        #     self.rect = Rectangle(size=self.size, pos=self.pos)
        # self.bind(pos=InfoForm.update_rect, size=InfoForm.update_rect)
        # self.add_widget())
        # self.prog_bar = MyProgressBar(value=dps, max=100, size_hint=(0.7, 1))
        # self.add_widget(self.prog_bar)
        # self.add_widget()


class Empty_Space(BoxLayout):
    def __init__(self, **kwargs):
        super(Empty_Space, self).__init__(**kwargs)


class MyProgressBar(ProgressBar):

    def __init__(self, **kwargs):
        super(MyProgressBar, self).__init__(**kwargs)


class StatsCruncherApp(App):

    def __init__(self, player, group, lines, **kwargs):
        super(StatsCruncherApp, self).__init__(**kwargs)
        self.group = group
        self.lines = lines
        self.parser = Parse_Line()
        self.info_pane = InfoForm(self.group)

    def update(self, dt):
        line = self.lines.readline()
        if line != "":
            self.parser.parse(line.split(" "), self.group)
        self.info_pane.update_stats(self.group)



    def build(self):
        self.root.add_widget(self.info_pane)
        Clock.schedule_interval(self.update, .1 / 60.0)
        self.info_pane.add_member(self.group.player)
