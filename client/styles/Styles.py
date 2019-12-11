import qstylizer.style
from styles.Colors import Colors


class MainWindowStyles:
    @staticmethod
    def main_window_information_style():
        css = qstylizer.style.StyleSheet()

        css.QGroupBox.setValues(
            backgroundColor=Colors.TRANSPARENT,
            border=f"2px solid {Colors.COLOR_BLACK}",
            borderRadius="5px"
        )

        css.QLabel.setValues(
            backgroundColor=Colors.TRANSPARENT,
            border="none",
            color=Colors.COLOR_BLACK
        )
        css.QLabel.disabled.setValues(
            backgroundColor=Colors.TRANSPARENT,
            border="none",
            color=Colors.DISABLED
        )
        css.QLabel.enabled.setValues(
            backgroundColor=Colors.TRANSPARENT,
            border="none",
            color=Colors.COLOR_ERROR
        )
        css['QLabel#serverip'].setValues(
            backgroundColor=Colors.TRANSPARENT,
            border="none",
            color=Colors.COLOR_BLACK
        )
        css['QLabel#serverip[connected="false"]'].setValues(
            color=Colors.COLOR_ERROR
        )
        css['QLabel#serverip[connected="true"]'].setValues(
            color=Colors.COLOR_SUCCESS
        )
        css['QLabel#cameraname'].setValues(
            backgroundColor=Colors.TRANSPARENT,
            border="none",
            color=Colors.COLOR_ERROR
        )
        css['QLabel#cameraname[connected="false"]'].setValues(
            color=Colors.COLOR_ERROR
        )
        css['QLabel#cameraname[connected="true"]'].setValues(
            color=Colors.COLOR_SUCCESS
        )

        return css

    @staticmethod
    def main_window_menu_style():
        css = qstylizer.style.StyleSheet()

        css.QMenuBar.item.selected.setValues(
            backgroundColor=Colors.BACKGROUND_SECONDARY
        )
        css.QMenu.selected.enabled.setValues(
            backgroundColor=Colors.BACKGROUND_SECONDARY,
            color=Colors.COLOR_BLACK
        )

        return css

    @staticmethod
    def main_window_settings_style():
        css = qstylizer.style.StyleSheet()

        css.QGroupBox.setValues(
            backgroundColor=Colors.TRANSPARENT,
            border=f"2px solid {Colors.COLOR_BLACK}",
            borderRadius="5px"
        )

        css.QLabel.setValues(
            backgroundColor=Colors.TRANSPARENT,
            border="none",
            color=Colors.COLOR_BLACK
        )
        css.QLabel.disabled.setValues(
            backgroundColor=Colors.TRANSPARENT,
            border="none",
            color=Colors.DISABLED
        )
        css.QLabel.enabled.setValues(
            backgroundColor=Colors.TRANSPARENT,
            border="none",
            color=Colors.COLOR_BLACK
        )

        css.QComboBox.setValues(
            backgroundColor=Colors.TRANSPARENT,
            border="none",
            color=Colors.COLOR_BLACK
        )
        css.QComboBox.disabled.setValues(
            backgroundColor=Colors.TRANSPARENT,
            border="none",
            color=Colors.DISABLED
        )
        css.QComboBox.enabled.setValues(
            backgroundColor=Colors.TRANSPARENT,
            border="none",
            color=Colors.COLOR_BLACK
        )

        css.QLineEdit.setValues(
            backgroundColor=Colors.BACKGROUND_SECONDARY,
            color=Colors.COLOR_BLACK,
            border="2px solid",
            borderRadius="5px"
        )
        css.QLineEdit.disabled.setValues(
            backgroundColor=Colors.TRANSPARENT,
            color=Colors.DISABLED,
            border="none"
        )
        css.QLineEdit.enabled.setValues(
            color=Colors.COLOR_BLACK,
            borderColor=Colors.BACKGROUND_SECONDARY
        )

        css.QPushButton.setValues(
            backgroundColor=Colors.BACKGROUND_SECONDARY,
            borderWidth="2px",
            borderStyle="solid",
            borderRadius="5px"
        )
        css.QPushButton.enabled.setValues(
            backgroundColor=Colors.BACKGROUND_SECONDARY,
            color=Colors.COLOR_BLACK,
            borderColor=Colors.BACKGROUND_SECONDARY
        )
        css.QPushButton.disabled.setValues(
            backgroundColor=Colors.TRANSPARENT,
            color=Colors.DISABLED,
            border="none"
        )

        return css


class ConnectServerStyles:
    @staticmethod
    def button_style():
        css = qstylizer.style.StyleSheet()

        css.QPushButton.setValues(
            backgroundColor=Colors.TRANSPARENT,
            borderWidth="2px",
            borderStyle="solid",
            borderRadius="5px"
        )
        css.QPushButton.enabled.setValues(
            color=Colors.COLOR_SUCCESS,
            backgroundColor=Colors.BACKGROUND_SECONDARY,
            borderColor=Colors.BACKGROUND_SECONDARY
        )
        css.QPushButton.disabled.setValues(
            color=Colors.COLOR_ERROR,
            borderColor=Colors.COLOR_ERROR
        )
        return css

    @staticmethod
    def line_edit_style():
        css = qstylizer.style.StyleSheet()

        css.QLineEdit.setValues(
            backgroundColor=Colors.BACKGROUND_SECONDARY,
            border=f"2px solid {Colors.COLOR_BLACK}",
            borderRadius="5px",
            color=Colors.COLOR_BLACK
        )
        css['QLineEdit[valid="true"]'].setValues(
            backgroundColor=Colors.BACKGROUND_SECONDARY,
            border=f"2px solid {Colors.COLOR_SUCCESS}",
            borderRadius="5px",
            color=Colors.COLOR_SUCCESS
        )
        css['QLineEdit[valid="false"]'].setValues(
            backgroundColor=Colors.BACKGROUND_SECONDARY,
            border=f"2px solid {Colors.COLOR_ERROR}",
            borderRadius="5px",
            color=Colors.COLOR_ERROR
        )
        return css
