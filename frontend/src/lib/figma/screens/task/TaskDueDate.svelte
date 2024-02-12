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

    import InputField from "$lib/funabashi/input-fields/InputField.svelte";

    // XXX For now, we store dates a plain strings
    // TODO when select due date, we should show the text as text-utility
    export let dueDate: string | undefined;
    export let onInteract: (() => void) | undefined = undefined;

    export let readonly = false;
</script>

<div class="flex flex-row items-center gap-4">
    <InputField
        bind:value={dueDate}
        label={undefined}
        placeholder={$_("task-screen.select-due-date")}
        name="due-date"
        style={{ inputType: "date" }}
        onClick={onInteract}
        {readonly}
    />
</div>
