<template>
  <div class="login-wrapper">
    <div class="login-card">
      <div class="brand-header">
        <div class="brand-badge">SISTEM TOKO</div>
        <h2>Katalog Produk Toko</h2>
        <p class="subtitle">UTS Konstruksi &amp; Evolusi Perangkat Lunak (544597)</p>
      </div>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div v-if="errorMessage" class="alert alert-error">
          {{ errorMessage }}
        </div>

        <div class="form-group">
          <label for="email">Alamat Email</label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="admin@toko.local"
            required
            autocomplete="email"
          />
        </div>

        <div class="form-group">
          <label for="password">Kata Sandi</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="password123"
            required
            autocomplete="current-password"
          />
        </div>

        <button type="submit" class="btn btn-primary" :disabled="loading">
          {{ loading ? 'Memproses...' : 'Masuk ke Sistem' }}
        </button>
      </form>

      <div class="demo-credentials">
        <p class="demo-title">Kredensial Pengujian:</p>
        <code>Email: admin@toko.local</code>
        <code>Password: password123</code>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '../api/axios';

const router = useRouter();
const email = ref('admin@toko.local');
const password = ref('password123');
const errorMessage = ref('');
const loading = ref(false);

const handleLogin = async () => {
  errorMessage.value = '';
  loading.value = true;
  try {
    const res = await apiClient.post('/login', {
      email: email.value,
      password: password.value,
    });

    if (res.data && res.data.access_token) {
      // Simpan token ke localStorage (Soal 2a)
      localStorage.setItem('auth_token', res.data.access_token);
      localStorage.setItem('user_name', res.data.user?.name || 'Administrator');
      router.push('/');
    }
  } catch (err) {
    if (err.response && err.response.data && err.response.data.message) {
      errorMessage.value = err.response.data.message;
    } else {
      errorMessage.value = 'Gagal terhubung ke server Laravel.';
    }
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
.login-wrapper {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.login-card {
  width: 100%;
  max-width: 420px;
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
  padding: 2.2rem;
}

.brand-header {
  text-align: center;
  margin-bottom: 1.8rem;
}

.brand-badge {
  display: inline-block;
  background: #0f172a;
  color: #ffffff;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  padding: 0.25rem 0.65rem;
  border-radius: 4px;
  margin-bottom: 0.75rem;
}

.brand-header h2 {
  font-size: 1.35rem;
  font-weight: 700;
  color: #0f172a;
  margin: 0 0 0.35rem 0;
}

.subtitle {
  font-size: 0.85rem;
  color: #64748b;
  margin: 0;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  text-align: left;
}

.form-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #334155;
}

.form-group input {
  padding: 0.7rem 0.9rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.92rem;
  outline: none;
  transition: border-color 0.15s ease;
}

.form-group input:focus {
  border-color: #0f172a;
}

.btn {
  padding: 0.75rem 1rem;
  border-radius: 6px;
  font-size: 0.92rem;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: all 0.15s ease;
}

.btn-primary {
  background: #0f172a;
  color: #ffffff;
}

.btn-primary:hover:not(:disabled) {
  background: #1e293b;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.alert {
  padding: 0.75rem 1rem;
  border-radius: 6px;
  font-size: 0.85rem;
  line-height: 1.4;
}

.alert-error {
  background: #fef2f2;
  color: #991b1b;
  border: 1px solid #fecaca;
}

.demo-credentials {
  margin-top: 1.6rem;
  padding-top: 1.2rem;
  border-top: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  text-align: center;
}

.demo-title {
  font-size: 0.78rem;
  color: #64748b;
  font-weight: 600;
  margin: 0 0 0.25rem 0;
}

.demo-credentials code {
  font-size: 0.8rem;
  background: #f1f5f9;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  color: #334155;
}
</style>
