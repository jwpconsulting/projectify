<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023 JWP Consulting GK

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { backToHomeUrl } from "$lib/urls";

    import illustration from "./illustration.svg";
</script>

<div class="flex h-full flex-col items-center justify-center px-16 py-8">
    <div class="flex flex-col items-center gap-12">
        <h1 class="text-center text-4xl font-bold">
            {$_("auth.confirmation-link-sent.header")}
        </h1>
        <img
            src={illustration}
            alt={$_("auth.confirmation-link-sent.illustration-alt")}
        />
        <p>{$_("auth.confirmation-link-sent.body")}</p>
        <Button
            label={$_("auth.confirmation-link-sent.back-to-homepage")}
            size="medium"
            style={{ kind: "primary" }}
            color="blue"
            action={{ kind: "a", href: backToHomeUrl }}
        />
    </div>
</div>
