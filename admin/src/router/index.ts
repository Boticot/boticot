import Vue from 'vue';
import VueRouter, { RouteConfig } from 'vue-router';
import store from '@/store';

Vue.use(VueRouter);

const routes: Array<RouteConfig> = [
  {
    path: '/try-it/:agentName',
    name: 'try-it',
    component: () => import('../views/TryIt.vue'),
  },
  {
    path: '/inputs/:agentName',
    name: 'inputs',
    component: () => import('../views/Inputs.vue'),
  },
  {
    path: '/training-data/:agentName',
    name: 'training-data',
    component: () => import('../views/TrainingData.vue'),
  },
  {
    path: '/responses/:agentName',
    name: 'responses',
    component: () => import('../views/Responses.vue'),
  },
  {
    path: '/model/:agentName',
    name: 'model',
    component: () => import('../views/Model.vue'),
  },
  {
    path: '/synonyms/:agentName',
    name: 'synonyms',
    component: () => import('../views/Synonyms.vue'),
  },
  {
    path: '/analytics/:agentName',
    name: 'analytics',
    component: () => import('../views/Analytics.vue'),
  },
  {
    path: '/agents',
    name: 'agents',
    component: () => import('../views/Agents.vue'),
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

router.beforeEach((to, from, next) => {
  const isLoggedIn = store.getters.isLoggedIn();
  const isGuest = to.matched.some((record) => (record.meta.guest));
  if (isLoggedIn) {
    if (isGuest) {
      next('/');
    } else {
      next();
    }
  } else if (isGuest) {
    next();
  } else {
    store.commit('updateToken', '');
    next('/login');
  }
});

export default router;
