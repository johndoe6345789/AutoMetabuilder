const nextJest = require('next/jest')

const createJestConfig = nextJest({
  // Provide the path to your Next.js app to load next.config.js and .env files in your test environment
  dir: './',
})

// Add any custom config to be passed to Jest
const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  testEnvironment: 'jest-environment-jsdom',
  moduleNameMapper: {
    // IMPORTANT: more-specific patterns must come BEFORE the generic '^@/(.*)$' catch-all.
    // Jest uses the FIRST matching pattern.

    // Mock @metabuilder/components (avoids ESM parse errors from deep transitive deps)
    '^@metabuilder/components$': '<rootDir>/__mocks__/componentsMock.tsx',
    '^@metabuilder/components/(.*)$': '<rootDir>/__mocks__/componentsMock.tsx',

    // Intercept @/../../../components/* (and similar) BEFORE the generic @/ catch-all
    '^@/(\\.\\./)+(components/.*)$': '<rootDir>/__mocks__/componentsMock.tsx',

    // Intercept @/../../../../../hooks/* (monorepo hooks with ESM deps)
    '^@/(\\.\\./)+(hooks/.*)$': '<rootDir>/__mocks__/componentsMock.tsx',

    // Sibling repos still import each other by paths from the pre-split
    // monorepo: hooks/ reaches for '../redux/service-adapters' and several
    // files for '../redux/redux-slices', but those directories are named
    // adapters/ and slices/ in the redux repo. Webpack never trips on this
    // because the barrels it pulls in differ; jest evaluates them eagerly.
    // Mapped here rather than edited in the other repos.
    '^(\\.\\./)+redux/service-adapters$': '<rootDir>/../redux/adapters/src/index.ts',
    '^(\\.\\./)+redux/redux-slices$': '<rootDir>/../redux/slices/src/index.ts',

    // postcss pulls nanoid, whose "browser" condition is ESM-only; jsdom picks
    // that build and jest cannot parse it. nanoid 3 ships a CJS twin.
    '^nanoid$': '<rootDir>/node_modules/nanoid/index.browser.cjs',

    // tsconfig maps these at the app level; jest needs its own copy.
    '^@icons/(.*)$': '<rootDir>/../icons/$1',
    '^@scss/(.*)$': 'identity-obj-proxy',

    // Handle module aliases
    '^@/(.*)$': '<rootDir>/src/$1',
    '^@metabuilder/m3$': '<rootDir>/__mocks__/m3Mock.tsx',
    '@/\\.\\./\\.\\./\\.\\./icons/react': '<rootDir>/__mocks__/iconsMock.tsx',
    '@/\\.\\./\\.\\./\\.\\./scss/(.*)$': 'identity-obj-proxy',
    // Fallback for icon mocks
    '\\.(svg|png|jpg|jpeg|gif)$': '<rootDir>/__mocks__/fileMock.js',
    // CSS modules
    '\\.(css|scss|sass)$': 'identity-obj-proxy',
  },
  testMatch: [
    '**/__tests__/**/*.[jt]s?(x)',
    '**/?(*.)+(spec|test).[jt]s?(x)',
  ],
  // collectCoverage is false so that normal `jest` runs stay fast.
  // CI passes --coverage explicitly via the test:coverage script.
  collectCoverage: false,
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.{js,jsx,ts,tsx}',
    '!src/**/_*.{js,jsx,ts,tsx}',
    '!src/**/__tests__/**',
    '!src/**/*.test.{js,jsx,ts,tsx}',
    '!src/**/*.spec.{js,jsx,ts,tsx}',
  ],
  coverageProvider: 'v8',
  coverageReporters: ['text', 'json', 'html', 'json-summary'],
  coverageThreshold: {
    global: {
      lines: 80,
      functions: 80,
      branches: 80,
      statements: 80,
    },
  },
  coveragePathIgnorePatterns: [
    '/node_modules/',
    '/.next/',
    '/coverage/',
    '/public/',
  ],
  // Sibling repos are imported by relative path, so their files sit outside
  // this project and Jest's upward node_modules walk never reaches ours - the
  // same gap webpack needs resolve.modules for. Without this, every suite that
  // renders an m3 component dies on "Cannot find module 'react/jsx-runtime'".
  moduleDirectories: ['node_modules', '<rootDir>/node_modules'],
  testPathIgnorePatterns: [
    '/node_modules/',
    '/.next/',
    // @metabuilder/workflow is a separate package with its own CI job; its
    // suites are not configured to run under this app's jest setup.
    '/workflow-lib/',
    // Playwright and vitest suites - different runners, not jest's to collect.
    '/playwright/',
    '/test-server/',
    '/workflow_editor/',
  ],
  // nanoid, uuid and lodash-es ship ESM only; without transforming them Jest
  // fails to parse their entry points ("Unexpected token 'export'").
  transformIgnorePatterns: [
    '/node_modules/(?!(@metabuilder|nanoid|uuid|lodash-es)/)',
  ],
}

// createJestConfig is exported this way to ensure that next/jest can load the Next.js config which is async
module.exports = createJestConfig(customJestConfig)
