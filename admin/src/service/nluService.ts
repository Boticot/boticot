
import { getInputs, parseText } from '@/client/agent';
import { getTrainingData } from '@/client/trainingData';
import _ from 'lodash';
import {
  NluData, Entity, SplitText, NluEntries, EntryType,
} from '@/types';

function calculateConfidence(confidence: number): number {
  if (confidence) {
    return (confidence <= 1) ? parseFloat((confidence * 100).toFixed(2)) : confidence;
  }
  return 0;
}

function convertToNluDataArray(entries: any, entryType: EntryType) {
  const nluData: Array<NluData> = [];
  entries.forEach((element: any) => {
    const data: NluData = {
      id: element._id,
      type: entryType,
      intent: {
        name: (element.intent.name) ? element.intent.name : element.intent,
        confidence: calculateConfidence(element.intent.confidence),
      },
      text: element.text,
      fulfillmentText: element.fulfillment_text,
      splitTexts: [],
      entities: [],
    };
    if (element.text !== undefined) {
      if (element.entities !== undefined && !_.isEmpty(element.entities)) {
        element.entities.sort((a: any, b: any) => a.start - b.start);
        if (element.entities[0].start !== 0 && element.text !== undefined) {
          const splitTextBeforeFirstEntity: SplitText = {
            text: (element.text !== undefined) ? element.text.substring(0, element.entities[0].start) : '',
            start: 0,
          };
          data.splitTexts.push(splitTextBeforeFirstEntity);
        }
        element.entities.forEach((entity: any, i: number) => {
          const ent: Entity = {
            entity: entity.entity,
            value: entity.value,
            start: entity.start,
            end: entity.end,
          };
          ent.confidence = calculateConfidence(entity.confidence);
          data.entities.push(ent);
          const splitTextEntity: SplitText = {
            text: element.text.substring(entity.start, entity.end),
            entity: entity.entity,
            start: ent.start,
          };
          data.splitTexts.push(splitTextEntity);
          if (element.entities[i + 1] !== undefined
            && element.entities[i + 1].start !== element.entities[i].end + 1) {
            const startIndex = element.entities[i].end + 1;
            const endIndex = element.entities[i + 1].start;
            const splitTextBetweenEntity: SplitText = {
              text: element.text.substring(startIndex, endIndex),
              start: startIndex,
            };
            data.splitTexts.push(splitTextBetweenEntity);
          }
        });
        if (element.entities[element.entities.length - 1].end < element.text.length) {
          const startIndex = element.entities[element.entities.length - 1].end;
          const endIndex = element.text.length;
          const splitTextAfterLastEntity: SplitText = {
            text: element.text.substring(startIndex, endIndex),
            start: startIndex,
          };
          data.splitTexts.push(splitTextAfterLastEntity);
        }
      } else {
        const splitText: SplitText = {
          text: element.text,
          start: 0,
        };
        data.splitTexts.push(splitText);
      }
      nluData.push(data);
    }
  });
  return nluData;
}

const convertToNluData = (entry: any, entryType: EntryType): NluData => {
  const nluDataArray: Array<NluData> = convertToNluDataArray([entry], entryType);
  return nluDataArray[0];
};

const getAgentTrainingData = async (agentName: string, page: number): Promise<NluEntries> => {
  const response: any = await getTrainingData(agentName, page);
  const trainings: any = response.items;
  const data = trainings.map((element: any) => ({ _id: element._id, ...element.data }));
  const nluDataArray: Array<NluData> = convertToNluDataArray(data, EntryType.TrainingData);
  const nluEntries: NluEntries = {
    count: response.count,
    items: nluDataArray,
  };
  return nluEntries;
};

const getAgentInputs = async (agentName: string, page: number): Promise<NluEntries> => {
  const response: any = await getInputs(agentName, page);
  const agentInputs: any = response.items;
  const nluDataArray: Array<NluData> = convertToNluDataArray(agentInputs, EntryType.Inputs);
  const nluEntries: NluEntries = {
    count: response.count,
    items: nluDataArray,
  };
  return nluEntries;
};

const getNluEntryFromParseText = async (agentName: string, text: string): Promise<NluData> => {
  const response: any = await parseText(agentName, text);
  const nluData: NluData = convertToNluData(response, EntryType.TryIt);
  nluData.id = '1';
  return nluData;
};

export {
  getAgentTrainingData, getAgentInputs, getNluEntryFromParseText, convertToNluData,
};
