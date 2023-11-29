import type { KnipConfig } from "knip";

const config: KnipConfig = {
    ignore: ["**/*.d.ts"],
    entry: [
        ".eslintrc.cjs",
        "postcss.config.cjs",
        "svelte.config.js",
        "vite.config.ts",
        "src/routes/**/+{page,error,layout}{,@*}.{ts,svelte}",
        "src/bin/*.ts",
        // XXX We might have more luck convincing knip that we are importing
        // src/lib/app.scss in src/routes/+layout.svelte:
        //   import "$lib/app.scss";
        // Instead of manually specifying the stylesheet here
        "src/lib/app.scss",
    ],
    rules: {
        binaries: "error",
        dependencies: "error",
        devDependencies: "error",
        exports: "warn",
        files: "error",
        nsExports: "warn",
        types: "warn",
        unlisted: "error",
    },
    paths: {
        // This ain't pretty, but Svelte basically does the same
        "$app/*": ["node_modules/@sveltejs/kit/src/runtime/app/*"],
        "$env/*": [".svelte-kit/ambient.d.ts"],
    },
    ignoreBinaries: [
        "bin/prebuild.sh",
        "env",
        "poetry",
        "tsx",
        "open",
        "bin/test",
    ],
    project: ["src/**/*.{js,ts,svelte}"],
    compilers: {
        // https://github.com/webpro/knip/blob/7011a5107b6693f70a966a12bc3c31b6bc3353a8/docs/compilers.md
        svelte: (text: string) =>
            [...text.matchAll(/import[^;]+/g)].join("\n"),
        scss: (text: string) =>
            [...text.matchAll(/(?<=@)import[^;]+/g)].join("\n"),
    },
};

export default config;
