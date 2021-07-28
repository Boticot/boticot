import getters from '@/store/getters';
import mutations from '@/store/mutations';
import { GlobalEntity } from '@/types';

const mockedCalculatedColor = 'mockedCalculatedColor';
const mockedEntity = { entity: 'mockedEntityName', color: 'mockedColor' };
jest.mock('@/service/entityService', () => ({
  calculateEntityColor: jest.fn().mockImplementation(() => mockedCalculatedColor),
  initEntities: jest.fn().mockImplementation(
    () => [mockedEntity],
  ),
}));

jest.mock('jsonwebtoken', () => ({
  decode: jest.fn().mockImplementation(
    () => ({ exp: new Date().getTime() / 1000 + 1 }),
  ),
}));

describe('store.ts', () => {
  let state: any;
  describe('Testing mutations', () => {
    beforeEach(() => {
      state = {
        agents: [],
        entities: Array<GlobalEntity>(),
        intents: [],
        token: '',
      };
    });

    it('should update agents of state when call initAgents', () => {
      const newAgentsData = ['agent1', 'agent2'];
      const { initAgents } = mutations;
      initAgents(state, newAgentsData);
      expect(state.agents).toEqual(newAgentsData);
    });

    it('should add agent to state when call addAgent', () => {
      const newAgentsData = 'agent1';
      const { addAgent } = mutations;
      addAgent(state, newAgentsData);
      expect(state.agents).toEqual([newAgentsData]);
    });

    it('should delete agent from state when call deleteAgent', () => {
      state.agents = ['agent1', 'agent2'];
      const agentToDeleteData = 'agent1';
      const { deleteAgent } = mutations;
      deleteAgent(state, agentToDeleteData);
      expect(state.agents).toEqual(['agent2']);
    });

    it('should update entity to state when call addEntity', () => {
      const { addEntity } = mutations;
      addEntity(state, 'entityName');
      expect(state.entities).toEqual([{ entity: 'entityName', color: 'mockedCalculatedColor' }]);
    });

    it('should add intent to state when call addIntent', () => {
      let newIntent = 'intentName2';
      const { addIntent } = mutations;
      addIntent(state, newIntent);
      expect(state.intents).toEqual(['intentName2']);
      newIntent = 'intentName1';
      addIntent(state, newIntent);
      expect(state.intents).toEqual(['intentName1', 'intentName2']); // check array sort()
    });

    it('should update agent of state when call updateAgent', () => {
      const editAgentData = { intents: ['agentName'] };
      const { updateAgent } = mutations;
      updateAgent(state, editAgentData);
      expect(state.intents).toEqual(['agentName']);
      expect(state.entities).toEqual([mockedEntity]);
    });

    it('should update token when call updateToken', () => {
      const testToken = 'token-for-test';
      const { updateToken } = mutations;
      updateToken(state, testToken);
      expect(state.token).toEqual(testToken);
      expect(localStorage.getItem('token')).toEqual(testToken);
    });
  });

  describe('Testing getters', () => {
    beforeEach(() => {
      state = {
        agents: ['agent1', 'agent2'],
        intents: ['intent1', 'intent2'],
        entities: [{ entity: 'entity1', color: 'color1' }, { entity: 'entity2', color: 'color2' }],
        token: 'test-token',
      };
    });
    it('should get names of entities from state when call entitiesNames', () => {
      const { entitiesNames } = getters;
      const result = entitiesNames(state);
      expect(result()).toEqual(['entity1', 'entity2']);
    });

    it('should get color of entity from state when call entityColor', () => {
      const { entityColor } = getters;
      const result = entityColor(state);
      expect(result('entity1')).toEqual('color1');
    });

    it('should return if the user is loggedIn when call isLoggedIn', () => {
      const { isLoggedIn } = getters;
      const result = isLoggedIn(state);
      expect(result()).toEqual(true);
    });

    it('should return the value of token when call authToken', () => {
      const { authToken } = getters;
      const result = authToken(state);
      expect(result()).toEqual('test-token');
    });
  });
});
