// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2021-2024 JWP Consulting GK
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
import adapterStatic from "@sveltejs/adapter-static";
import adapterNode from "@sveltejs/adapter-node";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

const adapter =
    process.env.PROJECTIFY_FRONTEND_ADAPTER === "static"
        ? adapterStatic({
              fallback: "fallback.html",
              strict: true,
          })
        : process.env.PROJECTIFY_FRONTEND_ADAPTER === "node"
        ? adapterNode({
              envPrefix: "SVELTE_KIT_",
          })
        : undefined;

/** @type {import('@sveltejs/kit').Config} */
const config = {
    // Consult https://github.com/sveltejs/svelte-preprocess
    // for more information about preprocessors
    preprocess: [vitePreprocess()],
    kit: {
        alias: {
            $messages: "src/messages",
            $routes: "src/routes",
        },
        adapter,
        csp: {
            directives: {
                // Mirrors root directory Caddyfile backend_headers,
                // with exception of making style-src more lenient
                // See https://github.com/sveltejs/kit/issues/11747 and
                // https://kit.svelte.dev/docs/configuration
                "default-src": ["self"],
                "style-src": ["self", "unsafe-inline"],
                "script-src": ["self"],
                "font-src": ["self"],
                "img-src": ["self", "res.cloudinary.com"],
                "form-action": ["self"],
                "connect-src": ["self"],
                "frame-ancestors": ["none"],
                "object-src": ["self"],
                "base-uri": ["self"],
            },
            // TODO add reports
        },
        typescript: {
            config(config) {
                return {
                    ...config,
                    include: [
                        ...config.include,
                        "../tailwind.config.ts",
                        "../knip.ts",
                    ],
                };
            },
        },
    },
};

// eslint-disable-next-line
export default config;
