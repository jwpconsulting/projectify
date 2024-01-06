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
    import { Camera } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";

    export let label: string;
    export let fileSelected: (file: File, src: string) => void;
    let inputFileRef: HTMLElement;

    function click() {
        inputFileRef.click();
    }

    function onFileSelected(event: Event) {
        const eventTarget = event.target;
        if (!(eventTarget instanceof HTMLInputElement)) {
            throw new Error("Expected HTMLInputElement");
        }
        if (!eventTarget.files) {
            throw new Error("Expected eventTarget.files");
        }
        const file = eventTarget.files.item(0);
        if (!file) {
            throw new Error("Expected file");
        }

        const reader = new FileReader();
        reader.addEventListener("load", (event: ProgressEvent) => {
            const eventTarget = event.target;
            if (eventTarget instanceof FileReader) {
                const src = eventTarget.result;
                if (typeof src !== "string") {
                    throw new Error("src wasn't string");
                }
                fileSelected(file, src);
            } else {
                throw new Error("Expected FileReader");
            }
        });
        reader.readAsDataURL(file);
    }
</script>

<button
    class="focus:border-focus group h-14 w-14 rounded-full border border-transparent p-0.5"
    on:click={click}
    name="picture"
    aria-label={label}
>
    <input
        bind:this={inputFileRef}
        type="file"
        class="hidden"
        accept=".jpg, .jpeg, .png"
        on:change={onFileSelected}
    />
    <div
        class="rounded-full border border-primary bg-foreground p-3 text-primary group-hover:bg-secondary-hover group-active:bg-disabled"
    >
        <Icon src={Camera} theme="outline" />
    </div>
</button>
