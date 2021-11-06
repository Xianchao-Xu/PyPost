# coding: utf-8
# author: xuxc

import re

__all__ = [
    'FileParser',
]


class FileParser:
    def __init__(self, filename):
        self.filename = filename
        self.type = ''
        self.node_ids = list()
        self.nodes = list()
        self.element_ids = list()
        self.element_types = list()
        self.elements = list()
        self.msg = None
        self.succeed = False

    def parse_fem(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as fr:
                line = fr.readline()
                while line:
                    line = line.strip().lower()
                    if line.startswith('#') or line == '':
                        pass
                    elif line[:7] != '** type':
                        self.msg = "<font color='red'>文件格式异常，打开失败：{}<font>".format(self.filename)
                        return
                    else:
                        data_type = line.split(',')[1]
                        if data_type.strip() == 'scatter':
                            self.type = 'scatter'
                            self.parse_fem_scatter()
                            self.succeed = True
                        elif data_type.strip() == 'mesh':
                            self.type = 'mesh'
                            self.parse_fem_mesh()
                            self.succeed = True
                        return
                    line = fr.readline()
        except ValueError as value_error:
            self.msg = str(value_error)

    def parse_fem_mesh(self):
        with open(self.filename, 'r', encoding='utf-8') as fr:
            line = fr.readline()
            while line:
                line = line.strip().lower()
                if line.startswith('**') or line.startswith('#') or line == '':
                    pass
                elif line.startswith('* node'):
                    node_num = int(line.split(',')[1])
                    for i in range(node_num):
                        line = fr.readline().strip()
                        line = re.split('[ ,;]', line)
                        line = [num for num in line if num != '']
                        node_id = int(line[0])
                        node = [0.0, 0.0, 0.0]
                        coord = [float(num) for num in line[1:]]
                        for j in range(len(coord)):
                            node[j] = coord[j]
                        self.node_ids.append(node_id)
                        self.nodes.append(node)
                elif line.startswith('* element'):
                    element_num = int(line.split(',')[1])
                    for i in range(element_num):
                        line = fr.readline().strip()
                        line = re.split('[ ,;]', line)
                        line = [int(num) for num in line if num != '']
                        self.element_ids.append(line[0])
                        self.element_types.append(line[1])
                        self.elements.append(line[2:])
                line = fr.readline()
        self.msg = """成功打开文件：{}\n  节点数：{}\n  单元数：{}""".format(
            self.filename, len(self.nodes), len(self.elements))

    def parse_fem_scatter(self):
        with open(self.filename, 'r', encoding='utf-8') as fr:
            node_id = 0
            line = fr.readline()
            while line:
                line = line.strip().lower()
                if line.startswith('#') or line.startswith('**') or line == '':
                    pass
                else:
                    line = re.split('[ ,;]', line)
                    line = [float(num) for num in line if num != '']
                    node = [0.0, 0.0, 0.0]
                    for j in range(len(line)):
                        node[j] = line[j]
                    node_id += 1
                    self.node_ids.append(node_id)
                    self.nodes.append(node)
                line = fr.readline()
        self.msg = """成功打开文件：{}\n  节点数：{}""".format(self.filename, len(self.nodes))
