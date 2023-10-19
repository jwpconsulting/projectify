import Settings from "$lib/figma/navigation/header/Settings.svelte";
import { mobileParameters, user1 } from "$lib/storybook";

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
