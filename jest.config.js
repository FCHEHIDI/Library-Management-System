module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/tests'],
  testMatch: ['**/*.test.ts', '**/*.spec.ts'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/index.ts'
  ],
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  moduleNameMapper: {
    '^@models/(.*)$': '<rootDir>/src/models/$1',
    '^@interfaces/(.*)$': '<rootDir>/src/interfaces/$1',
    '^@enums/(.*)$': '<rootDir>/src/enums/$1',
    '^@domains/(.*)$': '<rootDir>/src/domains/$1',
    '^@policies/(.*)$': '<rootDir>/src/policies/$1',
    '^@types/(.*)$': '<rootDir>/src/types/$1'
  }
};
