module.exports = {
    root: true,
    extends: [
        "eslint:recommended",
        "plugin:@typescript-eslint/strict-type-checked",
        "plugin:@typescript-eslint/stylistic-type-checked",
        "prettier",
        "plugin:import/recommended",
        "plugin:import/typescript",
        "plugin:svelte/recommended",
        "plugin:storybook/recommended",
        "plugin:@typescript-eslint/recommended",
    ],
    plugins: [
        "@typescript-eslint",
        "unused-imports",
        "import",
        "eslint-plugin-tsdoc",
    ],
    parser: "@typescript-eslint/parser",
    parserOptions: {
        project: ["./tsconfig.json"],
        sourceType: "module",
        ecmaVersion: 2020,
        extraFileExtensions: [".svelte"],
    },
    overrides: [
        {
            files: ["*.svelte"],
            parser: "svelte-eslint-parser",
            parserOptions: {
                parser: "@typescript-eslint/parser",
            },
            rules: {
                // TODO: Investigate whether any of these could be disabled
                "@typescript-eslint/require-await": "off",
                "@typescript-eslint/init-declarations": "off",
            },
        },
    ],
    ignorePatterns: [
        ".git",
        ".mypy_cache",
        "node_modules",
        ".storebook",
        ".svelte-kit",
    ],
    settings: {
        "import/ignore": [
            // TODO revisit this at some point in the future
            // Justus 2023-09-06
            "dom-focus-lock/dist/index.esm.js",
            "@steeze-ui/heroicons.index.js",
        ],
        "import/resolver": {
            typescript: {
                project: "./tsconfig.json",
                $lib: "src",
            },
        },
    },
    env: {
        browser: true,
        es2017: true,
        node: true,
    },
    rules: {
        "prefer-const": "error",
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
        // TODO Remove me
        "@typescript-eslint/prefer-optional-chain": "off",
        // TODO Remove me
        "@typescript-eslint/no-confusing-void-expression": "off",
        // TODO Remove me
        "@typescript-eslint/no-redundant-type-constituents": "off",
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
