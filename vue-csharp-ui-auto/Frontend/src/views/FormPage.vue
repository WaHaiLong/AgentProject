<template>
  <div class="form-container">
    <h2>表单提交测试</h2>
    <form @submit.prevent="handleSubmit" class="form-page">
      <div class="form-group">
        <label for="form-name">姓名:</label>
        <input 
          type="text" 
          id="form-name"
          v-model="name" 
          placeholder="请输入姓名" 
          class="form-input"
        />
      </div>
      <div class="form-group">
        <label for="form-email">邮箱:</label>
        <input 
          type="email" 
          id="form-email"
          v-model="email" 
          placeholder="请输入邮箱" 
          class="form-input"
        />
      </div>
      <button 
        type="submit" 
        :disabled="loading"
        class="form-submit-btn"
      >
        {{ loading ? '提交中...' : '提交' }}
      </button>
      <div v-if="result" class="form-result" data-testid="form-result">
        {{ result }}
      </div>
      <div v-if="error" class="error-message">{{ error }}</div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'FormPage',
  data() {
    return {
      name: '',
      email: '',
      loading: false,
      result: '',
      error: ''
    }
  },
  methods: {
    async handleSubmit() {
      this.loading = true
      this.error = ''
      this.result = ''
      
      try {
        const response = await axios.post('/api/data/submit', {
          name: this.name,
          email: this.email
        })
        
        if (response.data.success) {
          this.result = '提交成功: ' + response.data.message
        } else {
          this.error = response.data.message || '提交失败'
        }
      } catch (err) {
        this.error = err.response?.data?.message || '提交请求失败'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>

<style scoped>
.form-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.form-page {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  text-align: left;
}

.form-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

.form-submit-btn {
  padding: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
}

.form-submit-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.form-result {
  margin-top: 15px;
  padding: 10px;
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
  border-radius: 4px;
}

.error-message {
  color: red;
  margin-top: 10px;
}
</style>