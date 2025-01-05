<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023-2024 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import TaskCard from "$lib/figma/cards/TaskCard.svelte";
    import Anchor from "$lib/funabashi/typography/Anchor.svelte";
    import {
        sectionClosed,
        currentSectionTask,
        toggleSectionOpen,
        selectInProject,
    } from "$lib/stores/dashboard/ui";
    import { getNewTaskUrl } from "$lib/urls";

    import Loading from "$lib/components/Loading.svelte";
    import Button from "$lib/funabashi/buttons/Button.svelte";
    import { currentProject } from "$lib/stores/dashboard/project";
    import { currentTeamMemberCan } from "$lib/stores/dashboard/teamMember";
    import {
        openConstructiveOverlay,
        openContextMenu,
    } from "$lib/stores/globalUi";
    import type {
        ProjectDetail,
        ProjectDetailSection,
    } from "$lib/types/workspace";
    import { currentSections } from "$lib/stores/dashboard/section";
    import { handleKey } from "$lib/utils/keyboard";
    import { onMount } from "svelte";
    import { ChevronDown, ChevronRight, Plus } from "@steeze-ui/heroicons";
    import { Icon } from "@steeze-ui/svelte-icon";
    import SquovalIcon from "$lib/funabashi/buttons/SquovalIcon.svelte";

    export let data: { injectProject?: ProjectDetail } | undefined = undefined;

    let project: ProjectDetail | undefined = undefined;
    $: project = $currentProject.value ?? data?.injectProject;

    $: hasSections = project ? project.sections.length > 0 : false;

    let sections: readonly ProjectDetailSection[];
    $: sections = $currentSections ?? data?.injectProject?.sections ?? [];

    const sectionDropDownRefs: Record<string, HTMLElement> = {};

    async function onAddNewSection() {
        if (!project) {
            throw new Error("Expected project");
        }
        await openConstructiveOverlay({
            kind: "createSection",
            project,
        });
    }

    onMount(() => {
        return handleKey("j", () => selectInProject(project, "next-task"));
    });

    onMount(() => {
        return handleKey("k", () => selectInProject(project, "prev-task"));
    });

    onMount(() => {
        return handleKey("h", () => selectInProject(project, "prev-section"));
    });

    onMount(() => {
        return handleKey("l", () => selectInProject(project, "next-section"));
    });
</script>

<svelte:head>
    {#if project && data?.injectProject === undefined}<title
            >{$_("dashboard.title", {
                values: { title: project.title },
            })}</title
        >{/if}
</svelte:head>

<!-- Sections -->
{#if project}
    {#each sections as section (section.uuid)}
        {@const uuid = section.uuid}
        {@const open = !$sectionClosed.has(uuid)}
        {@const selected = $currentSectionTask?.sectionUuid === section.uuid}
        <section class="flex flex-col" class:ring={selected}>
            <header
                class="sticky top-0 flex w-full flex-row items-center justify-between bg-foreground px-4 py-2"
            >
                <div
                    data-figma-name="Section header"
                    class="flex min-w-0 shrink flex-row gap-4 text-base-content"
                >
                    <button on:click={toggleSectionOpen.bind(null, uuid)}>
                        <Icon
                            src={open ? ChevronDown : ChevronRight}
                            class="h-6 w-6"
                            theme="outline"
                        />
                        <div class="sr-only">
                            {open
                                ? $_("dashboard.section.collapse.close")
                                : $_("dashboard.section.collapse.open")}
                        </div>
                    </button>
                    <h1 class="line-clamp-1 min-w-0 shrink font-bold">
                        {section.title}
                    </h1>
                </div>
                <div
                    class="flex shrink-0 flex-row items-center gap-1"
                    data-figma-name="Right side"
                >
                    {#if $currentTeamMemberCan("create", "task")}
                        <Button
                            action={{
                                kind: "a",
                                href: getNewTaskUrl(section),
                            }}
                            style={{
                                kind: "tertiary",
                                icon: { position: "left", icon: Plus },
                            }}
                            size="medium"
                            color="blue"
                            label={$_("dashboard.section.add-task")}
                        />
                    {/if}
                    <div bind:this={sectionDropDownRefs[uuid]}>
                        <SquovalIcon
                            ariaLabel={$_(
                                "dashboard.section.open-context-menu",
                            )}
                            icon="ellipsis"
                            state="active"
                            active={false}
                            action={{
                                kind: "button",
                                action: async () => {
                                    const ref = sectionDropDownRefs[uuid];
                                    if (!ref) {
                                        throw new Error("Expected ref");
                                    }
                                    if (!project) {
                                        throw new Error("Expected project");
                                    }
                                    await openContextMenu(
                                        {
                                            kind: "section",
                                            project,
                                            section,
                                        },
                                        ref,
                                    );
                                },
                            }}
                        />
                    </div>
                </div>
            </header>
            {#if open}
                <table
                    class="flex flex-col gap-2 rounded-b-2xl bg-foreground p-4 lg:grid lg:grid-cols-[8fr_3fr_max-content] lg:gap-4"
                >
                    {#each section.tasks as task (task.uuid)}
                        <TaskCard {project} {task} {section} />
                    {:else}
                        <p>
                            {$_("dashboard.section.empty.message")}
                            <Anchor
                                label={$_("dashboard.section.empty.prompt")}
                                size="normal"
                                href={getNewTaskUrl(section)}
                            />
                        </p>
                    {/each}
                </table>
            {/if}
        </section>
    {:else}
        <section
            class="py-2 px-4 gap-8 bg-foreground rounded-lg flex flex-col"
        >
            <p>
                {$_("dashboard.no-sections.message")}
            </p>
            <Button
                style={{ kind: "primary" }}
                color="blue"
                size="medium"
                grow={false}
                label={$_("dashboard.no-sections.prompt")}
                action={{ kind: "button", action: onAddNewSection }}
            />
        </section>
    {/each}
{:else}
    <Loading />
{/if}

{#if hasSections && $currentTeamMemberCan("create", "section")}
    <div class="sticky bottom-0 self-end p-2">
        <Button
            style={{ kind: "primary" }}
            label={$_("dashboard.actions.add-section")}
            size="medium"
            action={{ kind: "button", action: onAddNewSection }}
            color="blue"
        />
    </div>
{/if}
