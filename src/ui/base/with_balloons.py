# coding=utf-8

from src.ui.widget_balloon.widget import WidgetBalloon


class WithBalloons:
    def __init__(self):
        self.balloons = []

    def remove_balloons(self):
        while self.balloons:
            balloon = self.balloons.pop()
            balloon.hide()
            del balloon

    def show_error_balloon(self, text, qt_object):
        self.balloons.append(WidgetBalloon.error(qt_object, text))
