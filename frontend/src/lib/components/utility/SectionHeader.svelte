<script lang="ts">
    let extraClasses;
    export {extraClasses as class}
</script>

<div class="flex-row-container items-center gap-4 {extraClasses}">
    <slot />
    <hr class="flex-grow border-b"/>
</div>