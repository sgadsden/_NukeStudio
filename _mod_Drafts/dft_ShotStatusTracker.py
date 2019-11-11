#import nuke, nukescripts
import json, sys, os
from Qt import QtWidgets, QtGui, QtCore




class StatusBox(QtWidgets.QComboBox):
    '''
    source: https://stackoverflow.com/questions/3241830/qt-how-to-disable-mouse-scrolling-of-qcombobox
    '''
    def __init__(self, scrollWidget=None, *args, **kwargs):
        super(StatusBox, self).__init__(*args, **kwargs)
        self.scrollWidget=scrollWidget
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

    def wheelEvent(self, *args, **kwargs):
        if self.hasFocus():
            QtGui.QComboBox.wheelEvent(self, *args, **kwargs)
        else:
            try:
                self.scrollWidget.wheelEvent(*args, **kwargs)
            except:
                pass



class DataAdd(QtWidgets.QDialog):
    entry = None
    def __init__(self):
        super(DataAdd, self).__init__()

        self.ls_header = ['FARM', 'RENDERED', 'VIEWED', 'DAILIED','NOTED','SENT','FINAL']

        self.st_shot = QtWidgets.QLineEdit()
        self.st_shot.setPlaceholderText('Shot (ie. str050_1010)')
        self.st_task = QtWidgets.QLineEdit()
        self.st_task.setPlaceholderText('Task (ie. mastercomp)')
        self.st_task.setCompleter(QtWidgets.QCompleter(['comp', 'mastercomp','precomp-']))
        self.lb_version = QtWidgets.QLabel('Version: ')
        self.no_version = QtWidgets.QSpinBox()
        self.bx_status = QtWidgets.QComboBox()
        self.bx_status.addItems(self.ls_header)
        self.st_comments = QtWidgets.QLineEdit()
        self.bt_add = QtWidgets.QPushButton('ADD')
        self.bt_add.clicked.connect(self.onClicked)

        self.layout_master = QtWidgets.QVBoxLayout()
        self.layout_version = QtWidgets.QHBoxLayout()
        self.layout_version.addWidget(self.st_shot)
        self.layout_version.addWidget(self.st_task)
        self.layout_version.addWidget(self.lb_version)
        self.layout_version.addWidget(self.no_version)
        self.layout_version.addWidget(self.bx_status)
        self.layout_master.addLayout(self.layout_version)
        self.layout_master.addWidget(self.st_comments)
        self.layout_master.addWidget(self.bt_add)
        self.setLayout(self.layout_master)
        self.setWindowTitle("Add a version")
        self.show()


    def onClicked(self):
        '''collect data from GUI and assign to variables'''

        self.entry = {}

        thisShot, thisTask, thisVersion, thisStatus, thisComments = None, None, None, None, None

        thisShot = self.st_shot.text()
        thisTask = self.st_task.text()
        thisVersion = int(self.no_version.text())
        thisStatus = self.bx_status.currentText()
        thisComments = self.st_comments.text()
        self.entry['SHOT']=thisShot
        self.entry['TASK']=thisTask
        self.entry['VERSION']=thisVersion
        self.entry['STATUS']=thisStatus
        self.entry['COMMENTS']=thisComments
        self.entry['NOTES']=""
        #print "added\n---SHOT: %s\n---TASK: %s\n---VERSION: %s\n---STATUS: %s\n---COMMENTS: %s" % (thisShot, thisTask, thisVersion, thisStatus, thisComments)

        self.close()


class Main_ShotStatusTracker(QtWidgets.QDialog):
    def __init__(self):
        super(Main_ShotStatusTracker,self).__init__()

        self.bt_reload = QtWidgets.QPushButton('Reload')
        self.bt_reload.clicked.connect(self.onReload)
        self.bt_save = QtWidgets.QPushButton('Save')
        self.bt_save.clicked.connect(self.onSave)
        self.bt_add = QtWidgets.QPushButton('Add')
        self.bt_add.clicked.connect(self.onAdd)
        self.bt_remove = QtWidgets.QPushButton('Remove')
        self.bt_remove.clicked.connect(self.onRemove)
        self.core = Core_ShotStatusTracker()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.layout_button = QtWidgets.QHBoxLayout()
        self.layout_button.setAlignment(QtCore.Qt.AlignLeft)
        self.layout_button.addWidget(self.bt_add)
        self.layout_button.addWidget(self.bt_remove)
        self.layout_button.addStretch(1)
        self.layout_button.addWidget(self.bt_reload)
        self.layout_button.addWidget(self.bt_save)

        self.layout.addWidget(self.core)
        self.layout.addLayout(self.layout_button)
        self.resize(800,500)
        self.setLayout(self.layout)
        self.setWindowTitle("Shot Status Tracker - beta")


    def getCellValue(self, core_obj, idx_r, idx_c, column):
        '''gets the value for current cell, if cell type differ from cell to cell'''

        cellTypes={'SHOT': 'item', 'TASK': 'item', 'VERSION': 'integer', 'STATUS': 'combo', 'COMMENTS': 'item', 'NOTES': 'item'}

        val_cell = None

        if cellTypes[column] == 'item':
            val_cell = core_obj.item(idx_r,idx_c).text()
        elif cellTypes[column] == 'integer':
            val_cell = int(core_obj.item(idx_r,idx_c).text().replace('v',''))
        elif cellTypes[column] == 'combo':
            val_cell = core_obj.cellWidget(idx_r,idx_c).currentText()
        return val_cell


    def onSave(self):
        '''when save button is pressed'''

        core = self.core
        out_path = os.path.join(core.json_folder,'ShotStatusTracker_Datasets_onSave.json')
        allRow = core.rowCount()
        allColumn = core.columnCount()
        column = core.ls_header

        ls_out = []

        for r in range(allRow): # row
            idx_r = r
            dic_row = {} # resets column value for every row
            for idx_c, c in enumerate(column): # column
                dic_row[c] = self.getCellValue(core, idx_r, idx_c, c)
            ls_out.append(dic_row)

        with open(out_path, 'w') as f:
            f.write(json.dumps(ls_out,indent=2))

        print "data save to json: %s entries" % len(ls_out)


    def onReload(self):
        '''when reload button is pressed'''
        self.core.setDefault()
        print "data load from json"

    def onAdd(self):
        '''add data entry'''
        core = self.core
        core.setRowCount(core.rowCount()+1)
        r = core.rowCount()-1
        d = DataAdd()
        d.show()
        thisData = d.entry
        for i,c in enumerate(core.ls_header):
            core.setCell(thisData, r, c, i)
            print r, c, i


    def onRemove(self):
        '''remove data of the last row'''
        core = self.core
        core.setRowCount(core.rowCount()-1)


    def run(self):
        '''run panel instance'''
        self.show()
        self.activateWindow()
        self.raise_()


