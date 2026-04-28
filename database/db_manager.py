import sqlite3
import os
from models.transaction import Transaction, transaction_from_tuple

class DatabaseManager:

    def __init__(self, db_name="keuangan.db"):
        #Simpan path database di folder root project
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), db_name)
        self.db_path = db_path
        self._create_table()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        conn = self._get_connection()
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS transaksi (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tanggal TEXT NOT NULL,
                    jenis TEXT NOT NULL,
                    kategori TEXT NOT NULL,
                    jumlah REAL NOT NULL,
                    metode_pembayaran TEXT NOT NULL,
                    deskripsi TEXT DEFAULT ''
                )
            """)
            conn.commit()
        finally:
            conn.close()

    def insert_transaction(self, trx):
        #Menambahkan transaksi baru ke database
        conn = self._get_connection()
        try:
            conn.execute(
                """INSERT INTO transaksi
                   (tanggal, jenis, kategori, jumlah, metode_pembayaran, deskripsi)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (trx.tanggal, trx.jenis, trx.kategori, trx.jumlah,
                 trx.metode_pembayaran, trx.deskripsi),
            )
            conn.commit()
        finally:
            conn.close()

    def get_all_transactions(self):
        conn = self._get_connection()
        try:
            cursor = conn.execute(
                "SELECT id, tanggal, jenis, kategori, jumlah, metode_pembayaran, deskripsi "
                "FROM transaksi ORDER BY tanggal DESC, id DESC"
            )
            rows = cursor.fetchall()
            return [transaction_from_tuple(row) for row in rows]
        finally:
            conn.close()

    def get_transaction_by_id(self, trx_id):
        conn = self._get_connection()
        try:
            cursor = conn.execute(
                "SELECT id, tanggal, jenis, kategori, jumlah, metode_pembayaran, deskripsi "
                "FROM transaksi WHERE id = ?",
                (trx_id,),
            )
            row = cursor.fetchone()
            if row:
                return transaction_from_tuple(row)
            return None
        finally:
            conn.close()

    def update_transaction(self, trx):
        conn = self._get_connection()
        try:
            conn.execute(
                """UPDATE transaksi
                   SET tanggal=?, jenis=?, kategori=?, jumlah=?,
                       metode_pembayaran=?, deskripsi=?
                   WHERE id=?""",
                (trx.tanggal, trx.jenis, trx.kategori, trx.jumlah,
                 trx.metode_pembayaran, trx.deskripsi, trx.id),
            )
            conn.commit()
        finally:
            conn.close()

    def delete_transaction(self, trx_id):
        conn = self._get_connection()
        try:
            conn.execute("DELETE FROM transaksi WHERE id = ?", (trx_id,))
            conn.commit()
        finally:
            conn.close()

    def get_summary(self):
        conn = self._get_connection()
        try:
            cursor = conn.execute(
                "SELECT jenis, SUM(jumlah) FROM transaksi GROUP BY jenis"
            )
            result = {"total_pemasukan": 0.0, "total_pengeluaran": 0.0, "saldo": 0.0}
            for row in cursor.fetchall():
                if row[0] == "Pemasukan":
                    result["total_pemasukan"] = row[1] or 0.0
                elif row[0] == "Pengeluaran":
                    result["total_pengeluaran"] = row[1] or 0.0
            result["saldo"] = result["total_pemasukan"] - result["total_pengeluaran"]
            return result
        finally:
            conn.close()