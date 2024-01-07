// SPDX-License-Identifier: AGPL-3.0-or-later
/*
 *  Copyright (C) 2023 JWP Consulting GK
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
import type { KnipConfig } from "knip";

const config: KnipConfig = {
    ignore: ["**/*.d.ts"],
    entry: ["postcss.config.cjs", "bin/check-i18n", "src/bin/check-i18n.ts"],
    /* Extensions looked up by running the following in fish:
     * for file in (find src -type f)
     * path extension "$file"
     * end | sort | uniq
     */
    project: ["static/**/*.png", "src/**/*.{css,html,scss,svg,png,ts,svelte}"],
    rules: {
        binaries: "error",
        dependencies: "error",
        devDependencies: "error",
        exports: "error",
        files: "error",
        nsExports: "error",
        types: "error",
        unlisted: "error",
        // False positive for *.html?raw
        unresolved: "off",
    },
    paths: {
        // This ain't pretty, but Svelte basically does the same
        "$app/*": ["node_modules/@sveltejs/kit/src/runtime/app/*"],
        "$env/*": [".svelte-kit/ambient.d.ts"],
    },
    ignoreBinaries: ["env", "poetry", "tsx", "open", "bin/test"],
    compilers: {
        // https://github.com/webpro/knip/blob/7011a5107b6693f70a966a12bc3c31b6bc3353a8/docs/compilers.md
        svelte: (text: string) =>
            [...text.matchAll(/import[^;]+/g)].join("\n"),
        scss: (text: string) =>
            [...text.matchAll(/(?<=@)import[^;]+/g)].join("\n"),
    },
};

export default config;
