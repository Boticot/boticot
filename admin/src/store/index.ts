import Vue from 'vue';
import Vuex from 'vuex';
import jwt from 'jsonwebtoken';
import { initEntities, calculateEntityColor } from '@/service/entityService';
import { GlobalEntity } from '@/types';

Vue.use(Vuex);

function getExpiration(token: string) {
  const decodedToken: any = jwt.decode(token);
  return decodedToken.exp;
}

export default new Vuex.Store({
  state: {
    agents: Array<string>(),
    intents: Array<string>(),
    entities: Array<GlobalEntity>(),
    token: localStorage.getItem('token') || '',
  },
  getters: {
    entitiesNames: (state) => () => state.entities.map((element: GlobalEntity): string => element.entity),
    entityColor: (state) => (entity: string) => state.entities.find((e) => e.entity === entity)?.color,
    isLoggedIn: (state) => () => (state.token !== '' && getExpiration(state.token) >= new Date().getTime() / 1000),
    authToken: (state) => () => state.token,
  },
  mutations: {
    initAgents(state, newAgents) {
      state.agents = newAgents;
    },
    addAgent(state, newAgent) {
      state.agents.push(newAgent);
    },
    deleteAgent(state, agentName) {
      const index = state.agents.indexOf(agentName);
      if (index > -1) {
        state.agents.splice(index, 1);
      }
    },
    addEntity(state, newEntity) {
      const usedColors = state.entities.map((e) => e.color);
      state.entities.push({
        entity: newEntity,
        color: calculateEntityColor(usedColors),
      });
    },
    addIntent(state, newIntent) {
      if (state.intents) {
        state.intents.push(newIntent);
        state.intents.sort();
      } else {
        state.intents = [newIntent];
      }
    },
    async updateAgent(state, agentResponse) {
      state.intents = agentResponse.intents.sort();
      state.entities = initEntities(agentResponse.entities);
    },
    updateToken(state, userToken) {
      state.token = userToken;
      localStorage.setItem('token', userToken);
    },
  },
  actions: {},
  modules: {},
});
