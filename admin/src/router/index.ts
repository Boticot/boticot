import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import store from '@/store';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: '/try-it/:agentName',
    name: 'try-it',
    component: () => import('../views/TryIt.vue'),
    meta: {
      requiresSuperAdmin: true,
      requiresAdmin: true,
      requiresWrite: true,
      requiresRead: true,
    },
  },
  {
    path: '/inputs/:agentName',
    name: 'inputs',
    component: () => import('../views/Inputs.vue'),
    meta: {
      requiresSuperAdmin: true,
      requiresAdmin: true,
      requiresWrite: true,
      requiresRead: true,
    },
  },
  {
    path: '/training-data/:agentName',
    name: 'training-data',
    component: () => import('../views/TrainingData.vue'),
    meta: {
      requiresSuperAdmin: true,
      requiresAdmin: true,
      requiresWrite: true,
      requiresRead: true,
    },
  },
  {
    path: '/responses/:agentName',
    name: 'responses',
    component: () => import('../views/Responses.vue'),
    meta: {
      requiresSuperAdmin: true,
      requiresAdmin: true,
      requiresWrite: true,
      requiresRead: true,
    },
  },
  {
    path: '/model/:agentName',
    name: 'model',
    component: () => import('../views/Model.vue'),
    meta: {
      requiresSuperAdmin: true,
      requiresAdmin: true,
      requiresWrite: true,
      requiresRead: true,
    },
  },
  {
    path: '/synonyms/:agentName',
    name: 'synonyms',
    component: () => import('../views/Synonyms.vue'),
    meta: {
      requiresSuperAdmin: true,
      requiresAdmin: true,
      requiresWrite: true,
      requiresRead: true,
    },
  },
  {
    path: '/lookups/:agentName',
    name: 'lookups',
    component: () => import('../views/Lookup.vue'),
    meta: {
      requiresSuperAdmin: true,
      requiresAdmin: true,
      requiresWrite: true,
      requiresRead: true,
    },
  },
  {
    path: '/analytics/:agentName',
    name: 'analytics',
    component: () => import('../views/Analytics.vue'),
    meta: {
      requiresSuperAdmin: true,
      requiresAdmin: true,
      requiresWrite: true,
      requiresRead: true,
    },
  },
  {
    path: '/agents',
    name: 'agents',
    component: () => import('../views/Agents.vue'),
    meta: {
      requiresSuperAdmin: true,
      requiresAdmin: true,
    },
  },
  {
    path: '/users',
    name: 'users',
    component: () => import('../views/Users.vue'),
    meta: {
      requiresSuperAdmin: true,
    },
  },
  {
    path: '/changePassword',
    name: 'changePassword',
    component: () => import('../views/ConfirmAccount.vue'),
    meta: {
      requiresSuperAdmin: true,
      requiresAdmin: true,
      requiresWrite: true,
      requiresRead: true,
    },
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/Login.vue'),
    meta: {
      guest: true,
    },
  },
  {
    path: '*',
    component: () => import('../views/TryIt.vue'),
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export function beforeEach(to: any, from: any, next: any) {
  const isLoggedIn = store.getters.isLoggedIn();

  const isSuperAdminMeta = to.matched.some((record: any) => (record.meta.requiresSuperAdmin));
  const isAdminMeta = to.matched.some((record: any) => record.meta.requiresAdmin);
  const isWriteMeta = to.matched.some((record: any) => record.meta.requiresWrite);
  const isReadMeta = to.matched.some((record: any) => record.meta.requiresRead);
  const isGuest = to.matched.some((record: any) => (record.meta.guest));
  const isForMainPath = to.path === '/';

  const isSuperAdmin = store.getters.isSuperAdmin() && isSuperAdminMeta;
  const isAdmin = store.getters.isAdmin() && isAdminMeta;
  const isWriteUser = store.getters.isWriteUser() && isWriteMeta;
  const isReadUser = store.getters.isReadUser() && isReadMeta;
  if (isLoggedIn) {
    if (isGuest) {
      next('/');
    } else if (isSuperAdmin || isAdmin || isWriteUser || isReadUser || isForMainPath) {
      next();
    } else {
      next('/');
    }
  } else if (isGuest) {
    next();
  } else {
    store.commit('updateToken', '');
    next('/login');
  }
}
router.beforeEach((to, from, next) => beforeEach(to, from, next));

export default router;
