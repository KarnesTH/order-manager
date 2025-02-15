from PyQt6.QtWidgets import QMessageBox, QWidget


def show_error(parent: QWidget, message: str, title: str = "Error"):
    """Show error message box."""
    QMessageBox.critical(parent, title, message)

def show_warning(parent: QWidget, message: str, title: str = "Warning"):
    """Show warning message box."""
    QMessageBox.warning(parent, title, message)

def show_info(parent: QWidget, message: str, title: str = "Information"):
    """Show info message box."""
    QMessageBox.information(parent, title, message)

def show_confirmation(
    parent: QWidget,
    message: str,
    title: str = "Confirm"
) -> bool:
    """
    Show confirmation dialog.

    Returns:
        bool: True if user confirmed, False otherwise
    """
    reply = QMessageBox.question(
        parent,
        title,
        message,
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        QMessageBox.StandardButton.No
    )
    return reply == QMessageBox.StandardButton.Yes
