import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb 
from ttkbootstrap.constants import *
import random

def generate_data():
    nama_depan = ["Rizky", "Siti", "Ahmad", "Dewi", "Bagus", "Putri", "Fajar", "Indah", "Yuda", "Maya"]
    nama_belakang = ["Pratama", "Wijaya", "Santoso", "Hidayat", "Kurniawan", "Sari", "Ramadhan", "Putra", "Utama", "Wibowo"]
    data = []
    for i in range(1, 101):
        data.append({
            "id": i, 
            "nama": f"{random.choice(nama_depan)} {random.choice(nama_belakang)}", 
            "berat": random.randint(1, 20), 
            "status": random.choice(["Proses", "Selesai", "Diambil"])
        })
    return data

def quick_sort(arr, key):
    if len(arr) <= 1: return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x[key] < pivot[key]]
    middle = [x for x in arr if x[key] == pivot[key]]
    right = [x for x in arr if x[key] > pivot[key]]
    return quick_sort(left, key) + middle + quick_sort(right, key)

class UltimateLaundryApp(tb.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.title("Sistem Laundry Pro - Ultimate Edition")
        self.geometry("950x750")
        self.data = generate_data()
        self.next_id = 101
        self.edit_id = None

        self.stats_lbl = tb.Label(self, text="", font=("Helvetica", 14, "bold"))
        self.stats_lbl.pack(pady=10)

        input_frame = ttk.LabelFrame(self, text="Manajemen Pelanggan")
        input_frame.pack(fill=X, padx=20, pady=5)
        
        ttk.Label(input_frame, text="Nama:").pack(side=LEFT, padx=5)
        self.entry_nama = ttk.Entry(input_frame, width=20)
        self.entry_nama.pack(side=LEFT, padx=5)
        
        ttk.Label(input_frame, text="Berat (kg):").pack(side=LEFT, padx=5)
        self.spin_berat = ttk.Spinbox(input_frame, from_=1, to=50, width=5)
        self.spin_berat.set(1)
        self.spin_berat.pack(side=LEFT, padx=5)
        
        ttk.Label(input_frame, text="Status:").pack(side=LEFT, padx=5)
        self.combo_status = ttk.Combobox(input_frame, values=["Proses", "Selesai", "Diambil"], width=10, state="readonly")
        self.combo_status.set("Proses")
        self.combo_status.pack(side=LEFT, padx=5)
        
        tb.Button(input_frame, text="Simpan Baru", command=self.tambah_data, bootstyle="primary").pack(side=LEFT, padx=5)
        tb.Button(input_frame, text="Simpan Edit", command=self.simpan_edit, bootstyle="warning").pack(side=LEFT, padx=5)

        ctrl_frame = ttk.Frame(self)
        ctrl_frame.pack(fill=X, padx=20, pady=5)
        
        self.entry_search = ttk.Entry(ctrl_frame, width=25)
        self.entry_search.pack(side=LEFT, padx=5)
        self.entry_search.bind("<KeyRelease>", self.filter_and_search)
        
        self.combo_filter_status = ttk.Combobox(ctrl_frame, values=["Semua", "Proses", "Selesai", "Diambil"], width=10, state="readonly")
        self.combo_filter_status.set("Semua")
        self.combo_filter_status.pack(side=LEFT, padx=5)
        self.combo_filter_status.bind("<<ComboboxSelected>>", self.filter_and_search)
        
        tb.Button(ctrl_frame, text="Sortir Berat", command=self.sort_by_berat, bootstyle="success").pack(side=LEFT, padx=5)
        tb.Button(ctrl_frame, text="Edit", command=self.edit_data, bootstyle="info").pack(side=LEFT, padx=5)
        tb.Button(ctrl_frame, text="Delete", command=self.delete_data, bootstyle="danger").pack(side=LEFT, padx=5)

        self.tree = ttk.Treeview(self, columns=("ID", "Nama", "Berat", "Status"), show="headings")
        for col in ("ID", "Nama", "Berat", "Status"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill=BOTH, expand=YES, padx=20, pady=20)
        
        self.refresh_table(self.data)

    def refresh_table(self, data):
        for i in self.tree.get_children(): self.tree.delete(i)
        for item in data:
            self.tree.insert("", END, values=(item["id"], item["nama"], item["berat"], item["status"]))
        
        total_berat = sum(x['berat'] for x in data)
        layanan_aktif = len([x for x in data if x['status']=='Proses'])
        self.stats_lbl.config(text=f"Total Berat: {total_berat} kg | Layanan Aktif: {layanan_aktif}")

    def tambah_data(self):
        nama = self.entry_nama.get().strip()
        if nama:
            self.data.append({"id": self.next_id, "nama": nama, "berat": int(self.spin_berat.get()), "status": self.combo_status.get()})
            self.next_id += 1
            self.filter_and_search(None)
            messagebox.showinfo("Sukses", "Data berhasil disimpan!")
        else:
             messagebox.showwarning("Peringatan", "Nama pelanggan tidak boleh kosong!")

    def edit_data(self):
        selected = self.tree.selection()
        if not selected: return
        values = self.tree.item(selected, 'values')
        self.edit_id = int(values[0])
        self.entry_nama.delete(0, END); self.entry_nama.insert(0, values[1])
        self.spin_berat.set(values[2]); self.combo_status.set(values[3])

    def simpan_edit(self):
        if self.edit_id is None: return
        for item in self.data:
            if item['id'] == self.edit_id:
                item.update({"nama": self.entry_nama.get(), "berat": int(self.spin_berat.get()), "status": self.combo_status.get()})
                break
        self.edit_id = None
        self.filter_and_search(None)
        messagebox.showinfo("Sukses", "Data berhasil diupdate!")

    def delete_data(self):
        selected = self.tree.selection()
        if not selected: return
        values = self.tree.item(selected, 'values')
        self.data = [x for x in self.data if x['id'] != int(values[0])]
        self.filter_and_search(None)

    def sort_by_berat(self):
        self.data = quick_sort(self.data, "berat")
        self.filter_and_search(None)

    def filter_and_search(self, event):
        k = self.entry_search.get().lower()
        s = self.combo_filter_status.get()
        filtered = [x for x in self.data if k in x["nama"].lower()]
        if s != "Semua":
            filtered = [x for x in filtered if x["status"] == s]
        self.refresh_table(filtered)

if __name__ == "__main__":
    app = UltimateLaundryApp()
    app.mainloop()