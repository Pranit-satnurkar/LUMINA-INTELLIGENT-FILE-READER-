module.exports = {
    preset: 'react-native',
    setupFilesAfterEnv: ['@testing-library/jest-native/extend-expect'],
    transformIgnorePatterns: [
        'node_modules/(?!(react-native|@react-native|expo|@expo|@react-navigation|react-native-vector-icons)/)',
    ],
    testMatch: [
        '**/__tests__/**/*.test.js',
        '**/?(*.)+(spec|test).js'
    ],
    collectCoverageFrom: [
        'App.js',
        '**/*.{js,jsx}',
        '!**/node_modules/**',
        '!**/coverage/**',
        '!jest.config.js'
    ],
    coverageThreshold: {
        global: {
            statements: 50,
            branches: 40,
            functions: 50,
            lines: 50
        }
    }
};
