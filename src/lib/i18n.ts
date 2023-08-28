import { addMessages, getLocaleFromNavigator, init } from "svelte-i18n";

import en from "../messages/en.json";

addMessages("en", en);

const initialization = init({
    fallbackLocale: "en",
    initialLocale: getLocaleFromNavigator(),
});
if (initialization) {
    initialization.catch((error) => {
        console.error("Something went wrong when adding messages:", error);
    });
}
