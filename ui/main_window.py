from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTableWidget, QTableWidgetItem, QPushButton,
    QHeaderView, QMessageBox, QFrame, QAbstractItemView,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QColor
from logic.controller import TransactionController
from ui.dialogs import TransactionDialog

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.setWindowTitle("DompetKu — Pencatat Keuangan Pribadi")
        self.setMinimumSize(850, 550)
        self.resize(950, 620)

        self._setup_menu_bar()
        self._setup_ui()
        self._connect_signals()
        self._refresh_data()

    def _setup_menu_bar(self):
        menu_bar = self.menuBar()

        #Menu file
        file_menu = menu_bar.addMenu("&File")
        action_add = QAction("Tambah Transaksi", self)
        action_add.setShortcut("Ctrl+N")
        action_add.triggered.connect(self._on_add)
        file_menu.addAction(action_add)

        file_menu.addSeparator()

        action_exit = QAction("Keluar", self)
        action_exit.setShortcut("Ctrl+Q")
        action_exit.triggered.connect(self.close)
        file_menu.addAction(action_exit)

        #Menu bantuan
        help_menu = menu_bar.addMenu("&Bantuan")

        action_about = QAction("Tentang Aplikasi", self)
        action_about.setShortcut("F1")
        action_about.triggered.connect(self._on_show_about)
        help_menu.addAction(action_about)

    def _on_show_about(self):
        QMessageBox.about(
            self,
            "Tentang DompetKu",
            "<h2>DompetKu</h2>"
            "<p>Versi 1.0.0</p>"
            "<p>Aplikasi pencatat keuangan pribadi.<br>"
            "Membantu untuk melacak pemasukan dan pengeluaran uang Anda.</p>"
            "<hr>"
            "<p><b>Muharromi Ali Ilham</b><br>"
            "NIM: F1D02410082</p>"
        )

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 12, 16, 12)

        layout.addLayout(self._create_header()) #Header (title, nama dan nim)
        layout.addLayout(self._create_summary_cards()) #Pemasukan, pengeluaran, saldo
        layout.addLayout(self._create_buttons()) #Tambah, edit, hapus
        layout.addWidget(self._create_table(), stretch=1) #Tabel transaksi

    def _create_header(self):
        header = QHBoxLayout()

        #Title
        title_col = QVBoxLayout()
        title_col.setSpacing(0)

        app_title = QLabel("DompetKu")
        app_title.setObjectName("appTitle")
        title_col.addWidget(app_title)

        app_subtitle = QLabel("Pencatat Keuangan Pribadi")
        app_subtitle.setObjectName("appSubtitle")
        title_col.addWidget(app_subtitle)

        header.addLayout(title_col)
        header.addStretch()

        #Nama dan NIM
        info_col = QVBoxLayout()
        info_col.setSpacing(0)

        nama = QLabel("Muharromi Ali Ilham")
        nama.setObjectName("studentName")
        nama.setAlignment(Qt.AlignmentFlag.AlignRight)
        info_col.addWidget(nama)

        nim = QLabel("NIM: F1D02410082")
        nim.setObjectName("studentNim")
        nim.setAlignment(Qt.AlignmentFlag.AlignRight)
        info_col.addWidget(nim)

        header.addLayout(info_col)
        return header

    def _create_summary_cards(self):
        cards = QHBoxLayout()
        cards.setSpacing(10)

        # Buat kartu dan simpan label nilainya ke variabel
        self.card_pemasukan, self.lbl_pemasukan = self._make_card("Total Pemasukan", "Rp 0", "cardPemasukan")
        self.card_pengeluaran, self.lbl_pengeluaran = self._make_card("Total Pengeluaran", "Rp 0", "cardPengeluaran")
        self.card_saldo, self.lbl_saldo = self._make_card("Saldo", "Rp 0", "cardSaldo")

        cards.addWidget(self.card_pemasukan)
        cards.addWidget(self.card_pengeluaran)
        cards.addWidget(self.card_saldo)
        return cards

    def _make_card(self, title, value, obj_name):
        card = QFrame()
        card.setObjectName(obj_name)
        card.setProperty("class", "summaryCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(2)

        lbl_title = QLabel(title)
        lbl_title.setProperty("class", "cardTitle")
        layout.addWidget(lbl_title)

        lbl_value = QLabel(value)
        lbl_value.setProperty("class", "cardValue")
        layout.addWidget(lbl_value)

        return card, lbl_value  #Return card dan label nilainya

    def _create_buttons(self):
        """Membuat tombol Tambah, Edit, dan Hapus."""
        toolbar = QHBoxLayout()
        toolbar.setSpacing(8)
        toolbar.addStretch()

        #Tombol tambah
        self.btn_add = QPushButton("Tambah")
        self.btn_add.setObjectName("btnAdd")
        toolbar.addWidget(self.btn_add)

        #Tombol edit
        self.btn_edit = QPushButton("Edit")
        self.btn_edit.setObjectName("btnEdit")
        self.btn_edit.setEnabled(False)
        toolbar.addWidget(self.btn_edit)

        #Tombol hapus
        self.btn_delete = QPushButton("Hapus")
        self.btn_delete.setObjectName("btnDelete")
        self.btn_delete.setEnabled(False)
        toolbar.addWidget(self.btn_delete)
        return toolbar

    def _create_table(self):
        #Buat tabel untuk menampilkan data transaksi
        self.table = QTableWidget()

        #Header kolom
        headers = ["ID", "Tanggal", "Jenis", "Kategori", "Jumlah", "Metode Bayar", "Deskripsi"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        #Pengaturan tabel
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSortingEnabled(True)

        #Mengatur lebar kolom
        header = self.table.horizontalHeader()
        for col in range(6):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Stretch)

        #Menyembunyikan id kolom supaya terlihat rapi
        self.table.setColumnHidden(0, True)
        return self.table

    def _connect_signals(self):
        self.btn_add.clicked.connect(self._on_add)
        self.btn_edit.clicked.connect(self._on_edit)
        self.btn_delete.clicked.connect(self._on_delete)

        self.table.selectionModel().selectionChanged.connect(self._on_selection_changed)
        self.table.doubleClicked.connect(self._on_edit)

    def _on_selection_changed(self):
        #Mengaktifkan tombol edit dan hapus jika ada baris yg dipilih
        ada_yang_dipilih = len(self.table.selectedItems()) > 0
        self.btn_edit.setEnabled(ada_yang_dipilih)
        self.btn_delete.setEnabled(ada_yang_dipilih)

    def _on_add(self):
        dialog = TransactionDialog(self)
        if dialog.exec() == TransactionDialog.DialogCode.Accepted:
            trx = dialog.get_transaction_data()
            error = self.controller.add_transaction(trx)
            if error:
                QMessageBox.warning(self, "Error", error)
            else:
                self._refresh_data()

    def _on_edit(self):
        trx_id = self._get_selected_id()
        if trx_id is None:
            return

        trx = self.controller.get_transaction_by_id(trx_id)
        if trx is None:
            QMessageBox.warning(self, "Error", "Transaksi tidak ditemukan.")
            return

        dialog = TransactionDialog(self, transaction=trx)
        if dialog.exec() == TransactionDialog.DialogCode.Accepted:
            updated = dialog.get_transaction_data()
            error = self.controller.update_transaction(updated)
            if error:
                QMessageBox.warning(self, "Error", error)
            else:
                self._refresh_data()

    def _on_delete(self):
        trx_id = self._get_selected_id()
        if trx_id is None:
            return
        reply = QMessageBox.question(
            self, "Konfirmasi Hapus",
            "Apakah Anda yakin ingin menghapus transaksi ini?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.controller.delete_transaction(trx_id)
            self._refresh_data()

    def _refresh_data(self):
        transactions = self.controller.get_all_transactions()
        self._populate_table(transactions)
        self._update_summary()

    def _populate_table(self, transactions):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(transactions))

        for row, trx in enumerate(transactions):
            #Kolom 0 untuk id
            id_item = QTableWidgetItem()
            id_item.setData(Qt.ItemDataRole.DisplayRole, trx.id)
            self.table.setItem(row, 0, id_item)

            #Kolom 1 untuk tanggal
            self.table.setItem(row, 1, QTableWidgetItem(trx.tanggal))

            #Kolom 2 jenis transaksi
            jenis_item = QTableWidgetItem(trx.jenis)
            if trx.jenis == "Pemasukan":
                jenis_item.setForeground(QColor("#27ae60"))
            else:
                jenis_item.setForeground(QColor("#e74c3c"))
            self.table.setItem(row, 2, jenis_item)

            #Kolom 3 kategori
            self.table.setItem(row, 3, QTableWidgetItem(trx.kategori))

            #Kolom 4 jumlah
            jumlah_item = QTableWidgetItem(trx.jumlah_formatted())
            jumlah_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
            if trx.jenis == "Pemasukan":
                jumlah_item.setForeground(QColor("#27ae60"))
            else:
                jumlah_item.setForeground(QColor("#e74c3c"))
            self.table.setItem(row, 4, jumlah_item)

            #Kolom 5 metode embayaran
            self.table.setItem(row, 5, QTableWidgetItem(trx.metode_pembayaran))

            #Kolom 6 deskripsi
            self.table.setItem(row, 6, QTableWidgetItem(trx.deskripsi))

        self.table.setSortingEnabled(True)

    def _update_summary(self):
        summary = self.controller.get_summary()
        pemasukan = summary["total_pemasukan"]
        pengeluaran = summary["total_pengeluaran"]
        saldo = summary["saldo"]

        #Mengubah format angka ke rupiah
        def format_rp(angka):
            return f"Rp {abs(angka):,.0f}".replace(",", ".")

        self.lbl_pemasukan.setText(format_rp(pemasukan))
        self.lbl_pengeluaran.setText(format_rp(pengeluaran))

        saldo_text = format_rp(saldo)
        if saldo < 0:
            saldo_text = f"- {saldo_text}"
        self.lbl_saldo.setText(saldo_text)

    def _get_selected_id(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.information(
                self, "Informasi", "Pilih transaksi terlebih dahulu."
            )
            return None
        row = selected_rows[0].row()
        id_item = self.table.item(row, 0)
        if id_item:
            return int(id_item.data(Qt.ItemDataRole.DisplayRole))
        return None