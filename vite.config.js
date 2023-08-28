import { sveltekit } from "@sveltejs/kit/vite";

/** @type {import('vite').UserConfig} */
const config = {
    plugins: [sveltekit()],
    esbuild: {
        // It could be useful to drop console etc. here using the following
        // config
        // drop: ["console", "debugger"],
    },
    build: {
        target: ["es2020"],
    },
};

// eslint-disable-next-line
export default config;
