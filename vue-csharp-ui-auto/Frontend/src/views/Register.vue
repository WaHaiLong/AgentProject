<template>
  <div class="register-container">
    <h2>用户注册</h2>
    <form @submit.prevent="handleRegister" class="register-form">
      <div class="form-group">
        <input 
          type="text" 
          v-model="username" 
          placeholder="用户名" 
          data-testid="register-username"
          class="form-input"
          required
        />
      </div>
      <div class="form-group">
        <input 
          type="email" 
          v-model="email" 
          placeholder="邮箱" 
          data-testid="register-email"
          class="form-input"
          required
        />
      </div>
      <div class="form-group">
        <input 
          type="password" 
          v-model="password" 
          placeholder="密码 (至少6位)" 
          data-testid="register-password"
          class="form-input"
          required
        />
      </div>
      <div class="form-group">
        <input 
          type="password" 
          v-model="confirmPassword" 
          placeholder="确认密码" 
          data-testid="register-confirm-password"
          class="form-input"
          required
        />
      </div>
      <button 
        type="submit" 
        :disabled="loading"
        data-testid="register-submit-btn"
        class="form-button"
      >
        {{ loading ? '注册中...' : '注册' }}
      </button>
      <div v-if="error" class="error-message">{{ error }}</div>
      <div v-if="success" class="success-message">{{ success }}</div>
      <div class="login-link">
        已有账号？<router-link to="/login">立即登录</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Register',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      loading: false,
      error: '',
      success: ''
    }
  },
  methods: {
    async handleRegister() {
      this.loading = true
      this.error = ''
      this.success = ''
      
      // 前端验证
      if (!this.username || !this.email || !this.password || !this.confirmPassword) {
        this.error = '所有字段都必须填写'
        this.loading = false
        return
      }

      if (this.password !== this.confirmPassword) {
        this.error = '两次输入的密码不一致'
        this.loading = false
        return
      }

      if (this.password.length < 6) {
        this.error = '密码长度至少为6位'
        this.loading = false
        return
      }
      
      try {
        const response = await axios.post('/api/auth/register', {
          username: this.username,
          email: this.email,
          password: this.password,
          confirmPassword: this.confirmPassword
        })
        
        if (response.data.success) {
          this.success = '注册成功！3秒后跳转到登录页...'
          setTimeout(() => {
            this.$router.push('/login')
          }, 3000)
        } else {
          this.error = response.data.message || '注册失败'
        }
      } catch (err) {
        this.error = err.response?.data?.message || '注册请求失败'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.register-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 30px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  background-color: #fff;
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
}

.register-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.form-input {
  width: 100%;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
  box-sizing: border-box;
  transition: border-color 0.3s;
}

.form-input:focus {
  outline: none;
  border-color: #007bff;
}

.form-button {
  padding: 12px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 10px;
}

.form-button:hover:not(:disabled) {
  background-color: #218838;
}

.form-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error-message {
  color: #dc3545;
  margin-top: 10px;
  padding: 10px;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  border-radius: 4px;
  font-size: 14px;
}

.success-message {
  color: #155724;
  margin-top: 10px;
  padding: 10px;
  background-color: #d4edda;
  border: 1px solid #c3e6cb;
  border-radius: 4px;
  font-size: 14px;
}

.login-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
}

.login-link a {
  color: #007bff;
  text-decoration: none;
  font-weight: bold;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
