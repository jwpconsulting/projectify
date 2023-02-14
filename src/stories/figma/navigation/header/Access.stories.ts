import Access from "$lib/figma/navigation/header/Access.svelte";
import { mobileParameters } from "$lib/storybook";

const component = Access;

export default {
    component: Access,
};

export const Default = () => ({
    Component: Access,
});

export const Mobile = () => ({
    Component: component,
});
Mobile.parameters = mobileParameters;
