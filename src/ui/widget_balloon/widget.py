# coding=utf-8

from src.qt import QWidget, QLabel, QGraphicsDropShadowEffect, QPoint
from src.qt.palette import PaletteBalloon


class WidgetBalloon(QLabel):
    def __init__(self, widget, text, color):
        assert isinstance(widget, QWidget)
        QLabel.__init__(self, widget.window())
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(10)
        effect.setOffset(2, 2)
        self.setGraphicsEffect(effect)
        self.setMargin(6)
        self.setMinimumWidth(widget.width())

        self.setStyleSheet('QLabel {{background-color: {}; border-radius: 5px;}}'.format(color))

        assert isinstance(widget, QWidget)
        self.widget = widget

        self.setText(text)

        self.show()

        q_point = self.widget.mapTo(self.parentWidget(), self.widget.rect().bottomLeft())
        assert isinstance(q_point, QPoint)
        q_point.setY(q_point.y() + 6)
        self.move(q_point)

    @staticmethod
    def note(widget, text):
        return WidgetBalloon(widget, text, PaletteBalloon.note)

    @staticmethod
    def warning(widget, text):
        return WidgetBalloon(widget, text, PaletteBalloon.warning)

    @staticmethod
    def error(widget, text):
        return WidgetBalloon(widget, text, PaletteBalloon.error)

    @staticmethod
    def background(widget, text):
        return WidgetBalloon(widget, text, PaletteBalloon.background)

    @staticmethod
    def info(widget, text):
        return WidgetBalloon(widget, text, PaletteBalloon.info)

    def mouseReleaseEvent(self, QMouseEvent):
        self.hide()
        super(WidgetBalloon, self).mouseReleaseEvent(QMouseEvent)
