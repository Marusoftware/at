<script lang="ts">
	import './layout.css';
	import { DarkMode, NavBrand, NavHamburger, NavLi, NavUl, Navbar } from 'flowbite-svelte';
	import { AuthService } from '$lib/openapi';
	import { goto } from '$app/navigation';
	import type { LayoutData } from './$types';
	import { destroyNotification, notifications } from '$lib/notification';
	import Notification from '$lib/components/Notification.svelte';
	import { fade } from 'svelte/transition';

	export let data: LayoutData;

	const user = data.user;

	const logout = async (e: Event) => {
		e.preventDefault();
		await AuthService.authSignout();
		user.set(undefined);
		await goto('/');
	};
</script>

<Navbar>
	<NavBrand href="/" class="dark:bg-gray-500 rounded p-2">
		<img src="https://marusoftware.net/theme/images/marusoftware.png" alt="Logo" class="m-1 h-6 sm:h-9" />
		@Marusoftware
	</NavBrand>
	<NavHamburger />
	<NavUl>
		{#if $user}
			<NavLi onclick={logout}>Log out</NavLi>
		{/if}

		<DarkMode class="m-0" />
	</NavUl>
</Navbar>
<div class="p-4">
	{#if $notifications}
		<div
			class="absolute top-20 right-5 w-full max-w-xs z-50 isolation space-y-1"
		>
			{#each $notifications as nortification (nortification.id)}
				<div transition:fade>
					<Notification
						title={nortification.title}
						subtitle={nortification.subtitle}
						kind={nortification.kind}
						onclose={() => destroyNotification(nortification.id ?? 0)}
					/>
				</div>
			{/each}
		</div>
	{/if}

	<slot></slot>
</div>
