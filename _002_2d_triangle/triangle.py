from PySide2.QtCore import Slot, Property, QObject, QSize
from PySide2.QtQuick import QQuickItem, QQuickWindow
from PySide2.QtCore import Qt
from PySide2.QtGui import QOpenGLShader, QOpenGLShaderProgram, QImage
import numpy as np
import ctypes
import OpenGL.GL as GL

positions = np.array([
    (-0.5, -0.8, 0.0),
    (0.5, -0.8, 0.0),
    (0.0, 0.8, 0.0)
], dtype=ctypes.c_float)

colors_mixed = np.array([
    (1.0, 0.0, 0.0),
    (0.0, 1.0, 0.0),
    (0.0, 0.0, 1.0)
], dtype=ctypes.c_float)

colors_red = np.array([
    (1.0, 0.0, 0.0, 0.0),
    (1.0, 0.1, 0.0, 0.0),
    (1.0, 0.1, 0.1, 0.0)
], dtype=ctypes.c_float)

colors_green = np.array([
    (0.0, 1.0, 0.0, 0.0),
    (0.1, 1.0, 0.0, 0.0),
    (0.1, 1.0, 0.1, 0.0)
], dtype=ctypes.c_float)

colors_blue = np.array([
    (0.0, 0.0, 1.0, 0.0),
    (0.0, 0.1, 1.0, 0.0),
    (0.1, 0.1, 1.0, 0.0)
], dtype=ctypes.c_float)

colors = colors_mixed


class TriangleUnderlay(QQuickItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._renderer = None
        self.windowChanged.connect(self.onWindowChanged)

    @Slot(QQuickWindow)
    def onWindowChanged(self, window):
        self.window().beforeSynchronizing.connect(self.sync, type=Qt.DirectConnection)
        self.window().setClearBeforeRendering(False)

    @Slot()
    def sync(self):
        if self._renderer is None:
            self._renderer = TriangleUnderlayRenderer()
            self.window().beforeRendering.connect(self._renderer.paint, type=Qt.DirectConnection)
        self._renderer.set_viewport_size(self.window().size() * self.window().devicePixelRatio())
        self._renderer.set_window(self.window())

    @Slot(int)
    def changeColor(self, color_enum):
        global colors
        if color_enum == 1:
            colors = colors_red
        elif color_enum == 2:
            colors = colors_green
        elif color_enum == 3:
            colors = colors_blue
        elif color_enum == 4:
            colors = colors_mixed


class TriangleUnderlayRenderer(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._shader_program = None
        self._viewport_size = QSize()
        self._window = None

    @Slot()
    def paint(self):
        try:
            gl = self._window.openglContext().functions()
            if self._shader_program is None:
                self._shader_program = QOpenGLShaderProgram()
                self._shader_program.addShaderFromSourceFile(QOpenGLShader.Vertex, 'shaders/OpenGL_2_1/vertex.glsl')
                self._shader_program.addShaderFromSourceFile(QOpenGLShader.Fragment, 'shaders/OpenGL_2_1/fragment.glsl')
                self._shader_program.bindAttributeLocation('position', 0)
                self._shader_program.bindAttributeLocation('color', 1)
                self._shader_program.link()

            self._shader_program.bind()
            self._shader_program.enableAttributeArray(0)
            self._shader_program.enableAttributeArray(1)

            self._shader_program.setAttributeArray(0, GL.GL_FLOAT, positions.tobytes(), 3)
            self._shader_program.setAttributeArray(1, GL.GL_FLOAT, colors.tobytes(), 3)

            gl.glViewport(0, 0, self._viewport_size.width(), self._viewport_size.height())

            gl.glClearColor(0.5, 0.5, 0.5, 1)
            gl.glDisable(GL.GL_DEPTH_TEST)

            gl.glClear(GL.GL_COLOR_BUFFER_BIT)

            gl.glDrawArrays(GL.GL_TRIANGLES, 0, 3)
            self._shader_program.disableAttributeArray(0)
            self._shader_program.disableAttributeArray(1)
            self._shader_program.release()

            self._window.resetOpenGLState()
            self._window.update()
        except Exception as e:
            print(f"exception {e}")

    def set_viewport_size(self, size):
        self._viewport_size = size

    def set_window(self, window):
        self._window = window
