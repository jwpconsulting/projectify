import { INITIAL_VIEWPORTS } from "@storybook/addon-viewport";
import type { Preview, Parameters } from "@storybook/svelte";

import "../src/storybook.css";
import "../src/app.scss";
import "../src/lib/i18n";

export const parameters: Parameters = {
    backgrounds: {
        default: "light",
    },
    actions: { argTypesRegex: "^on[A-Z].*" },
    controls: {
        matchers: {
            color: /(background|color)$/i,
            date: /Date$/,
        },
    },
    viewport: {
        viewports: INITIAL_VIEWPORTS,
    },
};

const preview: Preview = {
    parameters,
};

export default preview;
