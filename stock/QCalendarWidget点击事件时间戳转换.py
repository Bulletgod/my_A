import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCalendarWidget
from PyQt5.QtCore import QDateTime, QDate, QTime, Qt


class CalendarWidgetExample(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.calendar_widget = QCalendarWidget(self)
        self.calendar_widget.selectionChanged.connect(self.handle_selection_changed)

        layout.addWidget(self.calendar_widget)
        self.setLayout(layout)

    def handle_selection_changed(self):
        # 获取点击日期时间
        selected_date = self.calendar_widget.selectedDate()
        # 获取当前系统日期时间
        current_datetime = QDateTime.currentDateTime()

        if selected_date >= current_datetime.date():
            selected_timestamp = current_datetime.toSecsSinceEpoch()
        else:
            # 设置时间为中午12:00:00
            selected_datetime = QDateTime(selected_date, QTime(17, 0), Qt.TimeSpec.LocalTime)
            # 将所选日期和时间转换为时间戳（秒级）
            selected_timestamp = selected_datetime.toSecsSinceEpoch()

        print("Selected Date:", selected_date.toString(Qt.ISODate))   # Selected Date: 2023-08-18
        # print("Selected DateTime:", selected_datetime.toString("yyyy-MM-dd hh:mm:ss"))   # Selected DateTime: 2023-08-18 12:00:00
        print("Selected Timestamp:", selected_timestamp)    # Selected Timestamp: 1692331200




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalendarWidgetExample()
    window.setWindowTitle('Calendar Widget Example')
    window.show()
    sys.exit(app.exec_())
