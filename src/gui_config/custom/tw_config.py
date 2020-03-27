import os
import json

from pathlib import Path
from itertools import groupby
from jsonschema import validate, RefResolver, Draft7Validator

from aqt import mw
from aqt.qt import QDialog, QWidget, QAction
from aqt.utils import getText, showWarning, showInfo

from ...lib.config import deserialize_setting, serialize_setting, write_settings

from ..tw_config_ui import Ui_TWConfig

from .tw_setting_update import TWSettingUpdate
from .tw_wrap_tab import TWWrapTab

def sort_negative_first(v):
    return abs(int(v.name)) * 2 if int(v.name) < 0 else abs(int(v.name)) * 2 + 1

def save_settings(settings):
    serializedSettings = [serialize_setting(setting) for setting in settings]
    write_settings(serializedSettings)

class TWConfigDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent=parent)

        self.ui = Ui_TWConfig()
        self.ui.setupUi(self)

        self.ui.cancelButton.clicked.connect(self.reject)

    def setupUi(self, settings, startId=0):
        self.settings = settings

        def saveCurrentSetting(isClicked):
            nonlocal self
            nonlocal settings

            setting_data = self.ui.configWidget.exportData()
            settings = setting_data

            save_settings(settings)
            self.accept()

        self.ui.saveButton.clicked.connect(saveCurrentSetting)

        self.ui.helpButton.clicked.connect(self.showHelp)
        self.ui.aboutButton.clicked.connect(self.showAbout)
        self.ui.importButton.clicked.connect(self.importDialog)

    def updateConfigWidget(self, setting):
        self.ui.configWidget.setupUi(setting)

    def importDialog(self):
        setting_data = self.ui.configWidget.exportData()

        def updateAfterImport(new_data):
            # name of new_data is not actually used
            self.settings = deserialize_setting(setting_data.model_name, new_data)
            self.updateConfigWidget(self.settings)

        dirpath = Path(f'{os.path.dirname(os.path.realpath(__file__))}', '../../json_schemas/setting.json')
        schema_path = dirpath.absolute().as_uri()

        with dirpath.open('r') as jsonfile:
            schema = json.load(jsonfile)
            resolver = RefResolver(
                schema_path,
                schema,
            )

            validator = Draft7Validator(schema, resolver=resolver, format_checker=None)

            dial = TWSettingUpdate(mw)
            dial.setupUi(
                json.dumps(serialize_setting(self.settings), sort_keys=True, indent=4),
                validator,
                updateAfterImport,
            )
            dial.exec_()

    def showHelp(self):
        pass
    def showAbout(self):
        pass
