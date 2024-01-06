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
    // TODO rename to just Title or maybe TaskTitle
    import { _ } from "svelte-i18n";

    import InputField from "$lib/funabashi/input-fields/InputField.svelte";

    export let title: string | undefined;
    export let onInteract: (() => void) | undefined = undefined;

    export let readonly = false;
</script>

<InputField
    name="title"
    style={{ inputType: "text" }}
    bind:value={title}
    label={undefined}
    placeholder={$_("task-screen.new-task-name")}
    onClick={onInteract}
    {readonly}
    required
/>
