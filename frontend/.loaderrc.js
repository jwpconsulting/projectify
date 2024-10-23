// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 JWP Consulting GK
import { resolve } from "node:path";

const debug = false;

const isMd = (url) => url.match(/\.md(\?raw)?$/);

export default {
    loaders: [
        {
            // Resolve md files and stringify them
            // TODO find out how to write it like so:
            // test: isMd,
            // type: "asset/source",
            resolve(specifier, options) {
                const { parentURL } = options;
                const { href, pathname } = new URL(specifier, parentURL);
                if (!isMd(pathname)) {
                    return undefined;
                }
                if (debug) {
                    console.log(`[md] resolve: ${specifier}`);
                }
                return { format: "module", url: href };
            },
            format(url, _options) {
                const { pathname } = new URL(url);
                if (!isMd(pathname)) {
                    return undefined;
                }
                if (debug) {
                    console.log(`[md] format: ${url}`);
                }
                return { format: "module" };
            },
            transform(source, options) {
                const { url } = options;
                if (!isMd(url)) {
                    return undefined;
                }
                if (debug) {
                    console.log(`[md] transform: ${url}`);
                }
                return {
                    source: `export default ${JSON.stringify(String(source))}`,
                };
            },
        },
        {
            loader: "esm-loader-typescript",
            options: {
                debug,
            },
        },
        {
            loader: "esm-loader-import-alias",
            options: {
                aliases: {
                    $messages: `${resolve("src/messages")}`,
                },
                debug,
            },
        },
        {
            loader: "esm-loader-import-relative-extension",
            options: {
                extensions: {
                    ".ts": {
                        "": ".ts",
                    },
                },
                debug,
            },
        },
    ],
};
