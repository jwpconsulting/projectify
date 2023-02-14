import Continue from "$lib/figma/navigation/header/Continue.svelte";
import { mobileParameters } from "$lib/storybook";

const component = Continue;

export default {
    component,
};

export const Default = () => ({
    Component: component,
});

export const Mobile = () => ({
    Component: component,
});
Mobile.parameters = mobileParameters;
