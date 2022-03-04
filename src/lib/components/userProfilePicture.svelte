<script lang="ts">
    import ProfilePicture from "./profilePicture.svelte";
    export let pictureProps: any = {};
</script>

<div
    class:ring-2={pictureProps.size <= 64}
    class:ring-4={pictureProps.size > 64}
    class="rounded-full overflow-hidden bg-secondary text-secondary-content border-primary"
>
    <ProfilePicture {...pictureProps} />
</div>
