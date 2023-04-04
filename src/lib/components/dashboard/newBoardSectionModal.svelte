<script lang="ts">
    import { _ } from "svelte-i18n";

    let title = "";
    function submit() {
        console.error("TODO?");
    }
</script>

<div class="card-body items-center">
    <div class="form-control w-full">
        <label for="title" class="label label-text"
            >{$_("section-title")}</label
        >
        <input
            type="text"
            name="title"
            placeholder={$_("title")}
            class="input input-bordered"
            bind:value={title}
        />
    </div>
    <div class="pt-7">
        <button class="btn btn-primary" on:click={submit}
            >{$_("create")}</button
        >
    </div>
</div>
