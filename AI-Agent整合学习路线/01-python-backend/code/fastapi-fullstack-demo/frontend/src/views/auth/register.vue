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
            <!-- 密码强度和要求 -->
            <div class="password-strength" v-if="registerForm.password">
              <div class="strength-header">
                <div class="strength-bars">
                  <span :class="['strength-bar', { weak: strengthScore >= 1 }]"></span>
                  <span :class="['strength-bar', { medium: strengthScore >= 2 }]"></span>
                  <span :class="['strength-bar', { strong: strengthScore >= 3 }]"></span>
                  <span :class="['strength-bar', { veryStrong: strengthScore >= 4 }]"></span>
                </div>
                <span :class="['strength-text', getStrengthClass()]">{{ getStrengthText() }}</span>
              </div>
              <div class="password-requirements">
                <span :class="['req-item', { met: checkRequirement('length') }]">
                  <el-icon :size="11"><CircleCheck v-if="checkRequirement('length')" /><CircleClose v-else /></el-icon>
                  <span>8 个字符</span>
                </span>
                <span :class="['req-item', { met: checkRequirement('lowercase') }]">
                  <el-icon :size="11"><CircleCheck v-if="checkRequirement('lowercase')" /><CircleClose v-else /></el-icon>
                  <span>小写字母</span>
                </span>
                <span :class="['req-item', { met: checkRequirement('uppercase') }]">
                  <el-icon :size="11"><CircleCheck v-if="checkRequirement('uppercase')" /><CircleClose v-else /></el-icon>
                  <span>大写字母</span>
                </span>
                <span :class="['req-item', { met: checkRequirement('number') }]">
                  <el-icon :size="11"><CircleCheck v-if="checkRequirement('number')" /><CircleClose v-else /></el-icon>
                  <span>数字</span>
                </span>
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
import { reactive, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage, type FormInstance, type FormRules } from 'element-plus';
import { CircleCheck, CircleClose } from '@element-plus/icons-vue';
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
        // error 已经是响应拦截器返回的错误消息字符串
        ElMessage.error(typeof error === 'string' ? error : (error.message || '注册失败'));
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
    width: 100%;
    margin-top: 10px;
    padding: 12px;
    background: linear-gradient(135deg, #f8f9fa 0%, #f0f2f5 100%);
    border-radius: 6px;
    border: 1px solid #e8eaed;
    
    .strength-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      
      .strength-bars {
        display: flex;
        gap: 4px;
        flex: 1;
        max-width: 300px;
        
        .strength-bar {
          flex: 1;
          height: 4px;
          border-radius: 2px;
          background-color: #e0e0e0;
          transition: all 0.3s ease;
          
          &.weak {
            background: linear-gradient(90deg, #f44336, #f44336);
          }
          
          &.medium {
            background: linear-gradient(90deg, #ff9800, #ff9800);
          }
          
          &.strong {
            background: linear-gradient(90deg, #4caf50, #4caf50);
          }
          
          &.veryStrong {
            background: linear-gradient(90deg, #2196f3, #2196f3);
          }
        }
      }
      
      .strength-text {
        font-size: 12px;
        line-height: 20px;
        font-weight: 500;
        min-width: 45px;
        text-align: right;
        
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
  }
  
  // 密码要求
  .password-requirements {
    margin-top: 10px;
    width: 100%;
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    
    .req-item {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      padding: 6px 8px;
      font-size: 11px;
      line-height: 1;
      border-radius: 4px;
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
      color: #909399;
      background: rgba(255, 255, 255, 0.6);
      height: 24px;
      border: 1px solid #e8eaed;
      
      span {
        white-space: nowrap;
      }
      
      .el-icon {
        font-size: 11px;
        flex-shrink: 0;
        display: flex;
        align-items: center;
      }
      
      // 满足状态
      &.met {
        color: #67c23a;
        font-weight: 500;
        background: rgba(103, 194, 58, 0.08);
        border-color: rgba(103, 194, 58, 0.2);
        
        .el-icon {
          animation: successBounce 0.3s ease;
        }
      }
      
      // 未满足状态
      &:not(.met) {
        .el-icon {
          animation: subtlePulse 2s ease-in-out infinite;
        }
        
        &:hover {
          background: rgba(0, 0, 0, 0.02);
          border-color: #dcdfe6;
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

// 密码要求图标动画
@keyframes subtlePulse {
  0%, 100% {
    opacity: 0.6;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.05);
  }
}

@keyframes successBounce {
  0% {
    transform: scale(0.8);
    opacity: 0;
  }
  50% {
    transform: scale(1.2);
  }
  100% {
    transform: scale(1);
    opacity: 1;
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
