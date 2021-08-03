<script lang="ts">
    import type {IconDefinition} from '@fortawesome/fontawesome-common-types';
    
    let extraClasses;
    export {extraClasses as class};
    
    export let icon: IconDefinition;
    export let size: string;
    
    const [width, height, svgPath] = icon?.icon;
</script>

<svg class="fill-current {extraClasses}" viewBox="0 0 {width} {height}" height={size}>
    <path d="{svgPath}" />
</svg>
