// Import the `mount()` method from Vue Test Utils
import { createLocalVue, mount } from '@vue/test-utils';
import ElementUI from 'element-ui';
import App from '@/App.vue';
import router from '@/router';
import store from '@/store';
import VueRouter from 'vue-router';
import Login from '@/views/Login.vue';
import Agents from '@/views/Agents.vue';
import Vuex from "vuex";

const localVue = createLocalVue();
localVue.use(ElementUI);
localVue.use(VueRouter);
localVue.use(Vuex);

describe('App.vue', () => {

  it('render html element', () => {
    const wrapper = mount(App, {
      localVue,
      router,
      store
    });
    expect(wrapper.find("#app").isVisible()).toBe(true);
  });

  it('testing not authorized to login page redirection in App vue', async () => {
    const wrapper = mount(App, {
      localVue,
      router,
      store
    });
    router.push("/agents");
    await wrapper.vm.$nextTick();
    expect(wrapper.findComponent(Login).exists()).toBe(true);
  });

  it('testing success redirection routing in App vue', async () => {
    const routes = [
      {
        path: '/agents',
        component: Agents
      }
     ]
     const router = new VueRouter({
      routes
     })
    const wrapper = mount(App, {
      router,
      store,
      localVue,
    });
    router.push("/agents");
    await wrapper.vm.$nextTick();
    console.log(wrapper.vm.$store.getters.isLoggedIn());
    expect(wrapper.findComponent(Agents).exists()).toBe(true);
  });
});
