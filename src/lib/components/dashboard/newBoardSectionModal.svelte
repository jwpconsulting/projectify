<script lang="ts">
    import { getContext } from "svelte";

    let title = "";
    const modal = getContext<any>("modal");
    function submit() {
        modal.close({ title });
    }
</script>

<div class="card-body items-center">
    <div class="form-control w-full">
        <label for="title" class="label label-text">Section Title</label>
        <input
            type="text"
            name="title"
            placeholder="title"
            class="input input-bordered"
            bind:value={title}
        />
    </div>
    <div class="pt-7">
        <button class="btn btn-primary" on:click={submit}>Create</button>
    </div>
</div>
