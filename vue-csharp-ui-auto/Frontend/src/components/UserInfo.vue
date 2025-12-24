<template>
  <div class="user-info-component">
    <div v-if="isLoggedIn" class="logged-in">
      <span>欢迎, {{ username }}!</span>
      <button @click="handleLogout" class="logout-btn">退出登录</button>
    </div>
    <div v-else class="logged-out">
      <span>未登录</span>
      <router-link to="/login" class="login-link">去登录</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserInfo',
  data() {
    return {
      isLoggedIn: false,
      username: ''
    }
  },
  methods: {
    handleLogout() {
      // 简单的登出逻辑
      this.isLoggedIn = false
      this.username = ''
      this.$router.push('/login')
    }
  },
  mounted() {
    // 检查登录状态
    this.checkLoginStatus()
  },
  methods: {
    checkLoginStatus() {
      // 模拟检查登录状态
      const token = localStorage.getItem('authToken')
      if (token) {
        this.isLoggedIn = true
        this.username = localStorage.getItem('username') || 'test_user'
      }
    },
    handleLogout() {
      localStorage.removeItem('authToken')
      localStorage.removeItem('username')
      this.isLoggedIn = false
      this.username = ''
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.user-info-component {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.logged-in, .logged-out {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logout-btn, .login-link {
  padding: 5px 10px;
  background-color: #dc3545;
  color: white;
  text-decoration: none;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.login-link {
  background-color: #007bff;
}
</style>