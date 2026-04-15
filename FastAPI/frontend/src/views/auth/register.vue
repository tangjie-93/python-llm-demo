<template>
  <div class="register-container">
    <!-- 背景装饰 -->
    <div class="register-background">
      <div class="bg-circle circle-1"></div>
      <div class="bg-circle circle-2"></div>
      <div class="bg-circle circle-3"></div>
    </div>

    <div class="register-card-wrapper">
      <el-card class="register-card" shadow="always">
        <template #header>
          <div class="register-card__header">
            <h1 class="header-title">创建账号</h1>
            <p class="header-subtitle">加入我们，开启精彩旅程</p>
          </div>
        </template>

        <el-form
          ref="formRef"
          :model="registerForm"
          :rules="rules"
          class="register-form"
          size="large"
        >
          <el-form-item prop="username">
            <el-input
              v-model="registerForm.username"
              placeholder="请输入用户名"
              prefix-icon="User"
              clearable
            />
          </el-form-item>

          <el-form-item prop="email">
            <el-input
              v-model="registerForm.email"
              placeholder="请输入邮箱"
              prefix-icon="Message"
              clearable
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="registerForm.password"
              type="password"
              placeholder="请输入密码"
              prefix-icon="Lock"
              show-password
            />
            <!-- 密码强度提示 -->
            <div class="password-strength" v-if="registerForm.password">
              <div class="strength-bars">
                <span :class="['strength-bar', { weak: strengthScore >= 1 }]"></span>
                <span :class="['strength-bar', { medium: strengthScore >= 2 }]"></span>
                <span :class="['strength-bar', { strong: strengthScore >= 3 }]"></span>
                <span :class="['strength-bar', { veryStrong: strengthScore >= 4 }]"></span>
              </div>
              <span :class="['strength-text', getStrengthClass()]">{{ getStrengthText() }}</span>
            </div>
            <!-- 密码要求列表 -->
            <div class="password-requirements">
              <div :class="['requirement', { met: checkRequirement('length') }]">
                <i :class="checkRequirement('length') ? 'el-icon-check' : 'el-icon-close'"></i>
                <span>至少 8 个字符</span>
              </div>
              <div :class="['requirement', { met: checkRequirement('lowercase') }]">
                <i :class="checkRequirement('lowercase') ? 'el-icon-check' : 'el-icon-close'"></i>
                <span>包含小写字母</span>
              </div>
              <div :class="['requirement', { met: checkRequirement('uppercase') }]">
                <i :class="checkRequirement('uppercase') ? 'el-icon-check' : 'el-icon-close'"></i>
                <span>包含大写字母</span>
              </div>
              <div :class="['requirement', { met: checkRequirement('number') }]">
                <i :class="checkRequirement('number') ? 'el-icon-check' : 'el-icon-close'"></i>
                <span>包含数字</span>
              </div>
            </div>
          </el-form-item>

          <el-form-item prop="confirmPassword">
            <el-input
              v-model="registerForm.confirmPassword"
              type="password"
              placeholder="请再次输入密码"
              prefix-icon="Lock"
              show-password
              @keyup.enter="handleRegister"
            />
          </el-form-item>

          <el-form-item style="width: 100%">
            <el-button
              type="primary"
              :loading="loading"
              class="register-button"
              @click="handleRegister"
              style="width: 100%"
            >
              {{ loading ? '注册中...' : '注 册' }}
            </el-button>
          </el-form-item>

          <div class="form-footer">
            <span class="footer-text">已有账号？</span>
            <el-link
              type="primary"
              class="login-link"
              @click="goToLogin"
            >
              立即登录
            </el-link>
          </div>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup lang="ts" name="RegisterView">
import { reactive, ref } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, type FormInstance, type FormRules } from 'element-plus';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const authStore = useAuthStore();
const formRef = ref<FormInstance>();
const loading = ref(false);

const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
});

// 计算密码强度分数
const strengthScore = ref(0);

// 检查密码要求
const checkRequirement = (type: string) => {
  const password = registerForm.password;
  switch (type) {
    case 'length':
      return password.length >= 8;
    case 'lowercase':
      return /[a-z]/.test(password);
    case 'uppercase':
      return /[A-Z]/.test(password);
    case 'number':
      return /\d/.test(password);
    default:
      return false;
  }
};

// 计算密码强度
const calculateStrength = () => {
  const password = registerForm.password;
  let score = 0;
  
  if (password.length >= 8) score++;
  if (/[a-z]/.test(password)) score++;
  if (/[A-Z]/.test(password)) score++;
  if (/\d/.test(password)) score++;
  if (/[^a-zA-Z0-9]/.test(password)) score++; // 特殊字符加分
  
  strengthScore.value = Math.min(score, 4);
};

