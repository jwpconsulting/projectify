import Landing from "$lib/figma/navigation/header/Landing.svelte";
import { mobileParameters } from "$lib/storybook";

export default {
    component: Landing,
};

export const Default = () => ({
    Component: Landing,
});

export const Mobile = () => ({
    Component: Landing,
});
Mobile.parameters = mobileParameters;
