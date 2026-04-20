<template>
    <div class="layout-container">
        <!-- 头部 -->
        <AppHeader />

        <!-- 内容区域 -->
        <main class="layout-container__content">
            <!-- 左侧菜单 -->
            <AppSidebar />

            <!-- 右侧内容 -->
            <section class="layout-container__main">
                <router-view v-slot="{ Component }">
                    <transition
                        name="slide-fade"
                    >
                        <component
                            :is="Component"
                            :key="route.path"
                        />
                    </transition>
                </router-view>
            </section>
        </main>
    </div>
</template>

<script setup lang="ts" name="Layout">
import { useRoute } from 'vue-router';
import AppHeader from './components/AppHeader.vue';
import AppSidebar from './components/AppSidebar.vue';

const route = useRoute();
</script>

<style scoped lang="less">
.layout-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;

    &__content {
        display: flex;
        flex: 1;
        background-color: #f5f7fa;
    }

    &__main {
        flex: 1;
        overflow-y: auto;
    }
}

// 页面切换动画
.slide-fade-enter-active {
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  transition-delay: 0.1s;
}

.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(0.55, 0.085, 0.68, 0.53);
}

.slide-fade-enter-from {
  transform: translateX(50px) scale(0.98);
  opacity: 0;
  filter: blur(2px);
}

.slide-fade-leave-to {
  transform: translateX(-30px) scale(1.02);
  opacity: 0;
  filter: blur(1px);
}

/* 新增：更明显的淡入淡出动画 */
.fade-scale-enter-active {
  transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.fade-scale-leave-active {
  transition: all 0.3s cubic-bezier(0.55, 0.085, 0.68, 0.53);
}


.fade-scale-enter-from {
  transform: scale(0.95);
  opacity: 0;
}

.fade-scale-leave-to {
  transform: scale(1.05);
  opacity: 0;
}

/* 新增：滑动缩放组合动画 */
.slide-zoom-enter-active {
  transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  transition-delay: 0.1s;
}

.slide-zoom-leave-active {
  transition: all 0.4s cubic-bezier(0.55, 0.085, 0.68, 0.53);
}

.slide-zoom-enter-from {
  transform: translateY(30px) scale(0.9);
  opacity: 0;
}

.slide-zoom-leave-to {
  transform: translateY(-20px) scale(1.1);
  opacity: 0;
}
</style>
