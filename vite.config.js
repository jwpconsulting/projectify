import { sveltekit } from "@sveltejs/kit/vite";

/** @type {import('vite').UserConfig} */
const config = {
    plugins: [sveltekit()],
    esbuild: {
        // drop: ["console", "debugger"],
    },
    css: {
        preprocessorOptions: {
            scss: {
                additionalData: '@use "src/variables.scss" as *;',
            },
        },
    },
    build: {
        target: ["es2020"],
    },
};
export default config;
