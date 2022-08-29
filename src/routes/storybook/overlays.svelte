<script lang="ts">
    import DestructiveOverlay from "$lib/figma/DestructiveOverlay.svelte";

    const destructiveOverlays = [
        {
            kind: "deleteLabel" as const,
            label: { name: "This is a label", color: 0, uuid: "" },
        },
        {
            kind: "deleteMember" as const,
            workspaceUser: {
                user: {
                    email: "hello@example.com",
                    full_name: "Firstname Lastname",
                },
                uuid: "",
                role: "",
                created: "",
                modified: "",
            },
        },
        {
            kind: "deleteSection" as const,
            workspaceBoardSection: {
                title: "section name",
                created: "",
                modified: "",
                uuid: "",
                _order: 0,
            },
        },
        {
            kind: "deleteTask" as const,
            task: {
                title: "task name",
                created: "",
                modified: "",
                uuid: "",
                _order: 0,
                number: 1,
                labels: [],
            },
        },
        {
            kind: "deleteSelectedTasks" as const,
            tasks: [
                {
                    title: "task name",
                    created: "",
                    modified: "",
                    uuid: "",
                    _order: 0,
                    number: 1,
                    labels: [],
                },
            ],
        },
        {
            kind: "archiveBoard" as const,
            workspaceBoard: {
                title: "board name",
                created: "",
                modified: "",
                uuid: "",
            },
        },
    ];
</script>

{#each destructiveOverlays as target}
    <DestructiveOverlay {target} />
{/each}
