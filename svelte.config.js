import adapter from "@sveltejs/adapter-static";
import preprocess from "svelte-preprocess";

/** @type {import('@sveltejs/kit').Config} */
const config = {
    // Consult https://github.com/sveltejs/svelte-preprocess
    // for more information about preprocessors
    preprocess: [preprocess({})],

    kit: {
        adapter: adapter({
            pages: "build",
            assets: "build",
            fallback: "redirect.html",
            precompress: false,
            strict: true,
        }),
        typescript: {
            config(config) {
                return {
                    ...config,
                    include: [...config.include, "../tailwind.config.ts"],
                };
            },
        },
    },
};

// eslint-disable-next-line
export default config;
