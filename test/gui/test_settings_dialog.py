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

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtWidgets import QDialogButtonBox, QDialog

from dimensions_selector.core import Dimension, DimensionsManager
from dimensions_selector.gui.settings_dialog import DimensionsTableModel, SettingsDialog
from dimensions_selector.test.utils import add_layer


class DimensionsTableModelTest(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.rows = add_layer('rows.geojson', 'rows')
        self.dimensions = [
            Dimension(name="column", options="A,B,C,D", current_value="A"),
            Dimension(name="row", table=self.rows, value_field="id", label_field="name", current_value=1),
        ]

    def test_items(self):
        model = DimensionsTableModel(list(self.dimensions))
        self.assertEqual(model.items(), self.dimensions)

    def test_addItem(self):
        model = DimensionsTableModel([])
        for dimension in self.dimensions:
            model.addItem(dimension)
        self.assertEqual(model.items(), self.dimensions)

    def test_removeRows(self):
        model = DimensionsTableModel(list(self.dimensions))
        model.removeRows(0, 1)
        self.assertEqual(model.items(), [self.dimensions[1]])

    def test_columnIndex(self):
        model = DimensionsTableModel(list(self.dimensions))
        self.assertEqual(model.columnIndex("name"), 0)
        self.assertEqual(model.columnIndex("options"), 1)
        self.assertEqual(model.columnIndex("table"), 2)
        self.assertEqual(model.columnIndex("active"), 3)

    def test_columnCount(self):
        model = DimensionsTableModel(list(self.dimensions))
        self.assertEqual(model.columnCount(), 4)

    def test_rowCount(self):
        model = DimensionsTableModel(list(self.dimensions))
        self.assertEqual(model.rowCount(), 2)

    def test_headerData(self):
        model = DimensionsTableModel(list(self.dimensions))

        self.assertEqual(model.headerData(0, Qt.Horizontal), "Name")
        self.assertEqual(model.headerData(1, Qt.Horizontal), "Choices")
        self.assertEqual(model.headerData(2, Qt.Horizontal), "Table")
        self.assertEqual(model.headerData(3, Qt.Horizontal), "Active")

        self.assertEqual(model.headerData(0, Qt.Vertical), "0")
        self.assertEqual(model.headerData(1, Qt.Vertical), "1")

    def test_flags(self):
        model = DimensionsTableModel(list(self.dimensions))
        self.assertEqual(
            model.flags(model.index(0, 0)),
            Qt.ItemFlags(
                Qt.ItemIsSelectable |
                Qt.ItemIsEditable |
                Qt.ItemIsEnabled
            )
        )
        self.assertEqual(
            model.flags(model.index(0, 1)),
            Qt.ItemFlags(
                Qt.ItemIsSelectable |
                Qt.ItemIsEditable |
                Qt.ItemIsEnabled
            )
        )
        self.assertEqual(
            model.flags(model.index(0, 2)),
            Qt.ItemFlags(
                Qt.ItemIsSelectable |
                Qt.ItemIsEditable |
                Qt.ItemIsEnabled
            )
        )
        self.assertEqual(
            model.flags(model.index(0, 3)),
            Qt.ItemFlags(
                Qt.ItemIsSelectable |
                Qt.ItemIsEditable |
                Qt.ItemIsEnabled |
                Qt.ItemIsUserCheckable
            )
        )

    def test_data(self):
        model = DimensionsTableModel(list(self.dimensions))
        self.assertEqual(model.data(model.index(0, 0), Qt.DisplayRole), "column")
        self.assertEqual(model.data(model.index(0, 0), Qt.EditRole), "column")
        self.assertEqual(model.data(model.index(0, 1), Qt.DisplayRole), "A,B,C,D")
        self.assertEqual(model.data(model.index(0, 1), Qt.EditRole), "A,B,C,D")
        self.assertEqual(model.data(model.index(0, 2), Qt.DisplayRole), "")
        self.assertEqual(model.data(model.index(0, 2), Qt.EditRole), None)
        self.assertEqual(model.data(model.index(0, 3), Qt.CheckStateRole), Qt.Checked)

        self.assertEqual(model.data(model.index(1, 0), Qt.DisplayRole), "row")
        self.assertEqual(model.data(model.index(1, 0), Qt.EditRole), "row")
        self.assertEqual(model.data(model.index(1, 1), Qt.DisplayRole), "")
        self.assertEqual(model.data(model.index(1, 1), Qt.EditRole), "")
        self.assertEqual(model.data(model.index(1, 2), Qt.DisplayRole), "rows")
        self.assertEqual(model.data(model.index(1, 2), Qt.EditRole), self.rows)
        self.assertEqual(model.data(model.index(1, 3), Qt.CheckStateRole), Qt.Checked)

    def test_setData(self):
        dimensions = list(self.dimensions)
        model = DimensionsTableModel(dimensions)

        model.setData(model.index(0, 0), "new_name", Qt.EditRole)
        self.assertEqual(dimensions[0].name, "new_name")

        model.setData(model.index(0, 1), "A,B,C,D,E", Qt.EditRole)
        self.assertEqual(dimensions[0].options, "A,B,C,D,E")

        new_rows = add_layer('rows.geojson', 'new_rows')
        model.setData(model.index(0, 2), new_rows, Qt.EditRole)
        self.assertEqual(dimensions[0].table, new_rows)

        model.setData(model.index(0, 3), Qt.Unchecked, Qt.CheckStateRole)
        self.assertEqual(dimensions[0].active, False)


class SettingsDialogTest(unittest.TestCase):
    """Test dialog works."""

    def setUp(self):
        """Runs before each test."""
        self.manager = DimensionsManager('dimensions_selector')
        self.dialog = SettingsDialog(self.manager, None)

    def tearDown(self):
        """Runs after each test."""
        self.dialog = None
        self.manager.deleteLater()

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

    def test_on_addDimensionButton_clicked(self):
        self.dialog.on_addDimensionButton_clicked()


if __name__ == "__main__":
    suite = unittest.makeSuite(SettingsDialogTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
