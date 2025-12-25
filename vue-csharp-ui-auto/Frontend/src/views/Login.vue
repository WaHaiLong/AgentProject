<template>
  <div class="login-container">
    <h2>用户登录</h2>
    <form @submit.prevent="handleLogin" class="login-form">
      <div class="form-group">
        <input 
          type="text" 
          v-model="username" 
          placeholder="用户名" 
          data-testid="login-username"
          class="form-input"
        />
      </div>
      <div class="form-group">
        <input 
          type="password" 
          v-model="password" 
          placeholder="密码" 
          data-testid="login-password"
          class="form-input"
        />
      </div>
      <button 
        type="submit" 
        :disabled="loading"
        data-testid="login-submit-btn"
        class="form-button"
      >
        {{ loading ? '登录中...' : '登录' }}
      </button>
      <div v-if="error" class="error-message">{{ error }}</div>
      <div v-if="success" class="success-message">{{ success }}</div>
      <div class="register-link">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      loading: false,
      error: '',
      success: ''
    }
  },
  methods: {
    async handleLogin() {
      this.loading = true
      this.error = ''
      this.success = ''
      
      try {
        const response = await axios.post('/api/auth/login', {
          username: this.username,
          password: this.password
        })
        
        if (response.data.success) {
          this.success = '登录成功！正在跳转...'
          // 模拟跳转到首页
          setTimeout(() => {
            this.$router.push('/home')
          }, 1000)
        } else {
          this.error = response.data.message || '登录失败'
        }
      } catch (err) {
        this.error = err.response?.data?.message || '登录请求失败'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.login-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.form-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

.form-button {
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.form-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error-message {
  color: red;
  margin-top: 10px;
}

.success-message {
  color: green;
  margin-top: 10px;
}

.register-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
}

.register-link a {
  color: #007bff;
  text-decoration: none;
  font-weight: bold;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>