import { calculateEntityColor, initEntities } from '@/service/entityService';

export default {
  initAgents(state: any, newAgents: any) {
    state.agents = newAgents;
  },
  addAgent(state: any, newAgent: any) {
    state.agents.push(newAgent);
  },
  deleteAgent(state: any, agentName: any) {
    const index = state.agents.indexOf(agentName);
    if (index > -1) {
      state.agents.splice(index, 1);
    }
  },
  addEntity(state: any, newEntity: any) {
    const usedColors = state.entities.map((e: any) => e.color);
    state.entities.push({
      entity: newEntity,
      color: calculateEntityColor(usedColors),
    });
  },
  addIntent(state: any, newIntent: any) {
    if (state.intents) {
      state.intents.push(newIntent);
      state.intents.sort();
    } else {
      state.intents = [newIntent];
    }
  },
  async updateAgent(state: any, agentResponse: any) {
    state.intents = agentResponse.intents.sort();
    state.entities = initEntities(agentResponse.entities);
  },
  updateToken(state: any, userToken: any) {
    state.token = userToken;
    localStorage.setItem('token', userToken);
  },
};
