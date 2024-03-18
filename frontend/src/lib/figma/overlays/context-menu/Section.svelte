<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!--
    Copyright (C) 2023, 2024 JWP Consulting GK

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
    import {
        ArrowDown,
        ArrowUp,
        Pencil,
        Selector,
        Trash,
        X,
    } from "@steeze-ui/heroicons";
    import { _ } from "svelte-i18n";

    import ContextMenuButton from "$lib/figma/buttons/ContextMenuButton.svelte";
    import Layout from "$lib/figma/overlays/context-menu/Layout.svelte";
    import {
        moveSection,
        deleteSection as repoDeleteSection,
    } from "$lib/repository/workspace/section";
    import { toggleSectionOpen, sectionClosed } from "$lib/stores/dashboard";
    import { currentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import {
        openConstructiveOverlay,
        openDestructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { Project, Section } from "$lib/types/workspace";

    export let project: Project;
    export let section: Section;

    let closed: boolean;
    $: {
        closed = $sectionClosed.has(section.uuid);
    }

    let sections: Section[] = [];
    $: sections = project.sections ?? [];

    // TODO this might have to be refactored to check if previous or next section exists

    let sectionIndex: number | undefined;
    let previousIndex: number | undefined;
    let nextIndex: number | undefined;
    let previousSection: Section | undefined;
    let nextSection: Section | undefined;

    $: {
        sectionIndex = sections.findIndex(
            (s: Section) => s.uuid == section.uuid,
        );
        previousIndex = sectionIndex > 0 ? sectionIndex - 1 : undefined;
        nextIndex =
            sectionIndex < sections.length - 1 ? sectionIndex + 1 : undefined;
        previousSection =
            previousIndex !== undefined ? sections[previousIndex] : undefined;
        nextSection =
            nextIndex !== undefined ? sections[nextIndex] : undefined;
    }

    async function switchWithPreviousSection() {
        if (!previousSection) {
            throw new Error("Expected previousSection");
        }
        await moveSection(section, previousSection._order, { fetch });
    }
    async function switchWithNextSection() {
        if (!nextSection) {
            throw new Error("Expected nextSection");
        }
        await moveSection(section, nextSection._order, { fetch });
    }

    async function updateSection() {
        await openConstructiveOverlay({
            kind: "updateSection",
            section,
        });
    }

    async function deleteSection() {
        await openDestructiveOverlay({
            kind: "deleteSection",
            section,
        });
        await repoDeleteSection(section, {
            fetch,
        });
    }
</script>

<Layout>
    <ContextMenuButton
        kind={{
            kind: "button",
            action: toggleSectionOpen.bind(null, section.uuid),
        }}
        label={closed
            ? $_("overlay.context-menu.section.expand-section")
            : $_("overlay.context-menu.section.collapse-section")}
        state="normal"
        icon={closed ? Selector : X}
    />
    {#if $currentTeamMemberCan("update", "section")}
        {#if previousSection}
            <ContextMenuButton
                kind={{
                    kind: "button",
                    action: switchWithPreviousSection,
                }}
                label={$_("overlay.context-menu.section.switch-previous")}
                state="normal"
                icon={ArrowUp}
            />
        {/if}
        {#if nextSection}
            <ContextMenuButton
                kind={{
                    kind: "button",
                    action: switchWithNextSection,
                }}
                label={$_("overlay.context-menu.section.switch-next")}
                state="normal"
                icon={ArrowDown}
            />
        {/if}
        <ContextMenuButton
            kind={{
                kind: "button",
                action: updateSection,
            }}
            label={$_("overlay.context-menu.section.edit-title")}
            state="normal"
            icon={Pencil}
        />
    {/if}
    {#if $currentTeamMemberCan("delete", "section")}
        <ContextMenuButton
            kind={{
                kind: "button",
                action: deleteSection,
            }}
            label={$_("overlay.context-menu.section.delete-section")}
            state="normal"
            icon={Trash}
            color="destructive"
        />
    {/if}
</Layout>
