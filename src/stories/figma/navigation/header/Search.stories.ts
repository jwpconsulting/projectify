import Search from "$lib/figma/navigation/header/Search.svelte";
import { mobileParameters } from "$lib/storybook";

const component = Search;

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
