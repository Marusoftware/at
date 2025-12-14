import { defineConfig } from '@hey-api/openapi-ts';

export default defineConfig({
  client: '@hey-api/client-fetch',
  input: 'http://server:8000/openapi.json',
  output: './src/lib/openapi',
  plugins: [
    '@hey-api/schemas',
    '@hey-api/typescript',
    '@hey-api/transformers',
    {
      name: '@hey-api/sdk',
      transformer: true,
      asClass: true,
      classNameBuilder: '{{name}}Service',
    },
  ]
});