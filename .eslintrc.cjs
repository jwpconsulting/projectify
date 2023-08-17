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
        "plugin:svelte/recommended",
    ],
    plugins: ["@typescript-eslint", "unused-imports", "import"],
    overrides: [
        {
            files: ["*.svelte"],
            parser: "svelte-eslint-parser",
            parserOptions: {
                parser: "@typescript-eslint/parser",
            },
        },
    ],
    ignorePatterns: [
        "node_modules/*",
        "vite.config.js",
        "svelte.config.js",
        "*.cjs",
        "build/*",
    ],
    settings: {
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
        extraFileExtensions: [".svelte"],
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
        "@typescript-eslint/switch-exhaustiveness-check": "error",
        "@typescript-eslint/no-unused-vars": [
            "error",
            {
                argsIgnorePattern: "_.*",
                varsIgnorePattern: "_.*",
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
