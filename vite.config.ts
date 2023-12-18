import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";
import type {
    UserConfig,
    ProxyOptions,
    PluginOption,
    UserConfigExport,
} from "vite";
import type { ConfigEnv } from "vite";
import { loadEnv } from "vite";

const pluginDefaults: PluginOption[] = [sveltekit()];

const configDefaults: UserConfig = {
    esbuild: {
        // It could be useful to drop console etc. here using the following
        // config
        // drop: ["console", "debugger"],
    },
    build: {
        target: ["es2020"],
    },
};

async function getPluginOptions(mode: string): Promise<PluginOption[]> {
    if (mode !== "staging") {
        return pluginDefaults;
    }
    const { visualizer } = await import("rollup-plugin-visualizer");
    return [
        ...pluginDefaults,
        visualizer({
            emitFile: true,
            filename: "bundle.html",
        }),
    ];
}

function getFromEnv(env: Record<string, string>, key: string): string {
    const value = env[key];
    if (!value) {
        throw new Error(`Expected ${key} to be in env`);
    }
    return value;
}

function getProxyConfig(
    env: Record<string, string>,
): Record<string, ProxyOptions> | undefined {
    if (env.VITE_USE_LOCAL_PROXY === undefined) {
        return undefined;
    }
    return {
        "/ws": {
            target: getFromEnv(env, "VITE_PROXY_WS_ENDPOINT"),
            changeOrigin: true,
            ws: true,
            rewrite: (path: string) => path.replace(/^\/ws/, ""),
        },
        "/api": {
            target: getFromEnv(env, "VITE_PROXY_API_ENDPOINT"),
            changeOrigin: true,
            rewrite: (path: string) => path.replace(/^\/api/, ""),
        },
    };
}

const config: UserConfigExport = defineConfig(async ({ mode }: ConfigEnv) => {
    const env = loadEnv(mode, process.cwd());

    return {
        ...configDefaults,
        plugins: await getPluginOptions(mode),
        server: {
            proxy: getProxyConfig(env),
        },
    };
});

export default config;
