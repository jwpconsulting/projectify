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
import fs from "node:fs/promises";
import path from "node:path";
import { promisify } from "node:util";

import { sveltekit } from "@sveltejs/kit/vite";
import svg from "@poppanator/sveltekit-svg";
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
import { favicons } from "favicons";
import type { FaviconOptions } from "favicons";

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

function generateFavicons(): Plugin {
    const source = "src/favicon.svg";
    const dest = "static/";
    // TODO
    const configuration: FaviconOptions = {};
    let generatedHtml: string | undefined = undefined;
    return {
        name: "generate-favicons",
        async buildStart() {
            this.addWatchFile(source);

            const response = await favicons(source, configuration);
            const { html, images, files } = response;
            await fs.mkdir(dest, { recursive: true });
            await Promise.all(
                images.map(
                    async (image) =>
                        await fs.writeFile(
                            path.join(dest, image.name),
                            image.contents,
                        ),
                ),
            );
            await Promise.all(
                files.map(
                    async (file) =>
                        await fs.writeFile(
                            path.join(dest, file.name),
                            file.contents,
                        ),
                ),
            );

            generatedHtml = `const html = \`${html.join("\n")}\`;
export default html;`;
        },
        resolveId(id: string) {
            if (id !== "favicon-html") {
                return null;
            }
            return { id };
        },
        load(id: string) {
            if (id !== "favicon-html") {
                return null;
            }
            if (!generatedHtml) {
                throw new Error("HTML was not rendered");
            }
            return generatedHtml;
        },
    };
}

function createSitemapPlugin(domain: string, options: Options): Plugin {
    return {
        name: "create-sitemap",
        async writeBundle() {
            await createSitemap(domain, options);
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
        svg(),
        generateFavicons(),
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

async function buildInfo(env: Record<string, string>) {
    const __BUILD_DATE__ = JSON.stringify(
        new Date().toISOString().slice(0, 10),
    );

    const e = promisify(exec);
    const getResult = async (command: string): Promise<string> => {
        const { stdout } = await e(command);
        return stdout.toString().trimEnd();
    };

    const __GIT_COMMIT_DATE__ = JSON.stringify(
        "VITE_GIT_COMMIT_DATE" in env
            ? env.VITE_GIT_COMMIT_DATE
            : await getResult("git log -1 --format=%cd --date=short"),
    );
    const __GIT_BRANCH_NAME__ = JSON.stringify(
        "VITE_GIT_BRANCH_NAME" in env
            ? env.VITE_GIT_BRANCH_NAME
            : await getResult("git rev-parse --abbrev-ref HEAD"),
    );
    const __GIT_COMMIT_HASH__ = JSON.stringify(
        "VITE_GIT_COMMIT_HASH" in env
            ? env.VITE_GIT_COMMIT_HASH
            : await getResult("git rev-parse --short HEAD"),
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
            ...(await buildInfo(env)),
            __MODE__: JSON.stringify(mode),
            __WS_ENDPOINT__: JSON.stringify(
                getFromEnv(env, "VITE_WS_ENDPOINT"),
            ),
            __API_ENDPOINT__: JSON.stringify(
                getFromEnv(env, "VITE_API_ENDPOINT"),
            ),
        },
    } satisfies UserConfig;
});

export default config;
