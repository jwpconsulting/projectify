<!-- SPDX-License-Identifier: AGPL-3.0-or-later -->
<!-- SPDX-FileCopyrightText: 2023 JWP Consulting GK -->
<script lang="ts">
    import { _ } from "svelte-i18n";

    import Button from "$lib/funabashi/buttons/Button.svelte";
    import {
        rejectDestructiveOverlay,
        resolveDestructiveOverlay,
    } from "$lib/stores/globalUi";
    import type { DestructiveOverlayType } from "$lib/types/ui";
    import { getDisplayName } from "$lib/types/user";

    export let target: DestructiveOverlayType;

    let title: string;
    let body: string;
    let warning: string;
    let buttonLabel: string;
    $: {
        switch (target.kind) {
            case "deleteLabel":
                title = $_("overlay.destructive.delete-label.title");
                body = $_("overlay.destructive.delete-label.body", {
                    values: { label: target.label.name },
                });
                warning = $_("overlay.destructive.delete-label.warning");
                buttonLabel = $_("overlay.destructive.delete-label.button");
                break;
            case "deleteTeamMember":
                title = $_("overlay.destructive.delete-team-member.title");
                body = $_("overlay.destructive.delete-team-member.body", {
                    values: {
                        teamMember: getDisplayName(target.teamMember.user),
                    },
                });
                warning = $_("overlay.destructive.delete-team-member.warning");
                buttonLabel = $_(
                    "overlay.destructive.delete-team-member.button",
                );
                break;
            case "deleteSection":
                title = $_("overlay.destructive.delete-section.title");
                body = $_("overlay.destructive.delete-section.body", {
                    values: {
                        section: target.section.title,
                    },
                });
                warning = $_("overlay.destructive.delete-section.warning");
                buttonLabel = $_("overlay.destructive.delete-section.button");
                break;
            case "deleteTask":
                title = $_("overlay.destructive.delete-task.title");
                body = $_("overlay.destructive.delete-task.body", {
                    values: { task: target.task.title },
                });
                warning = $_("overlay.destructive.delete-task.warning");
                buttonLabel = $_("overlay.destructive.delete-task.button");
                break;
            case "archiveProject":
                title = $_("overlay.destructive.archive-project.title");
                body = $_("overlay.destructive.archive-project.body", {
                    values: { project: target.project.title },
                });
                warning = $_("overlay.destructive.archive-project.warning");
                buttonLabel = $_("overlay.destructive.archive-project.button");
                break;
            case "deleteProject":
                title = $_("overlay.destructive.delete-project.title");
                body = $_("overlay.destructive.delete-project.body", {
                    values: { project: target.project.title },
                });
                warning = $_("overlay.destructive.delete-project.warning");
                buttonLabel = $_("overlay.destructive.delete-project.button");
                break;
        }
    }
</script>

<div
    class="flex w-full max-w-lg flex-col items-center gap-4 rounded-lg bg-foreground p-8"
>
    <div class="text-center text-3xl font-bold text-base-content">{title}</div>
    <div
        class="flex w-full flex-col items-center gap-8 border-t border-border pt-2"
    >
        <div
            class="text-normal w-full overflow-auto text-center text-base-content"
        >
            <p>{body}</p>
            <p class="text-destructive">{warning}</p>
        </div>
        <div class="flex w-full flex-row items-center justify-center gap-2">
            <Button
                style={{ kind: "secondary" }}
                size="medium"
                color="blue"
                grow
                action={{ kind: "button", action: rejectDestructiveOverlay }}
                label={$_("overlay.destructive.cancel")}
            />
            <Button
                style={{ kind: "primary" }}
                size="medium"
                color="red"
                grow
                action={{ kind: "button", action: resolveDestructiveOverlay }}
                label={buttonLabel}
            />
        </div>
    </div>
</div>