// 获取强度等级类名
const getStrengthClass = () => {
  if (strengthScore.value <= 1) return 'weak';
  if (strengthScore.value === 2) return 'medium';
  if (strengthScore.value === 3) return 'strong';
  return 'very-strong';
};

// 获取强度文本
const getStrengthText = () => {
  if (strengthScore.value === 0) return '';
  if (strengthScore.value <= 1) return '弱';
  if (strengthScore.value === 2) return '中等';
  if (strengthScore.value === 3) return '强';
  return '非常强';
};

const validateUsername = (_rule: unknown, value: string, callback: (error?: Error) => void) => {
  if (!value) {
    callback(new Error('请输入用户名'));
  } else if (!/^[a-zA-Z0-9_]{4,32}$/.test(value)) {
    callback(new Error('用户名应为 4-32 位字母、数字或下划线'));
  } else {
    callback();
  }
};

const validatePassword = (_rule: unknown, value: string, callback: (error?: Error) => void) => {
  if (!value) {
    callback(new Error('请输入密码'));
    return;
  }
  
  if (value.length < 8) {
    callback(new Error('密码长度至少为 8 位'));
    return;
  }
  
  if (!/[a-z]/.test(value)) {
    callback(new Error('密码必须包含小写字母'));
    return;
  }
  
  if (!/[A-Z]/.test(value)) {
    callback(new Error('密码必须包含大写字母'));
    return;
  }
  
  if (!/\d/.test(value)) {
    callback(new Error('密码必须包含数字'));
    return;
  }
  
  callback();
};

const validateConfirmPassword = (_rule: unknown, value: string, callback: (error?: Error) => void) => {
  if (!value) {
    callback(new Error('请再次输入密码'));
  } else if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'));
  } else {
    callback();
  }
};

// 监听密码变化
const watch = (await import('vue')).watch;
watch(() => registerForm.password, () => {
  calculateStrength();
});

const rules: FormRules = {
  username: [
    { validator: validateUsername, trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { validator: validatePassword, trigger: 'blur' }
  ],
  confirmPassword: [
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
};

async function handleRegister() {
  if (!formRef.value) return;

  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true;
      try {
        await authStore.register(
          registerForm.username,
          registerForm.email,
          registerForm.password
        );
        ElMessage.success({
          message: '注册成功，请登录',
          duration: 1500
        });
        setTimeout(() => {
          router.push('/login');
        }, 1500);
      } catch (error: any) {
        ElMessage.error(error.response?.data?.detail || '注册失败');
      } finally {
        loading.value = false;
      }
    }
  });
}

function goToLogin() {
  router.push('/login');
}
</script>

<style scoped lang="less">
.register-container {
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

  .register-card {
    padding: 20px;
  }

  .register-card-wrapper {
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

  // 密码强度提示样式
  .password-strength {
    margin-top: 8px;
    padding: 8px 0;
    
    .strength-bars {
      display: flex;
      gap: 4px;
      margin-bottom: 6px;
      
      .strength-bar {
        flex: 1;
        height: 4px;
        border-radius: 2px;
        background-color: #e0e0e0;
        transition: all 0.3s ease;
        
        &.weak {
          background-color: #f44336;
        }
        
        &.medium {
          background-color: #ff9800;
        }
        
        &.strong {
          background-color: #4caf50;
        }
        
        &.veryStrong {
          background-color: #2196f3;
        }
      }
    }
    
    .strength-text {
      font-size: 12px;
      font-weight: 500;
      
      &.weak {
        color: #f44336;
      }
      
      &.medium {
        color: #ff9800;
      }
      
      &.strong {
        color: #4caf50;
      }
      
      &.very-strong {
        color: #2196f3;
      }
    }
  }
  
  // 密码要求列表样式
  .password-requirements {
    margin-top: 12px;
    padding: 12px;
    background-color: #f5f7fa;
    border-radius: 6px;
    
    .requirement {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 6px;
      font-size: 12px;
      color: #909399;
      transition: all 0.3s ease;
      
      &:last-child {
        margin-bottom: 0;
      }
      
      i {
        font-size: 12px;
        transition: all 0.3s ease;
      }
      
      &.met {
        color: #67c23a;
        
        i {
          color: #67c23a;
        }
      }
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

    .register-button {
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

  .login-link {
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
  .register-container {
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
