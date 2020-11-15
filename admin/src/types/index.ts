export interface GlobalEntity {
  entity: string;
  color: string;
}

export interface Entity {
  entity: string;
  value: string;
  confidence?: number;
  start: number;
  end: number;
}

export interface Intent {
  name: string;
  confidence?: number;
}

export interface SplitText {
  text: string;
  entity?: string;
  start: number;
}

export interface NluData {
  id: string;
  type: EntryType;
  intent: Intent;
  text: string;
  splitTexts: Array<SplitText>;
  entities: Array<Entity>;
  fulfillmentText?: string;
}

export interface NluParseResult {
  id: string;
  intent: Intent;
  text: string;
  entities: Array<Entity>;
}

export interface NluEntries {
  count: number;
  items: Array<NluData>;
}

export enum EntryType {
  TrainingData = 'TrainingData',
  Inputs = 'Inputs',
  TryIt = 'TryIt',
}
