import sys
from PySide6.QtWidgets import (QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
                               QListWidget, QStackedWidget, QMessageBox,
                               QStatusBar, QToolBar, QMenuBar, QMenu,
                               QApplication, QLabel, QFrame)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QSize

from tabs.employee_tab import EmployeeTab
from tabs.attendance_tab import AttendanceTab
from tabs.leave_tab import LeaveTab
from tabs.payroll_tab import PayrollTab
from tabs.reports_tab import ReportsTab
from tabs.dashboard_tab import DashboardTab   # new import

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Management System")
        self.setMinimumSize(1200, 700)

        # Create menu bar
        self.create_menu_bar()

        # # Create toolbar
        # self.create_toolbar()

        # Central widget with sidebar and stacked content
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar (vertical navigation)
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(200)
        self.sidebar.addItem(" Employees")      # index 0
        self.sidebar.addItem(" Attendance")     # index 1
        self.sidebar.addItem(" Leaves")          # index 2
        self.sidebar.addItem(" Payroll")         # index 3
        self.sidebar.addItem(" Reports")         # index 4
        self.sidebar.addItem(" Dashboard")       # index 5 (new)
        self.sidebar.currentRowChanged.connect(self.switch_page)

        # Stacked widget for pages
        self.stacked_widget = QStackedWidget()

        # Create pages
        self.employee_page = EmployeeTab()
        self.attendance_page = AttendanceTab()
        self.leave_page = LeaveTab()
        self.payroll_page = PayrollTab()
        self.reports_page = ReportsTab()
        self.dashboard_page = DashboardTab()       # new page

        self.stacked_widget.addWidget(self.employee_page)      # 0
        self.stacked_widget.addWidget(self.attendance_page)    # 1
        self.stacked_widget.addWidget(self.leave_page)         # 2
        self.stacked_widget.addWidget(self.payroll_page)       # 3
        self.stacked_widget.addWidget(self.reports_page)       # 4
        self.stacked_widget.addWidget(self.dashboard_page)     # 5

        # Add sidebar and stacked to layout
        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stacked_widget, 1)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready", 5000)

        # Set initial selection (Employees)
        self.sidebar.setCurrentRow(0)

        # Apply enhanced styles
        self.apply_enhanced_styles()

    def create_menu_bar(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("📁 File")
        exit_action = QAction("🚪 Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu("✏️ Edit")
        add_emp_action = QAction(" Add Employee", self)
        add_emp_action.triggered.connect(lambda: self.switch_page(0))
        edit_menu.addAction(add_emp_action)

        mark_att_action = QAction(" Mark Attendance", self)
        mark_att_action.triggered.connect(lambda: self.switch_page(1))
        edit_menu.addAction(mark_att_action)

        apply_leave_action = QAction(" Apply Leave", self)
        apply_leave_action.triggered.connect(lambda: self.switch_page(2))
        edit_menu.addAction(apply_leave_action)

        generate_payroll_action = QAction(" Generate Payroll", self)
        generate_payroll_action.triggered.connect(lambda: self.switch_page(3))
        edit_menu.addAction(generate_payroll_action)

        # View menu
        view_menu = menubar.addMenu("👁️ View")
        refresh_action = QAction("🔄 Refresh", self)
        refresh_action.triggered.connect(self.refresh_all_tabs)
        view_menu.addAction(refresh_action)

        # Help menu
        help_menu = menubar.addMenu("❓ Help")
        about_action = QAction("ℹ️ About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    # def create_toolbar(self):
    #     toolbar = QToolBar("Main Toolbar")
    #     toolbar.setIconSize(QSize(32, 32))
    #     self.addToolBar(toolbar)

    #     add_emp_action = QAction("➕ Add Emp", self)
    #     add_emp_action.triggered.connect(lambda: self.switch_page(0))
    #     toolbar.addAction(add_emp_action)

    #     mark_att_action = QAction("📝 Attendance", self)
    #     mark_att_action.triggered.connect(lambda: self.switch_page(1))
    #     toolbar.addAction(mark_att_action)

    #     leave_action = QAction(" Leave", self)
    #     leave_action.triggered.connect(lambda: self.switch_page(2))
    #     toolbar.addAction(leave_action)

    #     payroll_action = QAction("💰 Payroll", self)
    #     payroll_action.triggered.connect(lambda: self.switch_page(3))
    #     toolbar.addAction(payroll_action)

    #     reports_action = QAction("📊 Reports", self)
    #     reports_action.triggered.connect(lambda: self.switch_page(4))
    #     toolbar.addAction(reports_action)

    #     toolbar.addSeparator()

    #     refresh_action = QAction("🔄 Refresh", self)
    #     refresh_action.triggered.connect(self.refresh_all_tabs)
    #     toolbar.addAction(refresh_action)

    def switch_page(self, index):
        """Switch the stacked widget page and update sidebar selection."""
        self.stacked_widget.setCurrentIndex(index)
        self.sidebar.blockSignals(True)
        self.sidebar.setCurrentRow(index)
        self.sidebar.blockSignals(False)
        self.status_bar.showMessage(f"Switched to {self.sidebar.item(index).text()}", 3000)

    def refresh_all_tabs(self):
        """Refresh data in all pages, including dashboard."""
        try:
            self.employee_page.load_employees()
            self.attendance_page.load_today_attendance()
            self.leave_page.load_leaves()
            self.payroll_page.load_payroll_records()
            self.reports_page.load_employee_report()
            self.reports_page.load_attendance_report()
            self.reports_page.load_payroll_report()
            self.dashboard_page.update_charts()       # new line
            self.status_bar.showMessage("All data refreshed", 3000)
        except Exception as e:
            QMessageBox.warning(self, "Refresh Error", str(e))

    def show_about(self):
        QMessageBox.about(self, "About Employee Management System",
                          "<b>Employee Management System</b><br>"
                          "Version 1.0<br><br>"
                          "A comprehensive desktop application for managing employees, "
                          "attendance, leaves, and payroll.<br><br>"
                          "Built with PySide6 and MySQL.")

    def apply_enhanced_styles(self):
        """Modern styles with sidebar styling."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QListWidget {
                background-color: #2c3e50;
                color: white;
                font-size: 14px;
                font-weight: bold;
                border: none;
                outline: none;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #34495e;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QListWidget::item:hover:!selected {
                background-color: #34495e;
            }
            QStackedWidget {
                background-color: white;
                border: none;
            }
            QMenuBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #e0e0e0, stop:1 #c0c0c0);
                spacing: 5px;
            }
            QMenuBar::item:selected {
                background: #0078d7;
                color: white;
            }
            QToolBar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #f0f0f0, stop:1 #d0d0d0);
                border: 1px solid #a0a0a0;
                spacing: 3px;
            }
            QStatusBar {
                background: #e0e0e0;
                border-top: 1px solid #a0a0a0;
            }
            QPushButton {
                background: #0078d7;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #005a9e;
            }
            QPushButton:pressed {
                background: #004080;
            }
            QTableWidget {
                background: white;
                alternate-background-color: #f9f9f9;
                selection-background-color: #0078d7;
                gridline-color: #d0d0d0;
                border: 1px solid #a0a0a0;
            }
            QHeaderView::section {
                background: #e0e0e0;
                padding: 4px;
                border: 1px solid #a0a0a0;
                font-weight: bold;
            }
            QLineEdit, QComboBox, QDateEdit, QSpinBox, QDoubleSpinBox, QTextEdit {
                border: 1px solid #a0a0a0;
                border-radius: 3px;
                padding: 4px;
                background: white;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTextEdit:focus {
                border: 2px solid #0078d7;
            }
            QGroupBox {
                border: 2px solid #c0c0c0;
                border-radius: 5px;
                margin-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)