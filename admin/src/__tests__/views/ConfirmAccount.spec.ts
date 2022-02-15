import { createLocalVue, mount, Wrapper } from '@vue/test-utils';
import ElementUI from 'element-ui';
import VueRouter from 'vue-router';
import ConfirmAccount from '@/views/ConfirmAccount.vue';
import * as authModule from '@/client/auth';

const localVue = createLocalVue();
localVue.use(ElementUI);
localVue.use(VueRouter);
const mockedStore = {
  getters: {
    login: () => 'fake-login',
  },
};
const router = new VueRouter();

describe('ConfirmAccount.vue', () => {
  let wrapper: Wrapper<any>;
  let comp: any;

  beforeEach(() => {
    wrapper = mount(ConfirmAccount, {
      localVue,
      router,
      data() {
        return {
          changePasswordModel: {
            login: 'fake-login@mail.fr',
            password: 'fakePassword123',
            checkPassword: 'fakePassword123',
          },
        };
      },
      mocks: {
        $store: {
          ...mockedStore,
        },
      },
    });
    comp = wrapper.vm;
  });

  it('should call confirmChangePassword', async () => {
    // given
    jest.spyOn(authModule, 'resetPassword').mockResolvedValue('resolved-value');

    // when
    comp.confirmChangePassword();
    await comp.$nextTick();

    // then
    expect(router.currentRoute.path).toEqual('/');
    expect(comp.$data.showChangePasswordForm).toEqual(false);
    expect(authModule.resetPassword).toHaveBeenCalledTimes(1);
    expect(authModule.resetPassword).toHaveBeenCalledWith('fake-login@mail.fr', 'fakePassword123');
  });

  it('should call cancelChangePassword', async () => {
    // when
    comp.cancelChangePassword();
    await comp.$nextTick();

    // then
    expect(router.currentRoute.path).toEqual('/');
    expect(comp.$data.showChangePasswordForm).toEqual(false);
  });
});
