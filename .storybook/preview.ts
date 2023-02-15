import { INITIAL_VIEWPORTS } from "@storybook/addon-viewport";

import "../src/app.scss";
import "../src/i18n.js";

export const parameters = {
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
