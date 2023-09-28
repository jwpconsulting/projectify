import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";
import type { UserConfig, ProxyOptions, UserConfigFnObject } from "vite";
import type { ConfigEnv } from "vite";
import { loadEnv } from "vite";

const configDefaults: UserConfig = {
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

const config: UserConfigFnObject = defineConfig(({ mode }: ConfigEnv) => {
    const env = loadEnv(mode, process.cwd());

    function getFromEnv(key: string): string {
        const value = env[key];
        if (!value) {
            throw new Error(`Expected ${key} to be in env`);
        }
        return value;
    }
    const proxyConfig: Record<string, ProxyOptions> | undefined =
        env.VITE_USE_LOCAL_PROXY !== undefined
            ? {
                  // We crash here if these variables are not there
                  "/graphql": {
                      target: getFromEnv("VITE_PROXY_GRAPHQL_ENDPOINT"),
                      changeOrigin: true,
                      rewrite: (path: string) =>
                          path.replace(/^\/graphql/, ""),
                  },
                  "/ws": {
                      target: getFromEnv("VITE_PROXY_WS_ENDPOINT"),
                      changeOrigin: true,
                      ws: true,
                      rewrite: (path: string) => path.replace(/^\/ws/, ""),
                  },
                  "/api": {
                      target: getFromEnv("VITE_PROXY_API_ENDPOINT"),
                      changeOrigin: true,
                      rewrite: (path: string) => path.replace(/^\/api/, ""),
                  },
              }
            : undefined;

    return {
        ...configDefaults,
        server: {
            proxy: proxyConfig,
        },
    };
});

export default config;
