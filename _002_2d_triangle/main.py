import sys

from PySide2.QtCore import QUrl
from PySide2.QtGui import QGuiApplication, QSurfaceFormat
from PySide2.QtQuick import QQuickView
from PySide2.QtQml import qmlRegisterType

from triangle import TriangleUnderlay


if __name__ == '__main__':
    f = QSurfaceFormat()
    f.setVersion(2, 1)
    f.setDepthBufferSize(1) # fix depth buffer error
    f.setStencilBufferSize(1) # fix stencil buffer error

    # If CoreProfile is used, all the other QML rendering will fail, because they only use 2.1
    f.setProfile(QSurfaceFormat.CompatibilityProfile)
    QSurfaceFormat.setDefaultFormat(f)

    qmlRegisterType(TriangleUnderlay, 'OpenGLUnderQml', 1, 0, 'TriangleUnderlay')

    app = QGuiApplication(sys.argv)

    view = QQuickView()
    view.setFormat(f)
    view.setPersistentSceneGraph(True)
    view.setPersistentOpenGLContext(True)
    view.setResizeMode(QQuickView.SizeRootObjectToView)  # Set for the object to resize correctly
    view.setSource(QUrl('TriangleWindow.qml'))
    view.show()

    sys.exit(app.exec_())
