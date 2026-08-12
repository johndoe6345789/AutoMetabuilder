/** @type {import('next').NextConfig} */
import { resolve, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));

// The @metabuilder/* sources are micro-repos checked out beside this one, the
// same arrangement package.json's file: dependencies assume. These paths used
// to read ../../libraries/<name>, from when this app lived inside metabuilder
// at frontends/workflowui; that directory has not existed here since the split,
// so every alias below silently failed to resolve.
//
// Every path is derived from this one constant and passed absolute. Turbopack
// resolves relative aliases against its own root and webpack against the
// project directory, so relative values cannot be shared between them.
const siblingsPath = resolve(__dirname, '..');
const componentsPath = resolve(siblingsPath, 'components');
const m3Path = resolve(componentsPath, 'm3');
const hooksPath = resolve(siblingsPath, 'hooks');
const iconsPath = resolve(siblingsPath, 'icons');
const scssPath = resolve(siblingsPath, 'scss');
const reduxPath = resolve(siblingsPath, 'redux');
const m3ScssPath = resolve(scssPath, 'm3-scss');

const metabuilderAliases = {
  // M3
  '@metabuilder/m3': m3Path,
  '@metabuilder/m3/scss': join(m3Path, 'scss/index.scss'),
  '@metabuilder/m3/icons': join(m3Path, 'icons/index.ts'),
  '@metabuilder/m3/hooks': join(m3Path, 'hooks.ts'),
  // Components — resolve to source
  '@metabuilder/components': join(componentsPath, 'index.tsx'),
  '@metabuilder/components/cards': join(componentsPath, 'cards/index.ts'),
  '@metabuilder/components/layout': join(componentsPath, 'layout/index.ts'),
  '@metabuilder/components/navigation': join(componentsPath, 'navigation/index.ts'),
  '@metabuilder/components/feedback': join(componentsPath, 'feedback/index.ts'),
  '@metabuilder/components/workflow-editor': join(componentsPath, 'workflow-editor/index.ts'),
  // Redux — source, not dist/, so transpilePackages works on live code
  '@metabuilder/api-clients': join(reduxPath, 'api-clients/src'),
  '@metabuilder/dbal-sso': join(reduxPath, 'dbal-sso/src'),
  '@metabuilder/dbal-sso/core': join(reduxPath, 'dbal-sso/src/core'),
  // Hooks
  '@metabuilder/hooks': join(hooksPath, 'index.ts'),
  '@metabuilder/hooks/workflow-editor': join(hooksPath, 'workflow-editor/index.ts'),
  // Shared SCSS modules
  '@scss': scssPath,
  // Shared icon exports
  '@icons': iconsPath,
};

const nextConfig = {
  basePath: '/workflowui',
  output: 'standalone',
  allowedDevOrigins: ['metabuilder.wardcrew.com', 'wardcrew.com'],
  reactStrictMode: true,
  // typedRoutes moved from experimental to top-level in Next.js 16
  typedRoutes: true,
  // Transpile local packages
  transpilePackages: [
    '@metabuilder/m3',
    '@metabuilder/api-clients',
    '@metabuilder/redux-persist',
    '@metabuilder/components',
    '@metabuilder/hooks',
    '@metabuilder/services',
    '@metabuilder/interfaces',
    '@metabuilder/dbal-sso',
  ],
  turbopack: {
    // Sources are read from outside the project directory, so the root has to
    // be the directory holding this repo and its siblings.
    root: siblingsPath,
    resolveAlias: metabuilderAliases,
  },
  sassOptions: {
    // Load paths for Angular Material SCSS - order matters!
    // m3-scss must be first so 'cdk' resolves to m3-scss/cdk
    loadPaths: [
      m3ScssPath,
      scssPath,
    ],
    includePaths: [
      m3ScssPath,
      scssPath,
    ],
    silenceDeprecations: ['legacy-js-api', 'import']
  },
  webpack: (config, { isServer }) => {
    Object.assign(config.resolve.alias, metabuilderAliases);

    // The aliases above point at sources outside this project, and those files
    // import bare specifiers ('react', 'classnames', ...) of their own. Node
    // resolution walks up from the importing file, which for a sibling repo
    // never reaches this app's node_modules - in metabuilder these packages
    // were npm workspaces and the dependencies were hoisted to a shared root.
    // Searching this app's node_modules first restores that.
    //
    // Appended, never prepended: Next resolves react differently per layer (the
    // react-server condition for Server Components), and putting an absolute
    // node_modules path first overrides that, leaving the RSC layer with the
    // client build and a null hook dispatcher at prerender time.
    config.resolve.modules = [
      ...(config.resolve.modules ?? ['node_modules']),
      resolve(__dirname, 'node_modules'),
    ];

    // Exclude Prisma client from browser bundle (dev uses IndexedDB only)
    // Prisma adapter is loaded via dynamic import() - webpack won't bundle unless used
    if (!isServer) {
      config.resolve.alias['@prisma/client'] = false;
      config.resolve.alias['.prisma/client'] = false;
    }

    config.resolve.fallback = {
      ...config.resolve.fallback,
      fs: false,
      path: false,
      crypto: false
    };
    return config;
  },
  env: {
    API_URL: process.env.API_URL || 'http://localhost:5000'
  }
};

export default nextConfig;
