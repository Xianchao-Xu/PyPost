# coding: utf-8
# author: xuxc
import os
import platform
import random
import sys

from PyQt5.QtCore import (
    Qt,
    QSettings,
    QByteArray,
    PYQT_VERSION_STR
)
from PyQt5.QtGui import (QIcon, QKeySequence, QCloseEvent)
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QSplitter,
    QFrame,
    QLabel,
    QSpinBox,
    QSpacerItem,
    QFileDialog,
    QMessageBox,
    QAction,
    QTreeWidget,
    QTreeWidgetItem,
    QTabWidget,
    QTextBrowser,
    QSizePolicy
)

# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2  # 虽然后面没有用到，但必须导入这个，否则会报错
from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkCommonCore import (
    vtkPoints,
    vtkVersion
)
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import (
    VTK_VERTEX,
    VTK_POLY_VERTEX,
    VTK_LINE,
    VTK_POLY_LINE,
    VTK_TRIANGLE,
    VTK_TRIANGLE_STRIP,
    VTK_POLYGON,
    VTK_PIXEL,
    VTK_QUAD,
    VTK_TETRA,
    VTK_VOXEL,
    VTK_HEXAHEDRON,
    VTK_WEDGE,
    VTK_PYRAMID,
    VTK_QUADRATIC_EDGE,
    VTK_QUADRATIC_TRIANGLE,
    VTK_QUADRATIC_QUAD,
    VTK_QUADRATIC_TETRA,
    VTK_QUADRATIC_HEXAHEDRON,
    vtkUnstructuredGrid
)
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkInteractionWidgets import (
    vtkLogoWidget,
    vtkLogoRepresentation,
    vtkOrientationMarkerWidget,
    vtkTextWidget,
    vtkTextRepresentation
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderer,
    vtkTextActor
)
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor as QVTKWidget

from utility.FileParser import FileParser

__version__ = '0.01'
__author__ = 'XuXianchao'
__organization__ = '仿真坊'
__appname__ = 'PyFEM'

TREE_TOP_LEVEL_NAMES = [
    '坐标系',
    '几何',
    '网格',
    '载荷',
    '边界',
    '结果'
]

NAMED_COLORS = [
    'cold_grey', 'dim_grey', 'grey', 'light_grey',
    'slate_grey', 'slate_grey_dark', 'slate_grey_light',
    'warm_grey'
    'black', 'ivory_black', 'lamp_black',
    'alizarin_crimson', 'brick', 'cadmium_red_deep', 'coral',
    'coral_light', 'deep_pink', 'english_red', 'firebrick',
    'geranium_lake', 'hot_pink', 'indian_red', 'light_salmon',
    'madder_lake_deep', 'maroon', 'pink', 'pink_light',
    'raspberry', 'red', 'rose_madder', 'salmon', 'tomato',
    'venetian_red',
    'beige', 'brown', 'brown_madder', 'brown_ochre',
    'burlywood', 'burnt_sienna', 'burnt_umber', 'chocolate',
    'deep_ochre', 'flesh', 'flesh_ochre', 'gold_ochre',
    'greenish_umber', 'khaki', 'khaki_dark', 'light_beige',
    'peru', 'rosy_brown', 'raw_sienna', 'raw_umber', 'sepia',
    'sienna', 'saddle_brown', 'sandy_brown', 'tan',
    'van_dyke_brown',
    'cadmium_orange', 'cadmium_red_light', 'carrot',
    'dark_orange', 'mars_orange', 'mars_yellow', 'orange',
    'orange_red', 'yellow_ochre',
    'aureoline_yellow', 'banana', 'cadmium_lemon',
    'cadmium_yellow', 'cadmium_yellow_light', 'gold',
    'goldenrod', 'goldenrod_dark', 'goldenrod_light',
    'goldenrod_pale', 'light_goldenrod', 'melon',
    'naples_yellow_deep', 'yellow', 'yellow_light',
    'chartreuse', 'chrome_oxide_green', 'cinnabar_green',
    'cobalt_green', 'emerald_green', 'forest_green', 'green',
    'green_dark', 'green_pale', 'green_yellow', 'lawn_green',
    'lime_green', 'mint', 'olive', 'olive_drab',
    'olive_green_dark', 'permanent_green', 'sap_green',
    'sea_green', 'sea_green_dark', 'sea_green_medium',
    'sea_green_light', 'spring_green', 'spring_green_medium',
    'terre_verte', 'viridian_light', 'yellow_green',
    'aquamarine', 'aquamarine_medium', 'cyan', 'cyan_white',
    'turquoise', 'turquoise_dark', 'turquoise_medium',
    'turquoise_pale',
    'alice_blue', 'blue', 'blue_light', 'blue_medium',
    'cadet', 'cobalt', 'cornflower', 'cerulean', 'dodger_blue',
    'indigo', 'manganese_blue', 'midnight_blue', 'navy',
    'peacock', 'powder_blue', 'royal_blue', 'slate_blue',
    'slate_blue_dark', 'slate_blue_light',
    'slate_blue_medium', 'sky_blue', 'sky_blue_deep',
    'sky_blue_light', 'steel_blue', 'steel_blue_light',
    'turquoise_blue', 'ultramarine',
    'blue_violet', 'cobalt_violet_deep', 'magenta',
    'orchid', 'orchid_dark', 'orchid_medium',
    'permanent_red_violet', 'plum', 'purple',
    'purple_medium', 'ultramarine_violet', 'violet',
    'violet_dark', 'violet_red', 'violet_red_medium',
    'violet_red_pale'
]

