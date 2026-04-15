<template>
  <div class="login-container">
    <!-- 背景装饰 -->
    <div class="login-background">
      <div class="bg-circle circle-1"></div>
      <div class="bg-circle circle-2"></div>
      <div class="bg-circle circle-3"></div>
    </div>

    <div class="login-card-wrapper">
      <el-card class="login-card" shadow="always">
        <template #header>
          <div class="login-card__header">
            <h1 class="header-title">欢迎登录</h1>
            <p class="header-subtitle">FastAPI 后台管理系统</p>
          </div>
        </template>
        
        <el-form
          ref="formRef"
          :model="loginForm"
          :rules="rules"
          class="login-form"
          size="large"
        >
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              prefix-icon="User"
              clearable
            />
          </el-form-item>
          
          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              prefix-icon="Lock"
              show-password
              @keyup.enter="handleLogin"
            />
          </el-form-item>
          
          <el-form-item style="width: 100%">
            <el-button
              type="primary"
              :loading="loading"
              class="login-button"
              @click="handleLogin"
              style="width: 100%"
            >
              {{ loading ? '登录中...' : '登 录' }}
            </el-button>
          </el-form-item>
          
          <div class="form-footer">
            <span class="footer-text">还没有账号？</span>
            <el-link
              type="primary"
              class="register-link"
              @click="goToRegister"
            >
              立即注册
            </el-link>
          </div>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts" name="LoginView">
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, type FormInstance, type FormRules } from 'element-plus';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();
const formRef = ref<FormInstance>();
const loading = ref(false);

const loginForm = reactive({
  username: '',
  password: ''
});

const rules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
};

async function handleLogin() {
  if (!formRef.value) return;
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true;
      try {
        await authStore.login(loginForm.username, loginForm.password);
        ElMessage.success({
          message: '登录成功',
          duration: 500 // 1.5秒
        });
        // 延迟跳转，让用户看到成功提示
        setTimeout(() => {
          router.push('/home');
        }, 500);
      } catch (error: any) {
        ElMessage.error(error.message||error||'登录失败');
      } finally {
        loading.value = false;
      }
    }
  });
}

function goToRegister() {
  router.push('/register');
}
</script>

<style scoped lang="less">
.login-container {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  background-size: 200% 200%;
  animation: gradientShift 15s ease infinite;

  &__background {
    position: absolute;
    width: 100%;
    height: 100%;
    overflow: hidden;
    z-index: 0;
  }
  .login-card{
    padding: 20px;
  }
  .login-card-wrapper {
    position: relative;
    z-index: 1;
    width: 100%;
    max-width: 520px;
    padding: 20px;
    animation: slideIn 0.6s ease-out;
  }

  &__card {
    border-radius: 16px;
    overflow: hidden;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);

    :deep(.el-card__header) {
      background: #fff;
      border-bottom: 1px solid #ebeef5;
      padding: 28px 40px 20px;
    }

    :deep(.el-card__body) {
      padding: 32px 40px 28px;
    }
  }

  &__header {
    text-align: center;
    padding: 12px 0 8px;

    .header-title {
      margin: 0 0 10px 0;
      font-size: 26px;
      font-weight: 600;
      color: #303133;
      letter-spacing: 1px;
    }

    .header-subtitle {
      margin: 0;
      font-size: 14px;
      color: #909399;
      font-weight: 400;
    }
  }

  &__form {
    width: 100%;

    .el-form-item {
      margin-bottom: 26px;
      width: 100%;

      :deep(.el-input__wrapper) {
        padding: 13px 16px;
        border-radius: 6px;
        box-shadow: 0 0 0 1px #dcdfe6 inset;
        transition: all 0.3s ease;

        &:hover {
          box-shadow: 0 0 0 1px #c0c4cc inset;
        }

        &.is-focus {
          box-shadow: 0 0 0 1px #409EFF inset;
        }
      }

      :deep(.el-input__inner) {
        font-size: 15px;
      }
    }

    .login-button {
      width: 100%;
      display: block;
    }
  }

  &__button {
    width: 100%;
    height: 46px;
    font-size: 16px;
    font-weight: 500;
    letter-spacing: 4px;
    border-radius: 6px;
    background: #409EFF;
    border: none;
    transition: all 0.3s ease;

    &:hover {
      background: #66b1ff;
      box-shadow: 0 2px 12px rgba(64, 158, 255, 0.3);
    }

    &:active {
      background: #3a8ee6;
    }
  }
}

.form-footer {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #ebeef5;

  .footer-text {
    font-size: 14px;
    color: #909399;
  }

  .register-link {
    font-size: 14px;
    font-weight: 500;
    transition: all 0.3s ease;

    &:hover {
      transform: translateX(2px);
    }
  }
}

// 背景装饰动画
.bg-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(20px);
  animation: float 20s infinite ease-in-out;

  &.circle-1 {
    width: 400px;
    height: 400px;
    top: -150px;
    left: -150px;
    animation-delay: 0s;
  }

  &.circle-2 {
    width: 500px;
    height: 500px;
    bottom: -200px;
    right: -200px;
    animation-delay: -5s;
  }

  &.circle-3 {
    width: 300px;
    height: 300px;
    top: 50%;
    right: 10%;
    animation-delay: -10s;
  }
}

// 动画定义
@keyframes gradientShift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes logoFloat {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-8px);
  }
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg);
  }
  25% {
    transform: translate(20px, 30px) rotate(90deg);
  }
  50% {
    transform: translate(-20px, -20px) rotate(180deg);
  }
  75% {
    transform: translate(30px, -30px) rotate(270deg);
  }
}

// 响应式设计
@media (max-width: 768px) {
  .login-container {
    padding: 16px;

    &__card-wrapper {
      padding: 12px;
    }

    &__header {
      .logo-icon {
        width: 56px;
        height: 56px;
      }

      .header-title {
        font-size: 24px;
      }

      .header-subtitle {
        font-size: 14px;
      }
    }
  }
}
</style>
