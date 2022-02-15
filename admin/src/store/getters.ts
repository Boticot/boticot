import jwt from 'jsonwebtoken';
import { GlobalEntity } from '@/types';

function getExpiration(token: string) {
  const decodedToken: any = jwt.decode(token);
  return decodedToken.exp;
}

function getLogin(token: string) {
  const decodedToken: any = jwt.decode(token);
  return decodedToken.identity;
}

export default {
  entitiesNames: (state: any) => () => state.entities.map((element: GlobalEntity): string => element.entity),

  entityColor: (state: any) => (entity: string) => state.entities.find((e: any) => e.entity === entity)?.color,

  isLoggedIn: (state: any) => () => (state.token !== '' && getExpiration(state.token) >= new Date().getTime() / 1000),

  authToken: (state: any) => () => state.token,

  login: (state: any) => () => getLogin(state.token),

  isSuperAdmin: (state: any) => () => state.role === 'super-admin',

  isAdmin: (state: any) => () => state.role === 'admin',

  isReadUser: (state: any) => () => state.role === 'read',

  isWriteUser: (state: any) => () => state.role === 'write',
};
