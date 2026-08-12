// jest-dom's custom matchers (toBeInTheDocument, toHaveClass, ...) are added to
// expect() at runtime by jest.setup.js. Their type declarations are not global,
// so tsc needs this reference to know the matchers exist - without it every
// assertion in the suite is a TS2339 on JestMatchers.
/// <reference types="@testing-library/jest-dom" />

export {};
