module.exports = {
    root: true,
    parser: "@typescript-eslint/parser",
    extends: [
        "eslint:recommended",
        "plugin:@typescript-eslint/recommended",
        "prettier",
    ],
    plugins: ["svelte3", "@typescript-eslint"],
    ignorePatterns: ["*.cjs", "build/*"],
    overrides: [{ files: ["*.svelte"], processor: "svelte3/svelte3" }],
    settings: {
        "svelte3/typescript": () => require("typescript"),
    },
    parserOptions: {
        sourceType: "module",
        ecmaVersion: 2020,
        tsconfigRootDir: __dirname,
    },
    env: {
        browser: true,
        es2017: true,
        node: true,
    },
    rules: {
        "unused-imports/no-unused-imports": "error",
        // https://stackoverflow.com/a//64150393
        "no-unused-vars": "off",
        "@typescript-eslint/no-unused-vars": [
            "error",
            {
                argsIgnorePattern: "_.*",
            },
        ],
    },
};
