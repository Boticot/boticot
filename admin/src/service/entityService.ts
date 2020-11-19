import { newColorsArray } from '@/utils';
import { GlobalEntity } from '@/types';

const initEntities = (entities: Array<string>): Array<GlobalEntity> => {
  const colors = newColorsArray();
  let selectedColor: string;
  if (entities) {
    const globalEntities = entities.map((element: string): GlobalEntity => {
      [selectedColor] = colors;
      colors.splice(0, 1);
      return {
        entity: element,
        color: selectedColor,
      };
    });
    return globalEntities;
  }
  return [];
};

const calculateEntityColor = (usedColors: Array<string>): string => {
  const remainedColors = newColorsArray().filter((e) => !usedColors.includes(e));
  return remainedColors[0];
};

export { initEntities, calculateEntityColor };
