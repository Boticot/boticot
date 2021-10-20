module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    'plugin:vue/essential',
    '@vue/airbnb',
    '@vue/typescript/recommended',
  ],
  parserOptions: {
    ecmaVersion: 2020,
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'max-len': [2, { code: 120, tabWidth: 4, ignoreUrls: true }],
    indent: [2, 2],
    'no-underscore-dangle': 0,
    'no-param-reassign': 0,
    'import/prefer-default-export': 'off',
    'no-explicit-any': 0,
    'linebreak-style': 'off',
    '@typescript-eslint/no-non-null-assertion': 'off',
    '@typescript-eslint/camelcase': 'off',
    '@typescript-eslint/no-explicit-any': 'off',
  },
};
