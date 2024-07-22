// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2021, 2022, 2023 JWP Consulting GK
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
import adapter from "@sveltejs/adapter-static";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";
import frontendSvelte from "../frontend/svelte";

/** @type {import('@sveltejs/kit').Config} */
const config = {
    // Consult https://github.com/sveltejs/svelte-preprocess
    // for more information about preprocessors
    preprocess: [vitePreprocess()],

    kit: {
        alias: {
            "$messages": "src/messages",
            "$routes": "src/routes",
            "$lib-stories": "src/lib-stories",
        },
        adapter: adapter({
            pages: "build",
            assets: "build",
            /* XXX we get this error:
             * > Using @sveltejs/adapter-static
             * Overwriting build/redirect.html with fallback page. Consider
             * using a different name for the fallback.
             */
            fallback: "redirect.html",
            precompress: false,
            strict: true,
        }),
        csp: frontendSvelte.kit.csp,
        typescript: {
            config(config) {
                return {
                    ...config,
                    include: [...config.include, "../tailwind.config.ts"],
                };
            },
        },
    },
};

// eslint-disable-next-line
export default config;
