# coding=utf-8

from src.qt import QWidget, QLabel, QGraphicsDropShadowEffect, QPoint
from src.qt.palette import PaletteBalloon


class WidgetBalloon(QLabel):
    def __init__(self, widget, text, color, position='bottomLeft', offset_x=6, offset_y=6, adjust_size=False):
        assert isinstance(widget, QWidget)
        QLabel.__init__(self, widget.parent())
        effect = QGraphicsDropShadowEffect()
        effect.setBlurRadius(10)
        effect.setOffset(2, 2)
        self.setGraphicsEffect(effect)
        self.setMargin(6)

        self.setText(text)

        if adjust_size:
            self.setMinimumWidth(0)
            self.adjustSize()
        else:
            self.setMinimumWidth(widget.width())

        self.setStyleSheet('QLabel {{background-color: {}; border-radius: 5px;}}'.format(color))

        assert isinstance(widget, QWidget)
        self.widget = widget

        self.show()

        if position == 'center' and not adjust_size:
            self.setFixedWidth(self.widget.width() - 40)

        if not hasattr(self.widget.rect(), position):
            raise ValueError('unknown position: {}'.format(position))

        rel_pos = getattr(self.widget.rect(), position)()
        q_point = self.widget.mapTo(self.parentWidget(), rel_pos)
        assert isinstance(q_point, QPoint)
        if position == 'center':
            q_point.setX(q_point.x() - (self.widget.width() / 2) + 20)
            q_point.setY(q_point.y() - self.height() / 2)
        q_point.setX(q_point.x() + offset_x)
        q_point.setY(q_point.y() + offset_y)
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

    def mouseReleaseEvent(self, event):
        self.hide()
        super(WidgetBalloon, self).mouseReleaseEvent(event)
