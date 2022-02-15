import {
  authenticateUser, resetPassword,
} from '@/client/auth';
import {
  createUser, deleteUser,
  getAllUsers, getUser, updateUser,
} from '@/client/users';
import axios from 'axios';

describe('auth.ts', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should authenticate user', async () => {
    // given
    const mockedResponse = { data: { access_token: 'mocked-token' } };
    jest.spyOn(axios, 'post').mockResolvedValue(mockedResponse);

    // when
    const authUser = await authenticateUser({
      email: 'fake-login',
      password: 'fake-password',
    });

    // then
    expect(authUser).toEqual(mockedResponse.data);
    expect(axios.post).toHaveBeenCalledTimes(1);
  });

  it('should not authenticate user', async () => {
    // given
    jest.spyOn(axios, 'post').mockRejectedValue('errorResponse');

    // when
    authenticateUser({
      email: 'fake-login',
      password: 'fake-password',
    })
      .then() // then
      .catch((error) => expect(error).toEqual('errorResponse'));
    expect(axios.post).toHaveBeenCalledTimes(1);
  });

  it('should create user', async () => {
    // given
    const mockedResponse = { data: { fake_property: 'fake_value' } };
    jest.spyOn(axios, 'post').mockResolvedValue(mockedResponse);

    // when
    const createdUser = await createUser({
      email: 'fake_email',
      password: 'fake_password',
      role: 'fake_role',
      agents: [],
    });

    // then
    expect(createdUser).toEqual(mockedResponse.data);
    expect(axios.post).toHaveBeenCalledTimes(1);
  });

  it('should not create user', async () => {
    // given
    jest.spyOn(axios, 'post').mockRejectedValue('errorResponse');

    // when
    createUser({
      email: 'fake_email',
      password: 'fake_password',
      role: 'fake_role',
      agents: [],
    })
      .then() // then
      .catch((error) => expect(error).toEqual('errorResponse'));
    expect(axios.post).toHaveBeenCalledTimes(1);
  });

  it('should get all users', async () => {
    // given
    const mockedResponse = { data: { users: [{ fakeProperty: 'fakeValue' }] } };
    jest.spyOn(axios, 'get').mockResolvedValue(mockedResponse);
    // when
    const allUsers = await getAllUsers();

    // then
    expect(allUsers).toEqual(mockedResponse.data);
    expect(axios.get).toHaveBeenCalledTimes(1);
  });

  it('should not get all users', async () => {
    // given
    jest.spyOn(axios, 'get').mockRejectedValue('errorResponse');

    // when
    getAllUsers()
      .then() // then
      .catch((error) => expect(error).toEqual('errorResponse'));
    expect(axios.get).toHaveBeenCalledTimes(1);
  });

  it('should get users', async () => {
    // given
    const mockedResponse = { data: { user: { fakeProperty: 'fakeValue' } } };
    jest.spyOn(axios, 'get').mockResolvedValue(mockedResponse);
    // when
    const user = await getUser('fakeLogin');

    // then
    expect(user).toEqual(mockedResponse.data);
    expect(axios.get).toHaveBeenCalledTimes(1);
  });

  it('should not get users', async () => {
    // given
    jest.spyOn(axios, 'get').mockRejectedValue('errorResponse');

    // when
    getUser('fakeLogin')
      .then() // then
      .catch((error) => expect(error).toEqual('errorResponse'));
    expect(axios.get).toHaveBeenCalledTimes(1);
  });

  it('should update user', async () => {
    // given
    const mockedResponse = { data: { fake_property: 'fake_value' } };
    jest.spyOn(axios, 'put').mockResolvedValue(mockedResponse);

    // when
    const updatedUser = await updateUser({
      email: 'fake_email',
      password: 'fake_password',
      role: 'fake_role',
      agents: [],
    });

    // then
    expect(updatedUser).toEqual(mockedResponse.data);
    expect(axios.put).toHaveBeenCalledTimes(1);
  });

  it('should not update user', async () => {
    // given
    jest.spyOn(axios, 'put').mockRejectedValue('errorResponse');

    // when
    updateUser({
      email: 'fake_email',
      password: 'fake_password',
      role: 'fake_role',
      agents: [],
    })
      .then() // then
      .catch((error) => expect(error).toEqual('errorResponse'));
    expect(axios.put).toHaveBeenCalledTimes(1);
  });

  it('should delete user', async () => {
    // given
    const mockedResponse = { data: { user: { fakeProperty: 'fakeValue' } } };
    jest.spyOn(axios, 'delete').mockResolvedValue(mockedResponse);
    // when
    const deletedUser = await deleteUser('fakeLogin');

    // then
    expect(deletedUser).toEqual(mockedResponse.data);
    expect(axios.delete).toHaveBeenCalledTimes(1);
  });

  it('should not delete user', async () => {
    // given
    jest.spyOn(axios, 'delete').mockRejectedValue('errorResponse');

    // when
    deleteUser('fakeLogin')
      .then() // then
      .catch((error) => expect(error).toEqual('errorResponse'));
    expect(axios.delete).toHaveBeenCalledTimes(1);
  });

  it('should reset password', async () => {
    // given
    const mockedResponse = { data: { user: { fakeProperty: 'fakeValue' } } };
    jest.spyOn(axios, 'post').mockResolvedValue(mockedResponse);
    // when
    const result = await resetPassword('fakeLogin', 'fakeNewPassword');

    // then
    expect(result).toEqual(mockedResponse.data);
    expect(axios.post).toHaveBeenCalledTimes(1);
  });

  it('should not reset password', async () => {
    // given
    jest.spyOn(axios, 'post').mockRejectedValue('errorResponse');

    // when
    resetPassword('fakeLogin', 'fakeNewPassword')
      .then() // then
      .catch((error) => expect(error).toEqual('errorResponse'));
    expect(axios.post).toHaveBeenCalledTimes(1);
  });
});
