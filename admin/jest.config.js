module.exports = {
  testEnvironment: 'jsdom',
  moduleFileExtensions: [
    'js',
    'json',
    'ts',
    // tell Jest to handle *.vue files
    'vue',
  ],
  testMatch: ['**/__tests__/**/*.spec.ts?(x)'],
  transform: {
    // process TypeScript files
    '^.+\\.ts$': 'ts-jest',
    // process *.vue files with vue-jest
    '.*\\.(vue)$': 'vue-jest',
    '^.+\\.js$': 'babel-jest',
    '.+\\.(css|styl|less|sass|scss|png|jpg|ttf|woff|woff2)$': 'jest-transform-stub',
  },
  // support the same @ -> src alias mapping in source code
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  // serializer for snapshots
  snapshotSerializers: [
    'jest-serializer-vue',
  ],
  setupFilesAfterEnv: ['<rootDir>/src/__tests__/__mocks__/jest-setup-localStorage.js'],
};
