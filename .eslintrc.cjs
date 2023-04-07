module.exports = {
    root: true,
    parser: "@typescript-eslint/parser",
    extends: [
        "eslint:recommended",
        "plugin:@typescript-eslint/recommended",
        "prettier",
        "plugin:import/recommended",
        "plugin:import/typescript",
    ],
    plugins: ["svelte3", "@typescript-eslint", "unused-imports", "import"],
    ignorePatterns: ["*.cjs", "build/*"],
    overrides: [{ files: ["*.svelte"], processor: "svelte3/svelte3" }],
    settings: {
        "svelte3/typescript": () => require("typescript"),
        "import/resolver": {
            typescript: {
                project: "./tsconfig.json",
                $lib: "src",
            },
        },
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
        // "sort-imports": ["error", {}],
        "unused-imports/no-unused-imports": "error",
        "import/no-unresolved": "off",
        "import/order": "error",
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
