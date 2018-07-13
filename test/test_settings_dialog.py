# coding=utf-8
"""Dialog test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'info@camptocamp.com'
__date__ = '2018-07-05'
__copyright__ = 'Copyright 2018, Camptocamp'

import unittest

from qgis.PyQt.QtWidgets import QDialogButtonBox, QDialog

from dimensions_selector.core import DimensionsManager
from dimensions_selector.gui.settings_dialog import SettingsDialog


class SettingsDialogTest(unittest.TestCase):
    """Test dialog works."""

    def setUp(self):
        """Runs before each test."""
        manager = DimensionsManager('dimensions_selector')
        self.dialog = SettingsDialog(manager, None)

    def tearDown(self):
        """Runs after each test."""
        self.dialog = None

    def test_dialog_ok(self):
        """Test we can click OK."""
        button = self.dialog.button_box.button(QDialogButtonBox.Ok)
        button.click()
        result = self.dialog.result()
        self.assertEqual(result, QDialog.Accepted)

    def test_dialog_cancel(self):
        """Test we can click cancel."""
        button = self.dialog.button_box.button(QDialogButtonBox.Cancel)
        button.click()
        result = self.dialog.result()
        self.assertEqual(result, QDialog.Rejected)

if __name__ == "__main__":
    suite = unittest.makeSuite(SettingsDialogTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
