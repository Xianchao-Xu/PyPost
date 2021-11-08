# coding: utf-8
# author: xuxc
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QSplitter,
    QTabWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QSizePolicy,
    QFrame,
    QLabel,
    QSpinBox,
    QSpacerItem,
    QTextBrowser
)


class TopNavigationTab(QTabWidget):
    def __init__(self, parent=None):
        super(TopNavigationTab, self).__init__(parent)
        self.size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setSizePolicy(self.size_policy)

        self.add_navigation_tab()

    def add_navigation_tab(self):
        self.view_navigation_tab = QWidget(self)
        self.view_navigation_tab.setObjectName('view_navigation_tab')
        self.addTab(self.view_navigation_tab, '视图')

        size_frame = QFrame()
        size_frame.setFrameShape(QFrame.StyledPanel)
        size_frame.setFrameShadow(QFrame.Sunken)
        #
        node_size_layout = QHBoxLayout()
        node_size_label = QLabel('节点大小：')
        self.node_size_spinbox = QSpinBox()
        self.node_size_spinbox.setObjectName('node_size_spinbox')
        self.node_size_spinbox.setValue(5)
        self.node_size_spinbox.setMinimum(1)
        self.node_size_spinbox.setMaximum(10000)
        node_size_layout.addWidget(node_size_label)
        node_size_layout.addWidget(self.node_size_spinbox)
        #
        edge_size_layout = QHBoxLayout()
        edge_size_label = QLabel('网格粗细：')
        self.edge_size_spinbox = QSpinBox()
        self.edge_size_spinbox.setObjectName('edge_size_spinbox')
        self.edge_size_spinbox.setMinimum(1)
        self.edge_size_spinbox.setMaximum(10000)
        edge_size_layout.addWidget(edge_size_label)
        edge_size_layout.addWidget(self.edge_size_spinbox)
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

        self.view_navigation_tab.setLayout(view_navigation_layout)


class ModelTree(QTreeWidget):
    def __init__(self, parent=None):
        super(ModelTree, self).__init__(parent)

        self.top_level_names = [
            '坐标系',
            '几何',
            '网格',
            '载荷',
            '边界',
            '结果'
        ]

        self.setStyleSheet(
            "QTreeWidget::indicator:unchecked {image: url(Icons/Hide.png);}"
            "QTreeWidget::indicator:checked {image: url(Icons/Show.png);}"
        )

        self.setHeaderLabels(['', '编号', '颜色'])
        self.setColumnWidth(0, 160)
        self.setColumnWidth(1, 35)
        self.setColumnWidth(2, 35)

        for name in self.top_level_names:
            parent = QTreeWidgetItem(self)
            parent.setText(0, name)
            parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            parent.setCheckState(0, Qt.Checked)


class BottomAdditionalTab(QTabWidget):
    def __init__(self, parent=None):
        super(BottomAdditionalTab, self).__init__(parent)

        self.add_info_tab()

    def add_info_tab(self):
        self.info_tab = QWidget(self)
        self.info_tab.setObjectName('info_tab')
        self.addTab(self.info_tab, '信息')

        self.info_tab_layout = QVBoxLayout(self.info_tab)
        self.info_tab_layout.setObjectName('info_tab_layout')

        self.info_browser = QTextBrowser(self.info_tab)
        self.info_browser.setObjectName('info_browser')

        self.info_tab_layout.addWidget(self.info_browser)


class CentralWidget(QWidget):
    def __init__(self, parent=None):
        super(CentralWidget, self).__init__(parent)

        # 垂直部件
        self.vertical_layout = QVBoxLayout(self)
        self.vertical_layout.setObjectName('vertical_layout')

        # 顶部导航标签页
        self.navigation_tab = TopNavigationTab(self)
        self.navigation_tab.setObjectName('navigation_tab')

        # 水平分割器（左边添加模型树，右边添加垂直分割器）
        self.horizontal_splitter = QSplitter(self)
        self.horizontal_splitter.setObjectName('horizontal_splitter')
        self.horizontal_splitter.setOrientation(Qt.Horizontal)
        # 水平分割器添加左侧模型树
        self.tree_widget = ModelTree(self.horizontal_splitter)
        self.tree_widget.setObjectName('tree_widget')
        # 水平分割器添加垂直分割器（上边为主视图标签页，下边为附加标签页）
        self.vertical_splitter = QSplitter(self.horizontal_splitter)
        self.vertical_splitter.setObjectName('vertical_splitter')
        self.vertical_splitter.setOrientation(Qt.Vertical)
        # 垂直分割器添加主视图
        self.view_tab_widget = QTabWidget(self.vertical_splitter)
        self.view_tab_widget.setObjectName('view_tab_widget')
        self.size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.view_tab_widget.setSizePolicy(self.size_policy)
        # 垂直分割器添加附加部件
        self.additional_tab_widget = BottomAdditionalTab(self.vertical_splitter)
        self.additional_tab_widget.setObjectName('additional_tab_widget')

        self.vertical_layout.addWidget(self.navigation_tab)
        self.vertical_layout.addWidget(self.horizontal_splitter)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = CentralWidget()
    widget.show()
    app.exec_()
