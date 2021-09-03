module.exports = {
  testEnvironment: 'jsdom',
  restoreMocks: true,
  resetModules: true,
  moduleFileExtensions: [
    'js',
    'json',
    'ts',
    'vue',
  ],
  testMatch: ['**/__tests__/**/*.spec.ts?(x)'],
  transform: {
    '^.+\\.ts$': 'ts-jest',
    '.*\\.(vue)$': '@vue/vue2-jest',
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
  setupFilesAfterEnv: ['<rootDir>/jest-setup-localStorage.js'],
  setupFiles: ['<rootDir>/setEnvVars.js'],
};
