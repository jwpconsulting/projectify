import { mobileParameters, user1 } from "$lib/storybook";

import Settings from "$lib/figma/navigation/header/Settings.svelte";

const component = Settings;

export default {
    component,
};

export const Default = () => ({
    Component: component,
    props: {
        user: user1,
    },
});

export const Mobile = () => ({
    Component: component,
    props: {
        user: user1,
    },
});
Mobile.parameters = mobileParameters;
