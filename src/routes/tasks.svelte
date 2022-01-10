<script lang="ts">
    import AuthGuard from "$lib/components/authGuard.svelte";
    import WorkspacesSideNev from "$lib/components/tasks/workspaces-side-nev.svelte";
</script>

<AuthGuard>
    <main class="page page-center">
        <WorkspacesSideNev />
    </main>
</AuthGuard>
