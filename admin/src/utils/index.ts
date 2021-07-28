const colorsArray = [
  'powderblue',
  'palegreen',
  'orange',
  'yellow',
  'peachpuff',
  'gainsboro',
  'cyan',
  'tomato',
  'greenyellow',
  'fuchsia',
  'darkgoldenrod',
  'silver',
  'red',
  'cornflowerblue',
  'tan',
  'lemonchiffon',
  'gold',
  'chocolate',
  'indianred',
  'hotpink',
  'deeppink',
  'lime',
  'darkkhaki',
  'moccasin',
  'lightsalmon',
  'forestgreen',
  'deepskyblue',
  'tan',
];

const newColorsArray = (): Array<string> => Object.assign([], colorsArray);

const getRandomColor = () => {
  const letters = '0123456789ABCDEF'.split('');
  let color = '#';
  for (let i = 0; i < 6; i += 1) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
};

export { newColorsArray, getRandomColor, colorsArray };
