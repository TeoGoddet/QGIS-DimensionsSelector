# Variable Selector QGIS Plugin

QGIS Plugin which adds a toolbar to QGIS for filtering features upon multiple layers on a common field (floor, year, project, ...).

## Configuration

Open the "Plugin" / "Variable Selector" / "Settings" dialog.

Click the "Add" button to create a new dimension, give it a name and a list of values separated by ",".

After acceptation of the settings dialog, a new combox will appear in the "Dimensions Selector" toolbar.

## Limitations

The plugin only set a project variable with the selected value of the dimensions, you are responsible to create opacity/rendering expresion to filter based on this value.
