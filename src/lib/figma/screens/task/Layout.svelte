<script lang="ts">
</script>

<div class="block lg:hidden">
    <div class="flex h-full flex-col gap-8 p-4">
        <slot name="top-bar" />
        <slot name="tab-bar-mobile" />
        <slot name="content" />
    </div>
</div>
<div class="hidden lg:block">
    <div class="flex h-full w-full flex-col gap-8 p-4">
        <slot name="top-bar" />
        <div class="flex h-full w-full flex-row gap-4">
            <div class="flex w-full flex-col gap-8">
                <slot name="tab-bar-desktop" />
                <slot name="content" />
            </div>
        </div>
    </div>
</div>
