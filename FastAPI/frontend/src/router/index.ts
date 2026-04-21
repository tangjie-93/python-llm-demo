import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/index.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/register.vue')
  },
  {
    path: '/',
    component: () => import('@/layout/index.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: 'home',
        name: 'Home',
        component: () => import('@/views/home/index.vue')
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('@/views/users/index.vue')
      },
      {
        path: 'items',
        name: 'Items',
        component: () => import('@/views/items/index.vue')
      },
      {
        path: 'posts',
        name: 'Posts',
        component: () => import('@/views/posts/index.vue')
      },
      {
        path: 'tags',
        name: 'Tags',
        component: () => import('@/views/tags/index.vue')
      }
    ]
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach(async (to, _from, next) => {
  const authStore = useAuthStore();
  
  // 如果有 token 但没有用户信息，尝试获取用户信息
  if (authStore.token && !authStore.userInfo) {
    try {
      await authStore.fetchUserInfo();
    } catch (error) {
      // 获取用户信息失败，可能是 token 过期，尝试刷新
      const refreshed = await authStore.refreshTokenFunc();
      if (!refreshed) {
        next('/login');
        return;
      }
    }
  }
  
  if (to.meta.requiresAuth && !authStore.token) {
    next('/login');
  } else {
    next();
  }
});

export default router;
