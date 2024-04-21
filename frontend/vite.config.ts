// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023-2024 JWP Consulting GK
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as published
 *  by the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU Affero General Public License for more details.
 *
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */
import { exec } from "node:child_process";
import { promisify } from "node:util";

import { sveltekit } from "@sveltejs/kit/vite";
import { enhancedImages } from "@sveltejs/enhanced-img";
import { defineConfig } from "vite";
import type {
    UserConfig,
    ProxyOptions,
    PluginOption,
    UserConfigExport,
    Plugin,
} from "vite";
import type { ConfigEnv } from "vite";
import { loadEnv } from "vite";
import { createSitemap } from "svelte-sitemap/src/index.js";
import type { Options } from "svelte-sitemap/src/interfaces/global.interface";
import { getLicenseFileText } from "generate-license-file";

function generateLicenseFile(): Plugin {
    return {
        name: "generate-license-file",
        resolveId(source: string) {
            if (source !== "third-party-licenses") {
                return null;
            }
            return { id: source };
        },
        async load(id: string) {
            if (id !== "third-party-licenses") {
                return null;
            }
            const content = await getLicenseFileText("./package.json");
            return {
                code: `export default ${JSON.stringify(content)}`,
                map: { mappings: "" },
            };
        },
    };
}

function createSitemapPlugin(domain: string, options: Options): Plugin {
    return {
        name: "create-sitemap",
        writeBundle() {
            createSitemap(domain, options);
        },
    };
}

const configDefaults: UserConfig = {
    build: {
        target: ["es2020"],
    },
};

async function getPluginOptions(
    env: Record<string, string>,
    mode: string,
): Promise<PluginOption[]> {
    const pluginDefaults: PluginOption[] = [
        enhancedImages(),
        sveltekit(),
        createSitemapPlugin(getFromEnv(env, "VITE_PROJECTIFY_DOMAIN"), {
            debug: mode !== "production",
            changeFreq: "daily",
            outDir: ".svelte-kit/output/prerendered/pages",
        }),
        generateLicenseFile(),
    ];
    if (mode !== "staging") {
        return pluginDefaults;
    }
    const { visualizer } = await import("rollup-plugin-visualizer");
    const visualizerPlugin = visualizer({
        emitFile: true,
        filename: "bundle.html",
        // https://github.com/btd/rollup-plugin-visualizer/issues/176#issuecomment-1834045713
    }) as Plugin;
    return [...pluginDefaults, visualizerPlugin];
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

async function buildInfo() {
    const e = promisify(exec);

    const getResult = async (command: string) => {
        const { stdout } = await e(command);
        return JSON.stringify(stdout.toString().trimEnd());
    };

    // kinda awkward code to write, but ok...
    const [
        __GIT_COMMIT_DATE__,
        __GIT_BRANCH_NAME__,
        __GIT_COMMIT_HASH__,
        __BUILD_DATE__,
    ] = await Promise.all(
        [
            "git log -1 --format=%cd --date=short",
            "git rev-parse --abbrev-ref HEAD",
            "git rev-parse --short HEAD",
            "date -Idate",
        ].map(getResult),
    );
    return {
        __GIT_COMMIT_DATE__,
        __GIT_BRANCH_NAME__,
        __GIT_COMMIT_HASH__,
        __BUILD_DATE__,
    };
}

const config: UserConfigExport = defineConfig(async ({ mode }: ConfigEnv) => {
    const env = loadEnv(mode, process.cwd());

    return {
        ...configDefaults,
        esbuild: {
            drop: mode === "production" ? ["console", "debugger"] : [],
        },
        plugins: await getPluginOptions(env, mode),
        server: {
            proxy: getProxyConfig(env),
        },
        define: {
            ...(await buildInfo()),
            __MODE__: JSON.stringify(mode),
        },
    } satisfies UserConfig;
});

export default config;
