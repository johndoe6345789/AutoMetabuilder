import js from '@eslint/js'
import globals from 'globals'
import reactHooks from 'eslint-plugin-react-hooks'
import tseslint from 'typescript-eslint'

/**
 * Flat config for workflowui.
 *
 * `next lint` was removed in Next 16 and this repo had no ESLint config at all,
 * so nothing here had ever been linted.
 *
 * Deliberately does not extend eslint-config-next: that pulls in
 * eslint-plugin-react, whose latest release (7.37.5) peers at eslint ^9.7 and
 * crashes under the eslint 10 this repo pins - it calls context.getFilename(),
 * removed in 10. metabuilder's frontends/nextjs config avoids it the same way,
 * composing typescript-eslint and react-hooks directly.
 *
 * Rules are the non-type-checked recommended sets. Type-aware linting is the
 * obvious next step, but it wants a codebase that has been linted at least
 * once first.
 */
export default tseslint.config(
  {
    ignores: [
      '.next/**',
      'node_modules/**',
      'coverage/**',
      'public/**',
      'test-results/**',
      'next-env.d.ts',
      // @metabuilder/workflow is a separate package with its own CI job.
      'workflow-lib/**',
      // Different runners and toolchains, not this config's to police.
      'playwright/**',
      'test-server/**',
      'workflow_editor/**',
      '__mocks__/**',
    ],
  },
  {
    extends: [js.configs.recommended, ...tseslint.configs.recommended],
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      ecmaVersion: 2022,
      globals: { ...globals.browser, ...globals.node },
    },
    plugins: {
      'react-hooks': reactHooks,
    },
    rules: {
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',
      '@typescript-eslint/no-unused-vars': ['error', {
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_',
        caughtErrorsIgnorePattern: '^_',
      }],
      // Severities matched to metabuilder's frontends/nextjs config, which
      // treats both as debt to track rather than gates: this codebase predates
      // any linting, and 64 `any` uses are a typing project, not a bug fix.
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/no-require-imports': 'warn',
      'no-debugger': 'error',
      'prefer-const': 'error',
      'no-var': 'error',
      eqeqeq: ['error', 'always', { null: 'ignore' }],
    },
  },
  {
    // Mocks and assertions need shapes the production rules would reject.
    files: ['**/__tests__/**/*.{ts,tsx}', '**/*.test.{ts,tsx}'],
    languageOptions: {
      globals: { ...globals.jest },
    },
    rules: {
      '@typescript-eslint/no-explicit-any': 'off',
      '@typescript-eslint/no-empty-function': 'off',
    },
  },
)
