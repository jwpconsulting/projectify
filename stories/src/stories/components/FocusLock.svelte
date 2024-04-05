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
    import { onMount } from "svelte";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { keepFocusInside } from "$lib/utils/focus";

    let buttonGroup: HTMLElement;

    let message = "Nothing yet";

    let unfocus: (() => void) | undefined = undefined;

    function action(t: string) {
        message = t;
    }

    function activateFocusLock() {
        if (unfocus) {
            action("Already enabled");
            return;
        }
        unfocus = keepFocusInside(buttonGroup);
        action("Focus lock enabled");
    }

    function deactivateFocusLock() {
        if (!unfocus) {
            action("Already unfocused");
            return;
        }
        unfocus();
    }

    onMount(() => {
        return () => {
            if (unfocus) {
                unfocus();
            }
        };
    });
</script>

<div>
    <p>Status: {message}</p>
    <h1>Commands</h1>
    <Button
        action={{ kind: "button", action: activateFocusLock }}
        style={{ kind: "primary" }}
        size="medium"
        label="Activate focus lock"
        color="blue"
    />
</div>

<div>
    <h1>Unreachable button here:</h1>
    <Button
        action={{ kind: "button", action: () => action("0 was clicked") }}
        style={{ kind: "primary" }}
        size="medium"
        label="0"
        color="red"
    />
</div>

<div
    bind:this={buttonGroup}
    class="rounded-full border-2 border-black p-4 px-32 py-4"
    aria-labelledby="dialog-title"
    aria-describedby="dialog-description"
    role="dialog"
    aria-modal="true"
>
    <h1 id="dialog-title">These can be focused</h1>
    <p id="dialog-description">
        A focus trap should prevent focus from leaving this modal
    </p>
    <Button
        action={{ kind: "button", action: () => action("1 was clicked") }}
        style={{ kind: "primary" }}
        size="medium"
        label="1"
        color="blue"
    />
    <Button
        action={{ kind: "button", action: () => action("2 was clicked") }}
        style={{ kind: "primary" }}
        size="medium"
        label="2"
        color="blue"
    />
    <Button
        action={{ kind: "button", action: deactivateFocusLock }}
        style={{ kind: "primary" }}
        size="medium"
        label="Deactivate focus lock"
        color="blue"
    />
</div>

<div>
    <h1>Unreachable button here:</h1>
    <Button
        action={{ kind: "button", action: () => action("4 was clicked") }}
        style={{ kind: "primary" }}
        size="medium"
        label="4"
        color="red"
    />
</div>
