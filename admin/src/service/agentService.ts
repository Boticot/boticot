import { getAgents, addAgent } from '@/client/agent';
import { deleteTrainingData, updateTrainingData, addTrainingData } from '@/client/trainingData';
import { EntryType, NluData } from '@/types';

const getAgentsNames = async (): Promise<Array<string>> => {
  const agents = await getAgents();
  const agentNames = agents.map((a) => a.name);
  return agentNames;
};

const deleteElement = async (type: EntryType, agentName: string, elementId: string): Promise<void> => {
  if (type === EntryType.TrainingData) {
    deleteTrainingData(agentName, elementId);
  }
};

const updateElement = async (agentName: string, nluData: NluData): Promise<void> => {
  const entitiesToAdd = nluData.entities.map((e) => ({
    start: e.start,
    end: e.end,
    value: e.value,
    entity: e.entity,
  }));
  const body = {
    intent: nluData.intent.name,
    entities: entitiesToAdd,
    text: nluData.text,
  };
  const { type } = nluData;
  if (type === EntryType.TrainingData) {
    updateTrainingData(agentName, nluData.id, { data: body });
  } else if (type === EntryType.Inputs || type === EntryType.TryIt) {
    addTrainingData(agentName, { data: [body] });
  }
};

const createNewAgent = async (agentName: string, configType: string, language: string,
  configuration: any, fallback: number, trainingData: any, defaultResponses: any): Promise<void> => {
  let nluPipeline = {};
  if (configType === 'supervised_embeddings') {
    nluPipeline = { language, pipeline: configType };
  } else {
    nluPipeline = configuration;
  }
  const data = {
    name: agentName,
    config: nluPipeline,
    fallback: fallback / 100,
    rasa_nlu_data: trainingData,
    responses: defaultResponses,
  };
  const response = await addAgent(data);
  return response;
};

export {
  getAgentsNames, deleteElement, updateElement, createNewAgent,
};
