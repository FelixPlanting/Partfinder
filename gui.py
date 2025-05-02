from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QSpinBox, QCheckBox, QPushButton, QMessageBox, QHeaderView
)
import sys


def launch_ui(fetch_messages_callback):
    app = QApplication(sys.argv)

    # the main window
    window = QWidget()
    window.setWindowTitle("Part Finder")
    window.resize(800, 600)

    # the layout
    layout = QVBoxLayout()
    label = QLabel("Part Finder")
    layout.addWidget(label)

    # how many emails
    count_label = QLabel("How many emails to read?")
    count_spinner = QSpinBox()
    count_spinner.setMinimum(1)
    count_spinner.setMaximum(100)
    count_spinner.setValue(10)
    layout.addWidget(count_label)
    layout.addWidget(count_spinner)

    # read/unread checkbox
    unread_checkbox = QCheckBox("Only unread emails?")
    unread_checkbox.setChecked(True)
    layout.addWidget(unread_checkbox)

    # the table (starts empty)
    table = QTableWidget()
    table.setColumnCount(3)
    table.setHorizontalHeaderLabels(["Sender", "Subject", "Parts"])
    table.horizontalHeader().setStretchLastSection(True)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    layout.addWidget(table)

    # button to actually get the emails
    def fetch_and_display():
        count = count_spinner.value()
        unread = unread_checkbox.isChecked()
        messages = fetch_messages_callback(limit=count, unread=unread)
        table.setRowCount(len(messages))
        for row, msg in enumerate(messages):
            table.setItem(row, 0, QTableWidgetItem(msg.get("Sender", "")))
            table.setItem(row, 1, QTableWidgetItem(msg.get("Subject", "")))
            table.setItem(row, 2, QTableWidgetItem(msg.get("Parts", "")))
        if not messages:
            QMessageBox.information(window, "No Messages", "No emails matched your filters.")

    button = QPushButton("Fetch Emails")
    button.clicked.connect(fetch_and_display)
    layout.addWidget(button)

    window.setLayout(layout)
    window.show()
    sys.exit(app.exec_())
