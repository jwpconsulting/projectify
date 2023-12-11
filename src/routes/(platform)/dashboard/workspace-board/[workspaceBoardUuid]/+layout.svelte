<!-- shared layout for workspace board and search results -->
<!-- XXX: setting overflow-x-auto here magically solves an overflowing task card
Why? Justus 2023-08-28 -->
<div class="flex h-full flex-col overflow-y-auto bg-background">
    <slot />
</div>
