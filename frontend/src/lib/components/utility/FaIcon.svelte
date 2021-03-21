<script lang="ts">
    import type {IconDefinition} from '@fortawesome/fontawesome-common-types';
    
    export let icon: IconDefinition;
    export let size: string;
    
    const [width, height, ligatures, unicode, svgPath] = icon?.icon;
</script>

<div class="flex flex-col items-center">
    <svg class="animate-swim" viewBox="0 0 {width} {height}" height={size}>
        <path fill="gray" d="{svgPath}" />
    </svg>
    <span class="text-2xl">
        <slot />
    </span>
</div>