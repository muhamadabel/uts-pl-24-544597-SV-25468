<template>
  <div class="dashboard-wrapper">
    <!-- Navbar Atas -->
    <header class="top-nav">
      <div class="nav-brand">
        <span class="brand-tag">KATALOG TOKO</span>
        <span class="nav-title">Sistem Inventaris Produk</span>
      </div>
      <div class="nav-user">
        <span class="user-greeting">Petugas: <strong>{{ userName }}</strong></span>
        <button @click="handleLogout" class="btn btn-sm btn-outline">Keluar</button>
      </div>
    </header>

    <!-- Konten Utama -->
    <main class="dashboard-content">
      <!-- Kartu Ringkasan Metrik -->
      <section class="metrics-grid">
        <div class="metric-card">
          <span class="metric-label">Total Produk</span>
          <span class="metric-value">{{ products.length }}</span>
        </div>
        <div class="metric-card">
          <span class="metric-label">Total Unit Stok</span>
          <span class="metric-value">{{ totalStock }}</span>
        </div>
        <div class="metric-card">
          <span class="metric-label">Kategori Aktif</span>
          <span class="metric-value">{{ activeCategoriesCount }}</span>
        </div>
        <div class="metric-card">
          <span class="metric-label">Total Nilai Inventaris</span>
          <span class="metric-value">{{ formatCurrency(totalInventoryValue) }}</span>
        </div>
      </section>

      <!-- Bar Kontrol & Aksi -->
      <section class="action-bar">
        <div class="search-filter-group">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Cari nama produk atau SKU..."
            class="input-search"
          />
          <select v-model="selectedCategory" class="select-category">
            <option value="">Semua Kategori</option>
            <option v-for="cat in availableCategories" :key="cat" :value="cat">
              {{ cat }}
            </option>
          </select>
        </div>
        <button @click="openCreateModal" class="btn btn-primary">
          + Tambah Produk
        </button>
      </section>

      <!-- Notifikasi Pesan -->
      <div v-if="toastMessage" :class="['toast-banner', toastType === 'error' ? 'toast-error' : 'toast-success']">
        {{ toastMessage }}
      </div>

      <!-- Tabel Daftar Produk -->
      <section class="card table-card">
        <div class="table-header">
          <h3>Daftar Produk Toko</h3>
          <span class="record-count">Menampilkan {{ filteredProducts.length }} dari {{ products.length }} produk</span>
        </div>

        <div v-if="loading" class="state-message">
          Memuat data produk...
        </div>

        <div v-else-if="filteredProducts.length === 0" class="state-message">
          Tidak ada produk yang cocok dengan pencarian atau filter.
        </div>

        <div v-else class="table-responsive">
          <table class="data-table">
            <thead>
              <tr>
                <th>SKU</th>
                <th>Nama Produk</th>
                <th>Kategori</th>
                <th class="text-right">Harga Satuan</th>
                <th class="text-center">Stok</th>
                <th class="text-center">Status</th>
                <th class="text-center">Aksi</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in filteredProducts" :key="item.id">
                <td class="sku-cell">{{ item.sku }}</td>
                <td class="name-cell">
                  <div class="product-name">{{ item.name }}</div>
                  <div v-if="item.description" class="product-desc">{{ item.description }}</div>
                </td>
                <td><span class="category-pill">{{ item.category }}</span></td>
                <td class="text-right font-mono">{{ formatCurrency(item.price) }}</td>
                <td class="text-center font-mono">{{ item.stock }}</td>
                <td class="text-center">
                  <span :class="['badge-status', getStatusClass(item.status)]">
                    {{ getStatusLabel(item.status) }}
                  </span>
                </td>
                <td class="text-center">
                  <div class="action-buttons">
                    <button @click="openEditModal(item)" class="btn btn-xs btn-outline">Ubah</button>
                    <button @click="confirmDelete(item)" class="btn btn-xs btn-danger">Hapus</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>

    <!-- Modal Form Tambah / Ubah Produk -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-dialog">
        <div class="modal-header">
          <h4>{{ isEditing ? 'Ubah Data Produk' : 'Tambah Produk Baru' }}</h4>
          <button @click="closeModal" class="btn-close">&times;</button>
        </div>

        <form @submit.prevent="saveProduct" class="modal-form">
          <div v-if="formError" class="alert alert-error">
            {{ formError }}
          </div>

          <div class="form-grid">
            <div class="form-group full-width">
              <label>Nama Produk <span class="required">*</span></label>
              <input
                v-model="form.name"
                type="text"
                placeholder="Contoh: Kemeja Oxford Katun"
                required
              />
              <span v-if="fieldErrors.name" class="field-error">{{ fieldErrors.name[0] }}</span>
            </div>

            <div class="form-group">
              <label>Kode SKU <span class="required">*</span></label>
              <input
                v-model="form.sku"
                type="text"
                placeholder="Contoh: PRD-OXF-001"
                required
              />
              <span v-if="fieldErrors.sku" class="field-error">{{ fieldErrors.sku[0] }}</span>
            </div>

            <div class="form-group">
              <label>Kategori <span class="required">*</span></label>
              <select v-model="form.category" required>
                <option value="" disabled>Pilih Kategori</option>
                <option value="Pakaian">Pakaian</option>
                <option value="Alas Kaki">Alas Kaki</option>
                <option value="Aksesoris">Aksesoris</option>
                <option value="Elektronik">Elektronik</option>
                <option value="Perlengkapan">Perlengkapan</option>
              </select>
              <span v-if="fieldErrors.category" class="field-error">{{ fieldErrors.category[0] }}</span>
            </div>

            <div class="form-group">
              <label>Harga Satuan (Rp) <span class="required">*</span></label>
              <input
                v-model.number="form.price"
                type="number"
                min="0"
                step="500"
                placeholder="Contoh: 175000"
                required
              />
              <span v-if="fieldErrors.price" class="field-error">{{ fieldErrors.price[0] }}</span>
            </div>

            <div class="form-group">
              <label>Jumlah Stok <span class="required">*</span></label>
              <input
                v-model.number="form.stock"
                type="number"
                min="0"
                step="1"
                placeholder="Contoh: 25"
                required
              />
              <span v-if="fieldErrors.stock" class="field-error">{{ fieldErrors.stock[0] }}</span>
            </div>

            <div class="form-group full-width">
              <label>Status Ketersediaan <span class="required">*</span></label>
              <select v-model="form.status" required>
                <option value="available">Tersedia</option>
                <option value="low_stock">Stok Menipis</option>
                <option value="out_of_stock">Habis</option>
                <option value="discontinued">Nonaktif</option>
              </select>
              <span v-if="fieldErrors.status" class="field-error">{{ fieldErrors.status[0] }}</span>
            </div>

            <div class="form-group full-width">
              <label>Deskripsi Tambahan</label>
              <textarea
                v-model="form.description"
                rows="3"
                placeholder="Deskripsi spesifikasi produk (opsional)..."
              ></textarea>
              <span v-if="fieldErrors.description" class="field-error">{{ fieldErrors.description[0] }}</span>
            </div>
          </div>

          <div class="modal-footer">
            <button type="button" @click="closeModal" class="btn btn-outline" :disabled="submitting">
              Batal
            </button>
            <button type="submit" class="btn btn-primary" :disabled="submitting">
              {{ submitting ? 'Menyimpan...' : (isEditing ? 'Simpan Perubahan' : 'Tambah Produk') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal Konfirmasi Hapus -->
    <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
      <div class="modal-dialog modal-sm">
        <div class="modal-header">
          <h4>Konfirmasi Hapus</h4>
          <button @click="showDeleteModal = false" class="btn-close">&times;</button>
        </div>
        <div class="modal-body">
          <p>Apakah Anda yakin ingin menghapus produk <strong>{{ productToDelete?.name }}</strong> (SKU: {{ productToDelete?.sku }})?</p>
          <p class="modal-subtext">Tindakan ini akan menghapus data dari basis data.</p>
        </div>
        <div class="modal-footer">
          <button @click="showDeleteModal = false" class="btn btn-outline" :disabled="deleting">
            Batal
          </button>
          <button @click="executeDelete" class="btn btn-danger" :disabled="deleting">
            {{ deleting ? 'Menghapus...' : 'Hapus Produk' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '../api/axios';

const router = useRouter();
const userName = ref(localStorage.getItem('user_name') || 'Petugas Toko');

const products = ref([]);
const loading = ref(false);
const submitting = ref(false);
const deleting = ref(false);

const searchQuery = ref('');
const selectedCategory = ref('');
const toastMessage = ref('');
const toastType = ref('success');

const showModal = ref(false);
const isEditing = ref(false);
const editingId = ref(null);
const formError = ref('');
const fieldErrors = ref({});

const showDeleteModal = ref(false);
const productToDelete = ref(null);

const form = ref({
  name: '',
  sku: '',
  category: '',
  price: 0,
  stock: 0,
  status: 'available',
  description: '',
});

const availableCategories = ['Pakaian', 'Alas Kaki', 'Aksesoris', 'Elektronik', 'Perlengkapan'];

const showToast = (message, type = 'success') => {
  toastMessage.value = message;
  toastType.value = type;
  setTimeout(() => {
    toastMessage.value = '';
  }, 4000);
};

// Pengambilan data produk melalui Axios (Soal 2b)
const fetchProducts = async () => {
  loading.value = true;
  try {
    const res = await apiClient.get('/products');
    if (res.data && res.data.data) {
      products.value = res.data.data;
    }
  } catch (err) {
    showToast('Gagal memuat data produk dari server.', 'error');
  } finally {
    loading.value = false;
  }
};

const filteredProducts = computed(() => {
  return products.value.filter((p) => {
    const matchesSearch =
      searchQuery.value === '' ||
      p.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      p.sku.toLowerCase().includes(searchQuery.value.toLowerCase());

    const matchesCategory =
      selectedCategory.value === '' || p.category === selectedCategory.value;

    return matchesSearch && matchesCategory;
  });
});

const totalStock = computed(() => {
  return products.value.reduce((sum, item) => sum + Number(item.stock || 0), 0);
});

const activeCategoriesCount = computed(() => {
  const cats = new Set(products.value.map((p) => p.category));
  return cats.size;
});

const totalInventoryValue = computed(() => {
  return products.value.reduce((sum, item) => {
    return sum + Number(item.price || 0) * Number(item.stock || 0);
  }, 0);
});

const formatCurrency = (val) => {
  const num = Number(val || 0);
  return 'Rp ' + num.toLocaleString('id-ID');
};

const getStatusLabel = (status) => {
  switch (status) {
    case 'available':
      return 'Tersedia';
    case 'low_stock':
      return 'Stok Menipis';
    case 'out_of_stock':
      return 'Habis';
    case 'discontinued':
      return 'Nonaktif';
    default:
      return status;
  }
};

const getStatusClass = (status) => {
  switch (status) {
    case 'available':
      return 'status-available';
    case 'low_stock':
      return 'status-warning';
    case 'out_of_stock':
      return 'status-danger';
    case 'discontinued':
      return 'status-muted';
    default:
      return '';
  }
};

const openCreateModal = () => {
  isEditing.value = false;
  editingId.value = null;
  formError.value = '';
  fieldErrors.value = {};
  form.value = {
    name: '',
    sku: '',
    category: '',
    price: 0,
    stock: 0,
    status: 'available',
    description: '',
  };
  showModal.value = true;
};

const openEditModal = (item) => {
  isEditing.value = true;
  editingId.value = item.id;
  formError.value = '';
  fieldErrors.value = {};
  form.value = {
    name: item.name,
    sku: item.sku,
    category: item.category,
    price: Number(item.price),
    stock: Number(item.stock),
    status: item.status,
    description: item.description || '',
  };
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  formError.value = '';
  fieldErrors.value = {};
};

// Menyimpan data produk baru (POST) atau memperbarui (PUT) via Axios (Soal 2b)
const saveProduct = async () => {
  submitting.value = true;
  formError.value = '';
  fieldErrors.value = {};

  try {
    if (isEditing.value) {
      await apiClient.put(`/products/${editingId.value}`, form.value);
      showToast('Data produk berhasil diperbarui.');
    } else {
      await apiClient.post('/products', form.value);
      showToast('Produk baru berhasil ditambahkan.');
    }
    closeModal();
    fetchProducts();
  } catch (err) {
    if (err.response && err.response.status === 422) {
      formError.value = 'Validasi gagal: Harap periksa kembali input formulir.';
      fieldErrors.value = err.response.data.errors || {};
    } else if (err.response && err.response.data && err.response.data.message) {
      formError.value = err.response.data.message;
    } else {
      formError.value = 'Terjadi kesalahan saat menyimpan produk.';
    }
  } finally {
    submitting.value = false;
  }
};

const confirmDelete = (item) => {
  productToDelete.value = item;
  showDeleteModal.value = true;
};

// Menghapus data produk (DELETE) via Axios (Soal 2b)
const executeDelete = async () => {
  if (!productToDelete.value) return;
  deleting.value = true;
  try {
    await apiClient.delete(`/products/${productToDelete.value.id}`);
    showToast(`Produk ${productToDelete.value.name} berhasil dihapus.`);
    showDeleteModal.value = false;
    productToDelete.value = null;
    fetchProducts();
  } catch (err) {
    showToast('Gagal menghapus produk.', 'error');
  } finally {
    deleting.value = false;
  }
};

const handleLogout = async () => {
  try {
    await apiClient.post('/logout');
  } catch (err) {
    // Abaikan jika token telah kedaluwarsa di server
  } finally {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_name');
    router.push('/login');
  }
};

onMounted(() => {
  fetchProducts();
});
</script>

<style scoped>
.dashboard-wrapper {
  min-height: 100vh;
  background: #f8fafc;
  color: #0f172a;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.brand-tag {
  background: #0f172a;
  color: #ffffff;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 0.25rem 0.55rem;
  border-radius: 4px;
}

.nav-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #0f172a;
}

.nav-user {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-greeting {
  font-size: 0.88rem;
  color: #475569;
}

.dashboard-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}

.metric-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1.25rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.metric-label {
  font-size: 0.82rem;
  color: #64748b;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.metric-value {
  font-size: 1.55rem;
  font-weight: 700;
  color: #0f172a;
}

.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.search-filter-group {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
  max-width: 600px;
}

.input-search {
  flex: 1;
  padding: 0.65rem 0.9rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.9rem;
  background: #ffffff;
  outline: none;
}

.input-search:focus {
  border-color: #0f172a;
}

.select-category {
  padding: 0.65rem 0.9rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.9rem;
  background: #ffffff;
  outline: none;
}

.card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.table-header h3 {
  font-size: 1.1rem;
  font-weight: 700;
  margin: 0;
  color: #0f172a;
}

.record-count {
  font-size: 0.82rem;
  color: #64748b;
}

.table-responsive {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.data-table th {
  background: #f8fafc;
  padding: 0.85rem 1.25rem;
  text-align: left;
  font-weight: 600;
  color: #475569;
  border-bottom: 1px solid #e2e8f0;
}

.data-table td {
  padding: 0.9rem 1.25rem;
  border-bottom: 1px solid #f1f5f9;
  vertical-align: middle;
}

.data-table tbody tr:hover {
  background: #f8fafc;
}

.sku-cell {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-weight: 600;
  color: #0f172a;
  white-space: nowrap;
}

.name-cell {
  max-width: 320px;
}

.product-name {
  font-weight: 600;
  color: #0f172a;
}

.product-desc {
  font-size: 0.8rem;
  color: #64748b;
  margin-top: 0.15rem;
}

.category-pill {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  background: #f1f5f9;
  color: #334155;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 500;
}

.badge-status {
  display: inline-block;
  padding: 0.25rem 0.65rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-available {
  background: #dcfce7;
  color: #15803d;
}

.status-warning {
  background: #fef3c7;
  color: #b45309;
}

.status-danger {
  background: #fee2e2;
  color: #b91c1c;
}

.status-muted {
  background: #f1f5f9;
  color: #64748b;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.text-right {
  text-align: right;
}

.text-center {
  text-align: center;
}

.font-mono {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
}

.state-message {
  padding: 3rem 1.5rem;
  text-align: center;
  color: #64748b;
  font-size: 0.92rem;
}

/* Tombol */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.65rem 1rem;
  font-size: 0.88rem;
  font-weight: 600;
  border-radius: 6px;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-primary {
  background: #0f172a;
  color: #ffffff;
}

.btn-primary:hover:not(:disabled) {
  background: #1e293b;
}

.btn-outline {
  background: #ffffff;
  border-color: #cbd5e1;
  color: #334155;
}

.btn-outline:hover:not(:disabled) {
  background: #f8fafc;
  border-color: #94a3b8;
}

.btn-danger {
  background: #ef4444;
  color: #ffffff;
}

.btn-danger:hover:not(:disabled) {
  background: #dc2626;
}

.btn-sm {
  padding: 0.4rem 0.75rem;
  font-size: 0.8rem;
}

.btn-xs {
  padding: 0.25rem 0.55rem;
  font-size: 0.78rem;
  border-radius: 4px;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(15, 23, 42, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  padding: 1rem;
}

.modal-dialog {
  background: #ffffff;
  border-radius: 8px;
  width: 100%;
  max-width: 580px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.modal-sm {
  max-width: 440px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h4 {
  margin: 0;
  font-size: 1.05rem;
  font-weight: 700;
  color: #0f172a;
}

.btn-close {
  background: transparent;
  border: none;
  font-size: 1.5rem;
  line-height: 1;
  color: #64748b;
  cursor: pointer;
}

.modal-body {
  padding: 1.5rem;
}

.modal-subtext {
  font-size: 0.82rem;
  color: #64748b;
  margin-top: 0.5rem;
}

.modal-form {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.full-width {
  grid-column: 1 / -1;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.form-group label {
  font-size: 0.82rem;
  font-weight: 600;
  color: #334155;
}

.required {
  color: #ef4444;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 0.6rem 0.85rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.9rem;
  outline: none;
  background: #ffffff;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: #0f172a;
}

.field-error {
  font-size: 0.78rem;
  color: #ef4444;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid #e2e8f0;
}

.toast-banner {
  padding: 0.85rem 1.25rem;
  border-radius: 6px;
  font-size: 0.88rem;
  font-weight: 500;
}

.toast-success {
  background: #dcfce7;
  color: #166534;
  border: 1px solid #bbf7d0;
}

.toast-error {
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

.alert-error {
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #fecaca;
  padding: 0.75rem 1rem;
  border-radius: 6px;
  font-size: 0.85rem;
}
</style>
