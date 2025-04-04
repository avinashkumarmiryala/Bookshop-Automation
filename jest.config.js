module.exports = {
    testEnvironment: 'jsdom', // Simulates a browser environment
    setupFilesAfterEnv: ['<rootDir>/jest.setup.js'], // Optional setup file
    moduleNameMapper: {
      '\\.(css|less|scss|sass)$': 'identity-obj-proxy', // Mock CSS imports if needed
    },
    transform: {
      '^.+\\.(js|jsx)$': 'babel-jest', // Transform JS/JSX files
    },
  };