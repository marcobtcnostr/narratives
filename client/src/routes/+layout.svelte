<!-- src\routes\+layout.svelte -->
<script lang="ts">
	import '../app.css';
	import { onMount } from 'svelte';
	import { derived } from 'svelte/store';

	import NarrativesDashboard from '$lib/components/pages/NarrativesDashboard.svelte';

	import { login, prepareSession } from '$lib/utils/social-utils';
	import { createSessionStore } from '$lib/utils/utils';

	import { currentUser, userFollows, ndk, nsecKey } from '$lib/stores/social-stores';
	import { orientation, currentComponent } from '$lib/stores/stores';

	import SocialNavbar from '$lib/components/navbars/SocialNavbar.svelte';
	import NarrativesFiltersNavbar from '$lib/components/navbars/NarrativesFiltersNavbar.svelte';
	import LoginWindow from '$lib/components/modals/LoginWindow.svelte';

	import Spinner from '$lib/components/icons/Spinner.svelte';

	let isLoading = true;
	const loginMethod = createSessionStore('loginMethod', 'nip07');

	function setThemeFromLocalStorage() {
		const storedTheme = localStorage.getItem('theme');
		if (storedTheme) {
			document.documentElement.setAttribute('data-theme', storedTheme);
		}
	}

	async function connectAndLogin(key, method) {
		try {
			$ndk.connect();
			const user = await login($ndk, key, method);
			if (user) {
				await prepareSession(user);
				if (method === 'nsec') {
					nsecKey.set(key);
				} else if (method === 'nip07') {
					nsecKey.set('nip07_logged_in');
				}
				loginMethod.set(method);
			} else {
				console.error('Failed to log in');
			}
		} catch (error) {
			console.error('Error during login:', error);
		} finally {
			isLoading = false;
		}
	}

	onMount(() => {
		setThemeFromLocalStorage();
		const unsubscribe = nsecKey.subscribe(async (key) => {
			if (key) {
				await connectAndLogin(key, $loginMethod);
			}
		});

		return () => unsubscribe();
	});

	function handleLoginSubmit(event) {
		connectAndLogin(event.detail.key, event.detail.method);
	}

	let isNarrativesDashboard = false;

	$: {
		isNarrativesDashboard = $currentComponent === NarrativesDashboard;
	}
</script>

<div class="main-layout">
	{#if $nsecKey === ''}
		<LoginWindow on:submit={handleLoginSubmit} />
	{/if}

	{#if $orientation === 'portrait'}
		{#if isNarrativesDashboard}
			<div class="top-navbar-container">
				<NarrativesFiltersNavbar />
			</div>
		{/if}

		<div class="main-content-portrait">
			{#if !isLoading}
				<svelte:component this={$currentComponent} />
			{:else}
				<div class="spinner-container">
					<Spinner />
				</div>
			{/if}
		</div>

		<div class="bottom-navbar-container">
			<SocialNavbar />
		</div>
	{:else}
		<div class="left-navbar-container">
			<SocialNavbar />
		</div>

		<div class="main-content-landscape">
			{#if !isLoading}
				<svelte:component this={$currentComponent} />
			{:else}
				<div class="spinner-container">
					<Spinner />
				</div>
			{/if}
		</div>

		{#if isNarrativesDashboard}
		<div class="right-navbar-container">
				<NarrativesFiltersNavbar />
			</div>
		{/if}
	{/if}
</div>

<style lang="postcss">
	.main-layout {
		@apply text-xs xs:text-xs sm:text-sm md:text-md lg:text-lg xl:text-xl;
		background-color: var(--bg-color);
		color: var(--text-color);
		display: flex;
		height: 100vh;
	}

	.main-content-landscape {
		flex-grow: 1;
		overflow-x: hidden;
	}

	.main-content-portrait {
		flex-grow: 1;
		overflow-x: hidden;
		margin-top: 3rem;
		margin-bottom: 3rem; /* Adjust this value to match the height of the bottom navbar */
	}

	.spinner-container {
		display: flex;
		justify-content: center;
		align-items: center;
		position: absolute;
		top: 5%;
		left: 50%;
		height: 3rem;
		width: 3rem;
	}

	.left-navbar-container {
		flex: 0 0 auto;
		border-right: 1px solid var(--separator-line-color);
		overflow: hidden;
	}

	.right-navbar-container {
		flex: 0 0 auto;
		border-left: 1px solid var(--separator-line-color);
		overflow: hidden;
	}

	.bottom-navbar-container {
		z-index: 1000;
		display: flex;
		position: fixed;
		bottom: 0;
		width: 100%;
		border-top: 1px solid var(--separator-line-color);
		overflow: hidden;
	}

	.top-navbar-container {
		z-index: 1000;
		display: flex;
		position: fixed;
		top: 0;
		width: 100%;
		border-bottom: 1px solid var(--separator-line-color);
		overflow: hidden;
	}
</style>
