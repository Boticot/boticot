import { beforeEach } from '@/router';
import store from '@/store';

jest.mock('@/store', () => ({
  getters: {
    isLoggedIn: jest.fn(),
    isSuperAdmin: jest.fn(),
    isAdmin: jest.fn(),
    isReadUser: jest.fn(),
    isWriteUser: jest.fn(),
  },
  commit: jest.fn(),
}));

describe('should test routing functionality', () => {
  afterEach(() => {
    store.getters.isLoggedIn.mockClear();
  });

  it('should call next() when isLoggedIn is false and IsGuest is true', () => {
    // given
    store.getters.isLoggedIn.mockImplementation(() => false);
    const to = {
      matched: [{ meta: { guest: true } }],
    };
    const next = jest.fn();

    // when
    beforeEach(to, undefined, next);

    // then
    expect(next).toHaveBeenCalled();
  });

  it('should redirect to login when isLoggedIn is false and IsGuest is false', () => {
    // given
    store.getters.isLoggedIn.mockImplementation(() => false);
    const to = {
      matched: [{ meta: { guest: false } }],
    };
    const next = jest.fn();

    // when
    beforeEach(to, undefined, next);

    // then
    expect(next).toHaveBeenCalledWith('/login');
  });

  it('should redirect to / when isLoggedIn is true and IsGuest is true', () => {
    // given
    store.getters.isLoggedIn.mockImplementation(() => true);
    const to = {
      matched: [{ meta: { guest: true } }],
    };
    const next = jest.fn();

    // when
    beforeEach(to, undefined, next);

    // then
    expect(next).toHaveBeenCalledWith('/');
  });

  it('should call next() when isLoggedIn is true and IsGuest is true and isSuperAdmin is true', () => {
    // given
    store.getters.isLoggedIn.mockImplementation(() => true);
    store.getters.isSuperAdmin.mockImplementation(() => true);
    const to = {
      matched: [{ meta: { guest: true, requiresSuperAdmin: true } }],
    };
    const next = jest.fn();

    // when
    beforeEach(to, undefined, next);

    // then
    expect(next).toHaveBeenCalled();
  });
});
