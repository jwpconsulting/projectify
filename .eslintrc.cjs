module.exports = {
    root: true,
    parser: "@typescript-eslint/parser",
    extends: [
        "eslint:recommended",
        "plugin:@typescript-eslint/recommended",
        "plugin:@typescript-eslint/recommended-requiring-type-checking",
        "plugin:@typescript-eslint/strict",
        "prettier",
        "plugin:import/recommended",
        "plugin:import/typescript",
    ],
    plugins: ["svelte3", "@typescript-eslint", "unused-imports", "import"],
    ignorePatterns: ["vite.config.js", "svelte.config.js", "*.cjs", "build/*"],
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
        project: ["./tsconfig.json"],
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
        "import/newline-after-import": "error",
        "import/no-cycle": "error",
        "import/no-relative-packages": "error",
        // https://stackoverflow.com/a//64150393
        "no-unused-vars": "off",
        "@typescript-eslint/indent": "off",
        "@typescript-eslint/no-unused-vars": [
            "error",
            {
                argsIgnorePattern: "_.*",
            },
        ],
        "@typescript-eslint/no-misused-promises": [
            "error",
            {
                checksVoidReturn: {
                    arguments: false,
                    returns: false,
                    variables: false,
                },
            },
        ],
    },
};
