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
};
export default config;
