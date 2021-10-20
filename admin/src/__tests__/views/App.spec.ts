import { createLocalVue, mount } from '@vue/test-utils';
import ElementUI from 'element-ui';
import VueRouter from 'vue-router';
import App from '@/App.vue';
import router from '@/router';
import Login from '@/views/Login.vue';

const localVue = createLocalVue();
localVue.use(ElementUI);
localVue.use(VueRouter);
const mockedStore = {
  state: {
    agents: ['agent1', 'agent2'],
  },
  getters: {
    isLoggedIn: () => false,
  },
};

jest.mock('@/service/agentService');

describe('App.vue', () => {
  it('render html element', () => {
    const wrapper = mount(App, {
      localVue,
      router,
      mocks: {
        $store: {
          ...mockedStore,
        },
      },
    });
    expect(wrapper.find('#app').isVisible()).toBe(true);
  });

  it('should redirect to login page when the user is not authorized', async () => {
    const wrapper = mount(App, {
      localVue,
      router,
      mocks: {
        $store: {
          ...mockedStore,
        },
      },
    });
    router.push('/agents');
    await wrapper.vm.$nextTick();
    expect(wrapper.findComponent(Login).exists()).toBe(true);
  });
});
