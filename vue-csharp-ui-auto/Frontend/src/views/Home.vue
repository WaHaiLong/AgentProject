<template>
  <div class="home-container">
    <h1>首页</h1>
    <p>欢迎来到首页！</p>
    <div class="user-info">
      <p>当前用户: {{ username }}</p>
    </div>
    <div class="navigation">
      <router-link to="/form" class="nav-link">表单测试页</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      username: 'test_user' // 从登录信息获取
    }
  }
}
</script>

<style scoped>
.home-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.user-info {
  margin: 20px 0;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.navigation {
  margin-top: 20px;
}

.nav-link {
  display: inline-block;
  padding: 10px 20px;
  background-color: #28a745;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}
</style>