import Vue from 'vue';
import Vuex from 'vuex';
import { GlobalEntity } from '@/types';
import mutations from './mutations';
import getters from './getters';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    agents: Array<string>(),
    intents: Array<string>(),
    entities: Array<GlobalEntity>(),
    token: localStorage.getItem('token') || '',
    role: localStorage.getItem('role') || '',
  },
  getters,
  mutations,
  actions: {},
  modules: {},
});
