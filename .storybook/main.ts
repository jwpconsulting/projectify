import type { StorybookConfig } from "@storybook/sveltekit";

const config: StorybookConfig = {
    stories: ["../src/stories/figma/**/*.stories.ts"],
    addons: ["@storybook/addon-essentials", "@storybook/addon-interactions"],
    framework: {
        name: "@storybook/sveltekit",
        options: {},
    },
    docs: {
        autodocs: "tag",
    },
    staticDirs: ["../static"],
};
export default config;
