"""THESIS: A calm operational desk, not a dashboard collage.
OWN-WORLD: Deep mineral green, kiln-orange actions, warm paper-white workspace.
STORY: One owner updates the source tables, runs local AI reports, and files PDFs.
FIRST VIEWPORT: Data sources lead the left rail; the editable table owns the workspace.
FORM: Dense, native desktop controls with visible state and no decorative metric cards.
"""

from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path
from typing import Callable

import pandas as pd
from PySide6.QtCore import QObject, QRunnable, Qt, QThreadPool, Signal, Slot
from PySide6.QtGui import QAction, QColor, QFont, QPalette
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from ui.pdf_export import export_department_pdf


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATASETS = {
    "Stok": "stock.csv",
    "Satin Alma": "purchase.csv",
    "Satin Alma Siteleri": "purchase_sites.csv",
    "Satis": "sales.csv",
    "Giderler": "expenses.csv",
    "Uretim": "production.csv",
    "Uretim Asamalari": "production_stages.csv",
    "Firin Kapasitesi": "kiln_capacity.csv",
    "AR-GE Projeleri": "research_and_development.csv",
    "AR-GE Arastirmalari": "research_trends.csv",
    "Satis Firsatlari": "sales_prospects.csv",
    "Yeniden Siparis Plani": "reorder_schedule.csv",
    "Sosyal Medya": "social_posts.csv",
    "Rakip Analizi": "marketing_competitor_analysis.csv",
    "Marka Tutarliligi": "brand_consistency_audits.csv",
    "E-ticaret Urunleri": "ecommerce_products.csv",
    "E-ticaret Hunisi": "ecommerce_funnel.csv",
    "E-ticaret Urun Performansi": "ecommerce_product_performance.csv",
}


class WorkerSignals(QObject):
    completed = Signal(object)
    failed = Signal(str)


class TaskWorker(QRunnable):
    def __init__(self, task: Callable[[], object]) -> None:
        super().__init__()
        self.task = task
        self.signals = WorkerSignals()

    @Slot()
    def run(self) -> None:
        try:
            self.signals.completed.emit(self.task())
        except Exception:
            self.signals.failed.emit(traceback.format_exc())


