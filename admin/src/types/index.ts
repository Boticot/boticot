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

export interface IntentsCountItem {
  count: number;
  intent: string;
}

export interface AnalyticItem {
  date: Date | string;
  intents_count: Array<IntentsCountItem>;
  traffic: number;
  unique_users: number;
}

export interface Analytics {
  agent_name: string;
  analytics: Array<AnalyticItem>;
}

export type PreparedAnalyticsData = {
  intentDataList: Array<string>;
  allDateDataList: Array<Date>;
  allTrafficDataList: Array<number>;
  allUniqueUsersDataList: Array<number>;
  allFallbackDataList: Array<number>;
};

export type DataSetItem = {
  label?: string;
  data: Array<any>;
  fill?: boolean;
  borderColor?: string;
  tension?: number;
  backgroundColor?: string | Array<string>;
  hoverOffset?: number;
};

export type ChartData = {
  labels: Array<Date | string>;
  datasets: Array<DataSetItem>;
}

export type SynonymElement = {
  synonyms: Array<string>;
  value: string;
}

export type SynonymsItemData = {
  _id: string;
  synonyms: SynonymElement;
}

export type SynonymsData = {
  count: number;
  items: Array<SynonymsItemData>;
}
