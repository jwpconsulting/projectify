import { sveltekit } from "@sveltejs/kit/vite";
import type { UserConfig } from "vite";

const config: UserConfig = {
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