VTK_ELEMENT_TYPE_TABLE = {
    1: VTK_VERTEX,
    2: VTK_POLY_VERTEX,
    3: VTK_LINE,
    4: VTK_POLY_LINE,
    5: VTK_TRIANGLE,
    6: VTK_TRIANGLE_STRIP,
    7: VTK_POLYGON,
    8: VTK_PIXEL,
    9: VTK_QUAD,
    10: VTK_TETRA,
    11: VTK_VOXEL,
    12: VTK_HEXAHEDRON,
    13: VTK_WEDGE,
    14: VTK_PYRAMID,
    21: VTK_QUADRATIC_EDGE,
    22: VTK_QUADRATIC_TRIANGLE,
    23: VTK_QUADRATIC_QUAD,
    24: VTK_QUADRATIC_TETRA,
    25: VTK_QUADRATIC_HEXAHEDRON
}


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('{} - v{}'.format(__appname__, __version__))

        # 中央窗体
        self.central_widget = QWidget(self)
        self.central_widget.setObjectName('central_widget')
        self.setCentralWidget(self.central_widget)
        # 中央窗体布局
        self.vertical_layout = QVBoxLayout(self.central_widget)
        self.vertical_layout.setObjectName('vertical_layout')

        # 水平分割器
        self.horizontal_splitter = QSplitter(self.central_widget)
        self.horizontal_splitter.setOrientation(Qt.Horizontal)
        self.horizontal_splitter.setObjectName('horizontal_splitter')
        # 水平分割器添加左右部件，左边为模型树，右边为垂直分割器
        # 添加模型树
        self.tree_widget = QTreeWidget(self.horizontal_splitter)
        self.tree_widget.setObjectName('tree_widget')
        self.vertical_splitter = QSplitter(self.horizontal_splitter)
        # 添加垂直分割器
        self.vertical_splitter.setOrientation(Qt.Vertical)
        self.vertical_splitter.setObjectName('vertical_splitter')
        # 垂直分割器添加上下部件，上边为主视图tab，用于显示模型；下边为附加部件tab，用于显示信息，后续还可添加其他tab
        # 添加视图tab
        self.view_tab_widget = QTabWidget(self.vertical_splitter)
        self.view_tab_widget.setObjectName('view_tab_widget')
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.view_tab_widget.setSizePolicy(size_policy)
        # 添加附加部件tab
        self.additional_tab_widget = QTabWidget(self.vertical_splitter)
        self.additional_tab_widget.setObjectName('additional_tab_widget')
        # 附加部件添加信息tab
        self.info_tab = QWidget()
        self.info_tab.setObjectName('info_tab')
        self.additional_tab_widget.addTab(self.info_tab, '信息')
        # 信息tab添加text browser用于显示信息
        self.info_browser = QTextBrowser(self.additional_tab_widget)
        self.info_browser.setObjectName('info_browser')
        self.info_tab_layout = QVBoxLayout(self.info_tab)
        self.info_tab_layout.setObjectName('info_tab_layout')
        self.info_tab_layout.addWidget(self.info_browser)

        # vtk相关控件
        self.vtk_widget = QVTKWidget()
        self.render_window = self.vtk_widget.GetRenderWindow()
        self.iren = self.render_window.GetInteractor()
        self.renderer = vtkRenderer()
        self.actor_index = 0  # actor的索引号
        self.actors = dict()  # actor字典
        self.axes_actor = vtkAxesActor()
        self.logo_widget = vtkLogoWidget()  # 用于放置logo，必须全局可用
        self.text_widget = vtkTextWidget()  # 用于放置软件名和版本号
        self.marker_widget = vtkOrientationMarkerWidget()  # 用于放置坐标轴

        # 添加其他控件
        self.add_menu()  # 添加菜单栏和工具栏
        self.add_navigation_tab()  # 添加导航标签，用于放置各种控制按钮
        self.init_tree_widget()
        self.add_vtk_view()  # 添加VTK视图
        self.init_vtk_view()  # VTK视图初始化

        self.vertical_layout.addWidget(self.horizontal_splitter)

        self.statusBar().showMessage('准备完毕', 5000)  # 添加状态栏

        # 恢复上次关闭时的状态
        self.load_settings()

    @staticmethod
    def add_actions(target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def add_menu(self):
        self.add_file_menu()
        self.add_help_menu()

    def add_file_menu(self):
        file_menu = self.menuBar().addMenu('文件')
        file_menu.setObjectName('file_menu')
        file_toolbar = self.addToolBar('文件')
        file_toolbar.setObjectName('file_toolbar')
        file_new_action = self.create_action(
            '新建', self.file_new, QKeySequence.New, 'Images/New.png', '新建文件')
        file_open_action = self.create_action(
            '打开', self.file_open, QKeySequence.Open, 'Images/Open.png', '打开文件')
        file_exit_action = self.create_action(
            '退出', self.close, 'Ctrl+Q', 'Images/Exit.png', '退出')
        self.add_actions(file_menu, (file_new_action, file_open_action, None, file_exit_action))
        self.add_actions(file_toolbar, (file_new_action, file_open_action, file_exit_action))

    def add_help_menu(self):
        help_menu = self.menuBar().addMenu('帮助')
        help_menu.setObjectName('help_menu')
        file_help_action = self.create_action(
            '帮助', self.file_help, icon="Images/Help.png", tip='帮助')
        file_about_action = self.create_action(
            '关于', self.file_about, icon='Images/About.png', tip='关于')
        file_license_action = self.create_action(
            '许可', self.file_license, QKeySequence.HelpContents, 'Images/License.png', '许可')
        self.add_actions(help_menu, (file_help_action, None, file_about_action, file_license_action))

    def add_navigation_tab(self):
        navigation_tab = QTabWidget()
        navigation_tab.setObjectName('navigation_tab')
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        navigation_tab.setSizePolicy(size_policy)
        self.vertical_layout.addWidget(navigation_tab)

        self.add_view_navigation(navigation_tab)

    def add_view_navigation(self, widget: QTabWidget):
        view_navigation_tab = QWidget()
        view_navigation_tab.setObjectName('view_navigation_tab')
        widget.addTab(view_navigation_tab, '视图')

        size_frame = QFrame()
        size_frame.setFrameShape(QFrame.StyledPanel)
        size_frame.setFrameShadow(QFrame.Sunken)
        #
        node_size_layout = QHBoxLayout()
        node_size_label = QLabel('节点大小：')
        node_size_spinbox = QSpinBox()
        node_size_spinbox.setValue(5)
        node_size_spinbox.setMinimum(1)
        node_size_spinbox.setMaximum(10000)
        node_size_layout.addWidget(node_size_label)
        node_size_layout.addWidget(node_size_spinbox)
        #
        edge_size_layout = QHBoxLayout()
        edge_size_label = QLabel('网格粗细：')
        edge_size_spinbox = QSpinBox()
        edge_size_spinbox.setMinimum(1)
        edge_size_spinbox.setMaximum(10000)
        edge_size_layout.addWidget(edge_size_label)
        edge_size_layout.addWidget(edge_size_spinbox)
        #
        size_layout = QVBoxLayout()
        size_layout.addLayout(node_size_layout)
        size_layout.addLayout(edge_size_layout)
        #
        size_frame.setLayout(size_layout)

        space_item = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        view_navigation_layout = QHBoxLayout()
        view_navigation_layout.addWidget(size_frame)
        view_navigation_layout.addItem(space_item)

        view_navigation_tab.setLayout(view_navigation_layout)

        node_size_spinbox.valueChanged.connect(self.node_size_changed)

    def add_vtk_view(self):
        vtk_view_tab = QWidget()
        vtk_view_tab.setObjectName('vtk_view_tab')
        self.view_tab_widget.addTab(vtk_view_tab, 'VTK视图')
        vtk_layout = QVBoxLayout(vtk_view_tab)
        vtk_layout.addWidget(self.vtk_widget)

    def closeEvent(self, a0: QCloseEvent) -> None:
        settings = QSettings()
        settings.setValue('MainWindow/Geometry', self.saveGeometry())
        settings.setValue('MainWindow/State', self.saveState())
        settings.setValue('MainWindow/HorizontalSplitter', self.horizontal_splitter.saveState())
        settings.setValue('MainWindow/VerticalSplitter', self.vertical_splitter.saveState())

    def create_action(self, text, slot=None, shortcut=None, icon=None,
                      tip=None, checkable=False, signal='triggered'):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            getattr(action, signal).connect(slot)
        if checkable:
            action.setCheckable(True)
        return action

    def file_new(self):
        # 打开文件时，移除所有actor，并重新添加全局坐标轴，actor索引重置为1
        for actor in self.actors.values():
            self.renderer.RemoveActor(actor)

        self.axes_actor.AxisLabelsOff()
        self.renderer.AddActor(self.axes_actor)
        self.actor_index = 1
        self.actors[self.actor_index] = self.axes_actor

        self.render_window.Render()

    def file_open(self):
        supported_files_list = {
            '自定义{}文件': '*.fem'.format(__appname__),
        }
        supported_files = '支持的文件({})'.format(' '.join(supported_files_list.values()))
        format_filter = '所有文件(*.*);;' + supported_files
        for key, value in supported_files_list.items():
            format_filter += ';;' + key + '({})'.format(value)
        filename, dialog_title = QFileDialog.getOpenFileName(
            self, '打开文件', '.', format_filter)
        if filename:
            if '*'+os.path.splitext(filename)[-1] not in supported_files_list.values():
                self.info_browser.append("<font color='red'>错误：不支持的格式：{}<font>".format(filename))
                return
            else:
                if os.path.splitext(filename)[-1] == '.fem':
                    self.info_browser.append('正在打开文件：{}'.format(filename))
                    params = FileParser(filename)
                    params.parse_fem()
                    if params.succeed:
                        if params.type == 'scatter':
                            self.show_scatter(params)
                        elif params.type == 'mesh':
                            self.show_mesh(params)
                        item_index = TREE_TOP_LEVEL_NAMES.index('网格')
                        basename = os.path.splitext(os.path.basename(filename))[0]
                        mesh_item = QTreeWidgetItem(self.tree_widget.topLevelItem(item_index))
                        mesh_item.setText(0, '{}'.format(basename))
                        mesh_item.setCheckState(0, Qt.Checked)
                        mesh_item.setText(1, '{}'.format(self.actor_index))
                    self.info_browser.append(params.msg)

    def file_help(self):
        QMessageBox.about(
            self, '帮助',
            """<p>{}暂无帮助文档，如需帮助，可联系作者：
            <p>邮箱: 479902764@qq.com
            """.format(__appname__)
        )

    def file_about(self):
        QMessageBox.about(
            self, '关于{}'.format(__appname__),
            '''<b>{}</b> v{} 
            <p>一个简单的有限元软件。
            <p>作者：{}
            <p>知乎账号：悬臂梁
            <p>公众号：仿真坊
            <p>开发工具：Python {} - PyQt {} - VTK {}'''.format(
                __appname__,
                __version__,
                __author__,
                platform.python_version(),
                PYQT_VERSION_STR,
                vtkVersion.GetVTKVersion()
            )
        )

    def file_license(self):
        QMessageBox.about(
            self, '许可', '{}采用MIT开源协议进行许可'.format(__appname__)
        )

    def init_tree_widget(self):
        self.tree_widget.setStyleSheet(
            "QTreeWidget::indicator:unchecked {image: url(Images/Hide.png);}"
            "QTreeWidget::indicator:checked {image: url(Images/Show.png);}"
        )
        self.tree_widget.setHeaderLabels(['', '编号', '颜色'])
        self.tree_widget.setColumnWidth(0, 160)
        self.tree_widget.setColumnWidth(1, 35)
        self.tree_widget.setColumnWidth(2, 35)

        self.tree_widget.itemChanged.connect(self.show_hide_actor)

        for parent_name in TREE_TOP_LEVEL_NAMES:
            parent = QTreeWidgetItem(self.tree_widget)
            parent.setText(0, parent_name)
            parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            parent.setCheckState(0, Qt.Checked)

    def init_vtk_view(self):
        self.renderer.SetBackground(0.9, 0.9, 0.9)
        self.render_window.AddRenderer(self.renderer)
        self.iren.SetInteractorStyle(vtkInteractorStyleTrackballCamera())

        # 添加全局坐标轴
        self.axes_actor.AxisLabelsOff()
        self.renderer.AddActor(self.axes_actor)
        self.actor_index += 1
        self.actors[self.actor_index] = self.axes_actor
        # 模型树更新全局坐标轴信息
        axes_actor_item = QTreeWidgetItem(self.tree_widget.topLevelItem(0))
        axes_actor_item.setText(0, '全局坐标系')
        axes_actor_item.setCheckState(0, Qt.Checked)
        axes_actor_item.setText(1, '{}'.format(self.actor_index))
        self.tree_widget.expandAll()

        # 添加logo
        png_reader = vtkJPEGReader()
        png_reader.SetFileName('Images/qrcode.jpg')
        png_reader.Update(None)  # 不加None的时候PyCharm要报"Parameter 'p_int' unfilled"
        logo_representation = vtkLogoRepresentation()
        logo_representation.SetImage(png_reader.GetOutput())
        logo_representation.SetPosition(0.9, 0.03)
        logo_representation.SetPosition2(0.1, 0.1)
        logo_representation.GetImageProperty().SetOpacity(1.0)
        self.logo_widget.SetRepresentation(logo_representation)  # logo_widget需要全局可用
        self.logo_widget.SetInteractor(self.iren)
        self.logo_widget.On()
        self.logo_widget.ProcessEventsOff()

        # 添加软件名、版本号
        text_actor = vtkTextActor()
        text_actor.SetInput('{}\nv{}'.format(__appname__, __version__))
        text_actor.GetTextProperty().SetColor(0.1, 0.1, 0.1)
        text_representation = vtkTextRepresentation()
        text_representation.SetPosition(0.88, 0.88)
        text_representation.SetPosition2(0.1, 0.1)
        # representation需要在text_actor前面添加
        self.text_widget.SetRepresentation(text_representation)  # text_widget需要全局可用
        self.text_widget.SetInteractor(self.iren)
        self.text_widget.SetTextActor(text_actor)
        self.text_widget.On()
        self.text_widget.ProcessEventsOff()

        # 添加坐标轴
        axes_actor = vtkAxesActor()
        self.marker_widget.SetOrientationMarker(axes_actor)
        self.marker_widget.SetInteractor(self.iren)
        self.marker_widget.EnabledOn()
        self.marker_widget.InteractiveOff()

        self.renderer.ResetCamera()
        self.render_window.Render()

    def load_settings(self):
        settings = QSettings()
        self.restoreGeometry(settings.value('MainWindow/Geometry', type=QByteArray))
        self.restoreState(settings.value('MainWindow/State', type=QByteArray))
        self.horizontal_splitter.restoreState(
            settings.value('MainWindow/HorizontalSplitter', type=QByteArray))
        self.vertical_splitter.restoreState(
            settings.value('MainWindow/VerticalSplitter', type=QByteArray))

    def node_size_changed(self, i):
        actor_index = self.actor_index
        current_item_index = self.tree_widget.currentItem().text(1)
        if current_item_index:
            actor_index = int(current_item_index)
        if actor_index > 1:
            self.actors[actor_index].GetProperty().SetPointSize(i)
            self.render_window.Render()

    def show_hide_actor(self, item: QTreeWidgetItem):
        if item.text(1):
            actor_index = int(item.text(1))
            if item.checkState(0) == Qt.Checked:
                self.actors[actor_index].VisibilityOn()
            elif item.checkState(0) == Qt.Unchecked:
                self.actors[actor_index].VisibilityOff()
            self.render_window.Render()

    def show_mesh(self, params):
        node_ids = params.node_ids
        nodes = params.nodes
        element_types = params.element_types
        elements = params.elements

        points = vtkPoints()
        for index, node in enumerate(nodes):
            points.InsertPoint(index, node)

        grid = vtkUnstructuredGrid()
        grid.SetPoints(points)

        for index, element in enumerate(elements):
            connection = [node_ids.index(i) for i in element]
            grid.InsertNextCell(VTK_ELEMENT_TYPE_TABLE[element_types[index]], len(element), connection)

        mapper = vtkDataSetMapper()
        mapper.SetInputData(grid)

        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(vtkNamedColors().GetColor3d(random.choice(NAMED_COLORS)))
        actor.GetProperty().EdgeVisibilityOn()
        actor.GetProperty().RenderPointsAsSpheresOn()
        self.actor_index += 1
        self.actors[self.actor_index] = actor

        self.renderer.AddActor(actor)
        self.renderer.ResetCamera()

        self.render_window.Render()

    def show_scatter(self, params):
        nodes = params.nodes
        points = vtkPoints()
        for index, value in enumerate(nodes):
            points.InsertPoint(index, value)

        grid = vtkUnstructuredGrid()
        grid.SetPoints(points)
        for i in range(len(nodes)):
            grid.InsertNextCell(VTK_VERTEX, 1, [i])

        mapper = vtkDataSetMapper()
        mapper.SetInputData(grid)

        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(vtkNamedColors().GetColor3d(random.choice(NAMED_COLORS)))
        actor.GetProperty().SetPointSize(10)
        actor.GetProperty().RenderPointsAsSpheresOn()
        self.actor_index += 1
        self.actors[self.actor_index] = actor

        self.renderer.AddActor(actor)
        self.renderer.ResetCamera()

        self.render_window.Render()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName('{}'.format(__appname__))
    app.setOrganizationName('{}'.format(__organization__))
    win = MainWindow()
    win.show()
    app.exec_()
