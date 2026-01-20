from app.models.inventory_model import InventoryModel
from app.models.transaksi_model import TransaksiModel
from app.controllers.inventory_controller import InventoryController
from app.controllers.transaksi_controller import TransaksiController
from app.controllers.dashboard_controller import DashboardController

class MainController:
    def __init__(self, main_window):
        self.main_window = main_window
        
        # Inisialisasi Model
        self.inventory_model = InventoryModel()
        self.transaksi_model = TransaksiModel()
        
        # Inisialisasi Controller Tab
        self.dashboard_controller = DashboardController(
            self.inventory_model,
            self.transaksi_model,
            self.main_window.dashboard_tab,
            self.main_window
        )
        self.inventory_controller = InventoryController(
            self.inventory_model, 
            self.main_window.inventory_tab
        )
        self.transaksi_controller = TransaksiController(
            self.transaksi_model, 
            self.inventory_model, 
            self.main_window.rental_tab
        )
        
        # Muat Awal
        self.dashboard_controller.refresh_data()
        self.inventory_controller.refresh_data()
        self.transaksi_controller.refresh_all()
        
        # Hubungkan sinyal perubahan tab
        self.main_window.tabs.currentChanged.connect(self.on_tab_changed)
        
        # Baru: Koneksi Pencarian Global
        self.main_window.search_input.textChanged.connect(self.on_global_search)

    def on_global_search(self, text):
        index = self.main_window.tabs.currentIndex()
        if index == 1: # Inventory
            self.main_window.inventory_tab.search_input.setText(text)
        elif index == 2: # Transactions
            self.main_window.rental_tab.search_trans.setText(text)

    def on_tab_changed(self, index):
        if index == 0: # Dashboard
            self.dashboard_controller.refresh_data()
        elif index == 1: # Inventory
            self.inventory_controller.refresh_data()
        elif index == 2: # Transactions
            self.transaksi_controller.refresh_all()