class DataEditor(QWidget):
    status_changed = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self.current_file = next(iter(DATASETS.values()))
        self._build()
        self.load_current_data()

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 28, 30, 30)
        title = QLabel("Veri Merkezi")
        title.setObjectName("pageTitle")
        description = QLabel(
            "CSV kaynaklarini tablo uzerinden duzenleyin veya Excel dosyasini ice aktarip "
            "ayni sutun yapisiyla kaydedin."
        )
        description.setObjectName("pageDescription")
        self.dataset_picker = QComboBox()
        self.dataset_picker.addItems(DATASETS.keys())
        self.dataset_picker.currentTextChanged.connect(self._dataset_changed)
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setCornerButtonEnabled(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        controls = QHBoxLayout()
        import_button = QPushButton("Excel Ice Aktar")
        import_button.clicked.connect(self.import_excel)
        export_button = QPushButton("Excel Disari Aktar")
        export_button.setProperty("secondary", True)
        export_button.clicked.connect(self.export_excel)
        add_row_button = QPushButton("Satir Ekle")
        add_row_button.setProperty("secondary", True)
        add_row_button.clicked.connect(self.add_row)
        save_button = QPushButton("Degisiklikleri Kaydet")
        save_button.setObjectName("primaryButton")
        save_button.clicked.connect(self.save_csv)
        controls.addWidget(import_button)
        controls.addWidget(export_button)
        controls.addWidget(add_row_button)
        controls.addStretch()
        controls.addWidget(save_button)
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(self.dataset_picker)
        layout.addSpacing(10)
        layout.addWidget(self.table, 1)
        layout.addLayout(controls)

    def _dataset_changed(self, label: str) -> None:
        self.current_file = DATASETS[label]
        self.load_current_data()

    def load_current_data(self) -> None:
        try:
            data = pd.read_csv(DATA_DIR / self.current_file, dtype=str).fillna("")
            self._show_dataframe(data)
            self.status_changed.emit(f"{self.current_file} yuklendi.")
        except Exception as error:
            self._show_error(f"Veri dosyasi yuklenemedi: {error}")

    def _show_dataframe(self, data: pd.DataFrame) -> None:
        self.table.clear()
        self.table.setColumnCount(len(data.columns))
        self.table.setHorizontalHeaderLabels(data.columns.tolist())
        self.table.setRowCount(len(data))
        for row_index, row in data.iterrows():
            for column_index, value in enumerate(row):
                self.table.setItem(row_index, column_index, QTableWidgetItem(str(value)))
        self.table.resizeColumnsToContents()

    def _to_dataframe(self) -> pd.DataFrame:
        headers = [
            self.table.horizontalHeaderItem(index).text()
            for index in range(self.table.columnCount())
        ]
        rows = []
        for row_index in range(self.table.rowCount()):
            rows.append(
                [
                    self.table.item(row_index, column_index).text()
                    if self.table.item(row_index, column_index)
                    else ""
                    for column_index in range(self.table.columnCount())
                ]
            )
        return pd.DataFrame(rows, columns=headers)

    def add_row(self) -> None:
        self.table.insertRow(self.table.rowCount())
        self.status_changed.emit("Bos satir eklendi.")

    def save_csv(self) -> None:
        try:
            self._to_dataframe().to_csv(DATA_DIR / self.current_file, index=False, encoding="utf-8")
            self.status_changed.emit(f"{self.current_file} kaydedildi.")
            QMessageBox.information(self, "Kaydedildi", "Degisiklikler CSV dosyasina kaydedildi.")
        except Exception as error:
            self._show_error(f"Kaydetme basarisiz: {error}")

    def import_excel(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self, "Excel Dosyasi Sec", str(PROJECT_ROOT), "Excel Dosyalari (*.xlsx *.xls)"
        )
        if not path:
            return
        try:
            source = pd.read_excel(path, dtype=str).fillna("")
            current_columns = [
                self.table.horizontalHeaderItem(index).text()
                for index in range(self.table.columnCount())
            ]
            if source.columns.tolist() != current_columns:
                raise ValueError(
                    "Excel sutunlari secili veri dosyasiyla ayni sirada olmali: "
                    + ", ".join(current_columns)
                )
            self._show_dataframe(source)
            self.status_changed.emit("Excel verisi tabloya aktarıldı; kalici olmasi icin kaydedin.")
        except Exception as error:
            self._show_error(f"Excel dosyasi aktarılamadı: {error}")

    def export_excel(self) -> None:
        default_path = str(PROJECT_ROOT / f"{Path(self.current_file).stem}.xlsx")
        path, _ = QFileDialog.getSaveFileName(
            self, "Excel Olarak Kaydet", default_path, "Excel Dosyalari (*.xlsx)"
        )
        if not path:
            return
        try:
            self._to_dataframe().to_excel(path, index=False)
            self.status_changed.emit(f"Excel dosyasi kaydedildi: {path}")
        except Exception as error:
            self._show_error(f"Excel dosyasi olusturulamadi: {error}")

    def _show_error(self, message: str) -> None:
        self.status_changed.emit(message)
        QMessageBox.critical(self, "Islem Tamamlanamadi", message)


class ReportPage(QWidget):
    status_changed = Signal(str)
    REPORTS: dict[str, Callable[[], dict]] = {}

    def __init__(self) -> None:
        super().__init__()
        self.current_report: dict | None = None
        self.thread_pool = QThreadPool.globalInstance()
        self._load_backend_reports()
        self._build()

    def _load_backend_reports(self) -> None:
        from src.departments import finance, marketing, production, purchase, sales, stock
        from src.departments.ecommerce import ecommerce_report
        from src.departments.research_and_development import research_and_development_report

        self.REPORTS = {
            "Finans ve Muhasebe": finance.monthly_report,
            "Satin Alma ve Tedarik": purchase.purchase_report,
            "Stok ve Depo Yonetimi": stock.stock_report,
            "Uretim ve Uretim Planlama": production.production_report,
            "AR-GE ve Urun Gelistirme": research_and_development_report,
            "Satis ve Is Gelistirme": sales.sales_report,
            "Pazarlama ve Marka Yonetimi": marketing.marketing_report,
            "E-ticaret ve Dijital Operasyonlar": ecommerce_report,
        }

    def _build(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 28, 30, 30)
        title = QLabel("Departman Raporlari")
        title.setObjectName("pageTitle")
        description = QLabel(
            "Her rapor yerel Ollama analiziyle hazirlanir ve tek basina PDF olarak dosyalanir."
        )
        description.setObjectName("pageDescription")
        self.department_picker = QComboBox()
        self.department_picker.addItems(self.REPORTS.keys())
        self.run_button = QPushButton("Raporu Olustur")
        self.run_button.setObjectName("primaryButton")
        self.run_button.clicked.connect(self.run_report)
        self.pdf_button = QPushButton("Bu Departmani PDF Olarak Kaydet")
        self.pdf_button.setEnabled(False)
        self.pdf_button.clicked.connect(self.export_current_pdf)
        actions = QHBoxLayout()
        actions.addWidget(self.department_picker, 1)
        actions.addWidget(self.run_button)
        actions.addWidget(self.pdf_button)
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("Bir departman secip rapor olusturun.")
        layout.addWidget(title)
        layout.addWidget(description)
        layout.addLayout(actions)
        layout.addSpacing(10)
        layout.addWidget(self.output, 1)

    def run_report(self) -> None:
        department = self.department_picker.currentText()
        self.run_button.setEnabled(False)
        self.pdf_button.setEnabled(False)
        self.output.setPlainText("Llama 3.2 ile analiz hazirlaniyor...")
        self.status_changed.emit(f"{department} raporu hazirlaniyor.")
        worker = TaskWorker(self.REPORTS[department])
        worker.signals.completed.connect(self._report_ready)
        worker.signals.failed.connect(self._report_failed)
        self.thread_pool.start(worker)

    def _report_ready(self, report: dict) -> None:
        self.current_report = report
        self.output.setPlainText(json.dumps(report, ensure_ascii=False, indent=2, default=str))
        self.run_button.setEnabled(True)
        self.pdf_button.setEnabled(True)
        self.status_changed.emit("Rapor hazir. PDF olarak kaydedebilirsiniz.")

    def _report_failed(self, details: str) -> None:
        self.run_button.setEnabled(True)
        self.output.setPlainText(details)
        self.status_changed.emit("Rapor olusturulamadi. Ayrintilar ekranda.")

    def export_current_pdf(self) -> None:
        if self.current_report is None:
            return
        department = self.department_picker.currentText()
        try:
            path = export_department_pdf(department, self.current_report)
            self.status_changed.emit(f"PDF olusturuldu: {path}")
            QMessageBox.information(self, "PDF Hazir", f"Departman raporu kaydedildi:\n{path}")
        except Exception as error:
            QMessageBox.critical(self, "PDF Olusturulamadi", str(error))


class ElaiaDesktopApp(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Elaia Ceramics | Operasyon Masasi")
        self.resize(1300, 820)
        self.setMinimumSize(1050, 680)
        self._build()
        self._apply_style()

    def _build(self) -> None:
        self.stack = QStackedWidget()
        self.data_editor = DataEditor()
        self.report_page = ReportPage()
        self.data_editor.status_changed.connect(self.statusBar().showMessage)
        self.report_page.status_changed.connect(self.statusBar().showMessage)
        self.stack.addWidget(self.data_editor)
        self.stack.addWidget(self.report_page)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        side_layout = QVBoxLayout(sidebar)
        side_layout.setContentsMargins(22, 28, 18, 22)
        brand = QLabel("ELAIA\nCERAMICS")
        brand.setObjectName("brand")
        side_layout.addWidget(brand)
        side_layout.addSpacing(46)
        data_button = QPushButton("Veri Merkezi")
        reports_button = QPushButton("Departman Raporlari")
        data_button.setObjectName("navButton")
        reports_button.setObjectName("navButton")
        data_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        reports_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        side_layout.addWidget(data_button)
        side_layout.addWidget(reports_button)
        side_layout.addStretch()
        service = QLabel("Yerel model\nllama3.2:3b")
        service.setObjectName("serviceStatus")
        side_layout.addWidget(service)

        splitter = QSplitter()
        splitter.setHandleWidth(1)
        splitter.addWidget(sidebar)
        splitter.addWidget(self.stack)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([240, 1060])
        self.setCentralWidget(splitter)
        self.statusBar().showMessage("Hazir")

        toolbar = QToolBar("Ana Islemler")
        toolbar.setMovable(False)
        export_action = QAction("Veri Merkezi", self)
        export_action.triggered.connect(lambda: self.stack.setCurrentIndex(0))
        report_action = QAction("Raporlar", self)
        report_action.triggered.connect(lambda: self.stack.setCurrentIndex(1))
        toolbar.addAction(export_action)
        toolbar.addAction(report_action)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

    def _apply_style(self) -> None:
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#F5F1E8"))
        palette.setColor(QPalette.Base, QColor("#FFFDF8"))
        palette.setColor(QPalette.Text, QColor("#173B37"))
        palette.setColor(QPalette.ButtonText, QColor("#173B37"))
        self.setPalette(palette)
        self.setStyleSheet(
            """
            * { font-family: "Avenir Next", "Segoe UI", sans-serif; font-size: 13px; }
            QMainWindow { background: #F5F1E8; }
            QToolBar { background: #F5F1E8; border: none; spacing: 8px; padding: 7px 18px; }
            QToolButton { color: #365A52; padding: 6px 10px; }
            #sidebar { background: #173B37; }
            #brand { color: #F8D3A0; font-size: 21px; font-weight: 700; letter-spacing: 3px; }
            #serviceStatus { color: #BFD0C6; font-size: 12px; line-height: 1.5; }
            #navButton { background: transparent; color: #E4ECE6; text-align: left; border: 0; padding: 11px 10px; }
            #navButton:hover { background: #285149; color: #FFFDF8; }
            #pageTitle { color: #173B37; font-size: 28px; font-weight: 700; padding-top: 3px; }
            #pageDescription { color: #526B64; font-size: 14px; padding-bottom: 14px; }
            QComboBox, QTextEdit, QTableWidget {
                background: #FFFDF8; border: 1px solid #C9D5CC; border-radius: 5px; color: #173B37; selection-background-color: #D6E7DF; selection-color: #173B37;
            }
            QComboBox { padding: 8px 10px; min-height: 21px; }
            QTextEdit { padding: 16px; line-height: 1.5; }
            QTableWidget { gridline-color: #D7E0DA; selection-background-color: #D6E7DF; }
            QHeaderView::section { background: #E7EEE9; color: #173B37; border: 0; padding: 9px; font-weight: 700; }
            QPushButton { background: #E7EEE9; color: #173B37; border: 1px solid #B8CBC1; border-radius: 5px; padding: 9px 13px; font-weight: 600; }
            QPushButton:hover { background: #D9E6DE; }
            QPushButton:disabled { color: #879790; background: #EFF2EE; border-color: #DCE4DE; }
            #primaryButton { background: #B55A34; color: #FFFFFF; border: 1px solid #B55A34; }
            #primaryButton:hover { background: #984624; border-color: #984624; }
            QStatusBar { background: #E7EEE9; color: #365A52; }
            """
        )


def main() -> int:
    application = QApplication(sys.argv)
    application.setApplicationName("Elaia Ceramics")
    application.setFont(QFont("Avenir Next", 10))
    window = ElaiaDesktopApp()
    window.show()
    return application.exec()


if __name__ == "__main__":
    raise SystemExit(main())
