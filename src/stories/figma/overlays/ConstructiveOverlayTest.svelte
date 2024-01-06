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
    import OverlayContainer from "$lib/components/OverlayContainer.svelte";
    import ConstructiveOverlay from "$lib/figma/overlays/constructive/ConstructiveOverlay.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import {
        constructiveOverlayState,
        openConstructiveOverlay,
        rejectConstructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { ConstructiveOverlayType } from "$lib/types/ui";

    export let target: ConstructiveOverlayType;

    let disabled = false;
    let result = "";

    async function openConstructive() {
        disabled = true;
        result = "waiting";
        try {
            await openConstructiveOverlay(target);
            result = "resolved";
        } catch {
            result = "rejected";
        } finally {
            disabled = false;
        }
    }
</script>

<p>
    Result: {result}
</p>
<Button
    action={{ kind: "button", action: openConstructive, disabled }}
    style={{ kind: "primary" }}
    color="blue"
    size="medium"
    label="Open constructive overlay"
/>

<OverlayContainer
    closeOverlay={rejectConstructiveOverlay}
    store={constructiveOverlayState}
    let:target
>
    <ConstructiveOverlay {target} />
</OverlayContainer>
