# Packages that don't like being removed

-   "@storybook/addon-interactions": "^7.0.0-beta.47"
-   "@storybook/blocks": "^7.0.0-beta.47"
-   "@storybook/testing-library": "^0.0.14-next.1"

# @storybock/sveltekit

## beta.47

Vite suddenly stops hot module reloading after updating some random svelte or ts
files for a while.

It happened after a while after updating a src/stories/figma/buttons/Button.svelte

Now I'm just running npm run storybook with this page open: http://localhost:6006/?path=/story/buttons-button--secondary
And I am trying to see whether it will crash after some time.

Nothing yet, so I touched src/stories/figma/buttons/Button.stories.ts and try
to see whether it crashes, yes, after a while it fails to connect to
storybook-server-channel

## beta.30

WARN Failed to load preset: "@storybook/sveltekit/preset"
ERR! Error: Cannot find module '/Users/justusperlwitz/projects/projectify/projectify-frontend/node_modules/vite-plugin-externals/dist/index.js'. Please verify that the package.json has a valid "main" entry
