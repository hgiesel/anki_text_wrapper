from aqt import QAction, mw

from .gui_config.custom.tw_config import TWConfigDialog
from .lib.config import get_settings

from .utils import find_addon_by_name

def invoke_options():
    dialog = TWConfigDialog(mw)
    dialog.setupUi(get_settings())

    return dialog.exec_()

def setup_menu_option():
    action = QAction('Text Wrapper Settings...', mw)
    action.triggered.connect(invoke_options)
    mw.form.menuTools.addAction(action)

def setup_addon_manager():
    mw.addonManager.setConfigAction(__name__, invoke_options)
