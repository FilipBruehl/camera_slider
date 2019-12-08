import qstylizer.style


class MainWindowStyles:
    @staticmethod
    def main_window_style():
        css = qstylizer.style.StyleSheet()
        return css


class ConnectServerStyles:
    @staticmethod
    def button_style():
        css = qstylizer.style.StyleSheet()

        css.QPushButton.setValues(
            backgroundColor="transparent",
            borderWidth="2px",
            borderStyle="solid",
            borderRadius="5px"
        )
        css.QPushButton.enabled.setValues(
            color="#00c853",
            backgroundColor="#f5f5f5",
            borderColor="#f5f5f5"
        )
        css.QPushButton.disabled.setValues(
            color="#DB2828",
            borderColor="#DB2828"
        )
        return css

    @staticmethod
    def line_edit_style(valid=False):
        css = qstylizer.style.StyleSheet()

        if not valid:
            css.QLineEdit.setValues(
                backgroundColor="#f5f5f5",
                border="2px solid #DB2828",
                borderRadius="5px"
            )
        else:
            css.QLineEdit.setValues(
                backgroundColor="#f5f5f5",
                border="2px solid #00c853",
                borderRadius="5px"
            )
        return css
