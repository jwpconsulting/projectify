<script lang="ts">
    import ProfilePicture from "./profilePicture.svelte";
    export let pictureProps: any = {};
</script>

<div
    class:ring-2={pictureProps.size <= 64}
    class:ring-4={pictureProps.size > 64}
    class="shrink-0 overflow-hidden rounded-full border-primary bg-secondary text-secondary-content"
>
    <ProfilePicture {...pictureProps} />
</div>
