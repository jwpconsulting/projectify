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
            rules: {
                "@typescript-eslint/init-declarations": "off",
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
        "unused-imports/no-unused-imports": "error",
        "import/no-unresolved": "off",
        "import/order": [
            "error",
            {
                "alphabetize": {
                    order: "asc",
                    caseInsensitive: true,
                },
                "groups": [
                    "builtin",
                    "external",
                    "internal",
                    "parent",
                    "sibling",
                    "index",
                    "object",
                ],
                "newlines-between": "always",
                "pathGroups": [{ pattern: "$lib/*", group: "internal" }],
            },
        ],
        "import/first": "error",
        "import/newline-after-import": "error",
        "import/no-cycle": "error",
        "import/no-relative-packages": "error",
        // https://stackoverflow.com/a//64150393
        "no-unused-vars": "off",
        // TODO find a way to apply me to svelte as well
        // While ignoring export lets.
        // This is useful because reactive code might refer to
        // HTMLElements that are undefined? Is this true? Can
        // reactive code blocks be run before a svelte component is
        // mounted?
        // Justus 2023-08-17
        "@typescript-eslint/init-declarations": ["error", "always"],
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
