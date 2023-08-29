import type { KnipConfig } from "knip";

const config: KnipConfig = {
    ignore: ["**/*.d.ts"],
    entry: [
        ".eslintrc.cjs",
        "postcss.config.cjs",
        "svelte.config.js",
        "vite.config.ts",
        "src/routes/**/+{page,server,page.server,error,layout,layout.server}{,@*}.{js,ts,svelte}",
        "src/stories/**/*.stories.ts",
    ],
    rules: {
        binaries: "warn",
        dependencies: "warn",
        devDependencies: "warn",
        exports: "warn",
        files: "error",
        nsExports: "warn",
        types: "warn",
        unlisted: "warn",
    },
    paths: {
        // This ain't pretty, but Svelte basically does the same
        "$app/*": ["node_modules/@sveltejs/kit/src/runtime/app/*"],
        "$env/*": [".svelte-kit/ambient.d.ts"],
    },
    project: ["src/**/*.{js,ts,svelte}"],
    compilers: {
        // https://github.com/webpro/knip/blob/7011a5107b6693f70a966a12bc3c31b6bc3353a8/docs/compilers.md
        svelte: (text: string) =>
            [...text.matchAll(/import[^;]+/g)].join("\n"),
        css: (text: string) =>
            [...text.matchAll(/(?<=@)import[^;]+/g)].join("\n"),
    },
};

export default config;
