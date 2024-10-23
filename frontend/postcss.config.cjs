// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2021, 2022 JWP Consulting GK
const tailwindcss = require("tailwindcss");
const autoprefixer = require("autoprefixer");

const config = {
    plugins: [
        //Some plugins, like tailwindcss/nesting, need to run before Tailwind,
        tailwindcss(),
        //But others, like autoprefixer, need to run after,
        autoprefixer,
    ],
};

module.exports = config;
