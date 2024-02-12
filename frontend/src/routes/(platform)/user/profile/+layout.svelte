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
</script>

<div class="flex h-full flex-col items-center bg-background p-8">
    <div class="w-full max-w-lg">
        <div class="flex flex-col gap-4">
            <h1 class="text-2xl font-bold">
                {$_("user-account-settings.title")}
            </h1>
            <div class="flex flex-col gap-12 rounded-lg bg-foreground p-4">
                <slot />
            </div>
        </div>
    </div>
</div>
