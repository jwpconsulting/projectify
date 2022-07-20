import adapter from "@sveltejs/adapter-static";
import preprocess from "svelte-preprocess";

/** @type {import('@sveltejs/kit').Config} */
const config = {
    // Consult https://github.com/sveltejs/svelte-preprocess
    // for more information about preprocessors
    preprocess: [
        preprocess({
            scss: {
                prependData: '@use "src/variables.scss" as *;',
            },
        }),
    ],

    kit: {
        adapter: adapter({
            pages: "build",
            assets: "build",
            fallback: null,
            precompress: false,
        }),

        vite: {
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
            server: {
                proxy: {
                    "/api": {
                        target: "http://127.0.0.1:8000",
                        changeOrigin: true,
                        rewrite: (path) => path.replace(/^\/api/, ""),
                    },
                    "/graphql": {
                        target: "http://127.0.0.1:8000",
                        changeOrigin: true,
                    },
                    "/ws": {
                        target: "ws://127.0.0.1:8000",
                        ws: true,
                    },
                },
            },
        },
    },
};

export default config;
