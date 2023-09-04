import { addMessages, getLocaleFromNavigator, init } from "svelte-i18n";
// TODO use register

import en from "../messages/en";

const defaultLocale = "en";

function initializeI18n() {
    addMessages("en", en);
    const initialization = init({
        fallbackLocale: defaultLocale,
        initialLocale: getLocaleFromNavigator(),
    });

    if (!initialization) {
        return;
    }

    initialization.catch((error) => {
        console.error("Something went wrong when adding messages:", error);
    });
}

initializeI18n();
