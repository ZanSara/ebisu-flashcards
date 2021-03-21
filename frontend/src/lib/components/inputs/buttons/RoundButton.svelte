<script lang="ts">
    export let href: string;
    export let color: string;
</script>

<a href={href}
   class="py-1.5 px-4 rounded-xl font-medium transition-colors shadow-sm hover:text-white hover:bg-{color}-500 bg-{color}-300"
>
    <slot />
</a>