class Core_ShotStatusTracker(QtWidgets.QTableWidget):
    def __init__(self):
        super(Core_ShotStatusTracker, self).__init__()

        self.json_filename = 'ShotStatusTracker_datasets.json'
        self.json_folder = '/Users/Tianlun/Desktop/_NukeTestScript/doc/'
        # self.json_folder = '/net/homes/tjiang/Documents/'
        self.json_file_path = os.path.join(self.json_folder,self.json_filename)

        self.data = self.getData()
        self.ls_header = ['SHOT', 'TASK', 'VERSION','STATUS','COMMENTS', 'NOTES']
        self.ls_status = ['FARM', 'RENDERED', 'VIEWED', 'DAILIED','NOTED','SENT','FINAL']
        self.resize(800,500)
        self.setShowGrid(False)
        self.setSortingEnabled(False)
        self.setRowCount(len(self.data))
        self.setColumnCount(len(self.ls_header))
        self.setHorizontalHeaderLabels(self.ls_header)
        # for i, h in enumerate(self.ls_header):
        #     self.setHorizontalHeaderItem(i,QtWidgets.QTableWidgetItem(h))
        self.horizontalHeader().setStretchLastSection(True)

        self.setColumnWidth(0,125)
        self.setColumnWidth(1,150)
        self.setColumnWidth(2,80)
        self.setColumnWidth(3,100)
        self.setColumnWidth(4,150)

        self.setDefault()

    def setDefault(self):
        '''set default value when instancing'''
        self.setTable(self.getData())


    def int2str(self, int):
        '''convert integer to string'''
        return "v%03d" % int


    def setCell(self, d, r, c, i):
        '''
        set cell value
        d: data, r: row, c: column value, i: column index
        '''
        thisData, thisCell = None, None
        if c=='SHOT':
            thisData = d[c]
            thisCell = QtWidgets.QTableWidgetItem(thisData)
            thisCell.setTextAlignment(QtCore.Qt.AlignCenter)
            self.setItem(r, i, thisCell)
        elif c=='TASK':
            thisData = d[c]
            thisCell = QtWidgets.QTableWidgetItem(thisData)
            self.setItem(r, i, thisCell)
        elif c=='VERSION':
            thisData = self.int2str(d[c])
            thisCell = QtWidgets.QTableWidgetItem(thisData)
            thisCell.setTextAlignment(QtCore.Qt.AlignCenter)
            self.setItem(r, i, thisCell)
        elif c=='STATUS':
            thisData = d[c]
            thisCell = StatusBox()
            # thisCell.setStyleSheet("QComboBox::down-arrow {border: 1px; image: none}")
            # thisCell.insertSeparator(0)
            thisCell.addItems(self.ls_status)
            thisCell.setCurrentIndex(thisCell.findText(thisData))
            self.setCellWidget(r, i, thisCell)
        elif c=='COMMENTS':
            thisData = d[c]
            thisCell = QtWidgets.QTableWidgetItem(thisData)
            thisCell.setToolTip(thisData)
            # self.setItem(r, i, thisCell)
        elif c=='NOTES':
            thisData = d[c]
            thisCell = QtWidgets.QTableWidgetItem(thisData)
            thisCell.setToolTip(thisData)
            self.setItem(r, i, thisCell)


    def setTable(self, data):
        '''populating table with data'''

        for r, d in enumerate(data):
            #r: row number, d: data for this row - 'SHOT', 'TASK', 'VERSION', 'COMMENTS', 'NOTES'
            # self.setRowHeight(r,24)
            for i, c in enumerate(self.ls_header):
                # i: column index, c: column title
                # SHOT: String | TASK: String with completer | VERSION: Integer | COMMENTS: String | NOTES: String
                self.setCell(d,r,c,i)

        self.setAlternatingRowColors(True)


    def getData(self):
        '''get data from json file'''
        with open(self.json_file_path, 'r') as f:
            data = json.load(f)

        return data



# Show the panel


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ShotStatusTracker = Main_ShotStatusTracker()
    ShotStatusTracker.run()
    app.exec_()
else:
    ShotStatusTracker = Main_ShotStatusTracker()
    ShotStatusTracker.run()