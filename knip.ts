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
