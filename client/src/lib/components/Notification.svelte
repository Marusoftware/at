<script lang="ts">
    import Toast from 'flowbite-svelte/Toast.svelte';
	import Exclamation from "flowbite-svelte-icons/ExclamationCircleOutline.svelte";
    import Info  from 'flowbite-svelte-icons/InfoCircleOutline.svelte';
	import type { EventHandler } from 'svelte/elements';

    const kinds:{[key: string]: {color:'blue'|'yellow', icon: any}}={
        'info':{ color:"blue", icon:Info},
        'warn':{ color:"yellow", icon:Exclamation },
    }
    let { onclose, title, subtitle, kind = "info" }:{
        title:string, subtitle:string|undefined, kind:string,
        onclose: EventHandler<Event, HTMLDivElement> | null | undefined
    } = $props();
</script>

<Toast class="rounded-md" onclose={onclose} color={kinds[kind].color}>
    {#snippet icon()}
        {@const Icon = kinds[kind].icon}
        <Icon />
    {/snippet}
    {#if subtitle}
        <span class="font-semibold text-gray-900 dark:text-white">{title}</span>
    {:else}
        {title}
    {/if}
    <div class="mt-3">  
        <div class="mb-2 text-sm font-normal">{subtitle}</div>
        <slot name="actions"></slot>
    </div>
</Toast>