<!-- src\lib\components\navbars\SocialNavbar.svelte -->
<script lang="ts">
	import { page } from '$app/stores';
	import { orientation, currentComponent } from '$lib/stores/stores';
	import Home from '$lib/components/pages/Home.svelte';
	import NarrativesDashboard from '$lib/components/pages/NarrativesDashboard.svelte';
	import NarrativesLogo from '$lib/components/icons/NarrativesLogo.svelte';
	import Settings from '$lib/components/pages/Settings.svelte';
	import BootstrapFillIcon from '$lib/components/icons/BootstrapFillIcon.svelte';
	import HomeIcon from '$lib/components/icons/HomeIcon.svelte';
	import SearchIcon from '$lib/components/icons/SearchIcon.svelte';
	import EnvelopeIcon from '$lib/components/icons/EnvelopeIcon.svelte';
	import BellIcon from '$lib/components/icons/BellIcon.svelte';
	import SettingsIcon from '$lib/components/icons/GearWideIcon.svelte';
	import ProfileIcon from '$lib/components/icons/ProfileIcon.svelte';
	import InfoIcon from '$lib/components/icons/InfoIcon.svelte';

	let currentPath = '';
	$: currentPath = $page.url.pathname;

	function navigate(component) {
		currentComponent.set(component);
	}
</script>

<div class="social-navbar" class:landscape={$orientation === 'landscape'} class:portrait={$orientation === 'portrait'}>
	<button class="icon" on:click={() => navigate(NarrativesDashboard)} aria-label="Home">
		<NarrativesLogo />
	</button>
	<button class="icon" on:click={() => navigate(Home)} aria-label="Home">
		<HomeIcon />
	</button>
	<button class="icon" on:click={navigate} aria-label="Search">
		<SearchIcon />
	</button>
	<button class="icon" on:click={navigate} aria-label="Messages">
		<EnvelopeIcon />
	</button>
	<button class="icon" on:click={navigate} aria-label="Notifications">
		<BellIcon />
	</button>
	<button class="icon" on:click={() => navigate(Settings)} aria-label="Settings">
		<SettingsIcon />
	</button>

	<div class="flex-grow"></div>

	<button class="icon" on:click={navigate} aria-label="About">
		<InfoIcon />
	</button>
	<button class="icon" on:click={navigate} aria-label="Profile">
		<ProfileIcon />
	</button>
</div>

<style>
	.social-navbar {
		background: var(--navbar-bg-color);
	}

	.social-navbar.landscape {
		@apply flex flex-col items-center justify-start h-full w-10 p-2 xs:w-10 sm:w-10 md:w-10 lg:w-16;
	}

	.social-navbar.portrait {
		@apply flex flex-row items-center justify-start w-full h-10 p-2 xs:h-10 sm:h-12 md:h-12 lg:w-16;
	}

	.icon {
		@apply cursor-pointer flex justify-center items-center transition-colors duration-300;
		color: var(--text-color);
		background: none;
		border: none;
		padding: 0.25rem;
	}

	.icon:hover {
		background: var(--navbar-bg-color-hover);
		color: var(--navbar-text-color-hover);
		border-radius: 0.3rem;
		/* box-shadow: 0 0 0 0.125rem var(--logo-color); */
	}

	.social-navbar.landscape .icon {
		@apply w-10 p-2 xs:w-10 sm:w-10 md:w-10 lg:w-16;
	}

	.social-navbar.portrait .icon {
		@apply h-10 p-2 xs:h-10 sm:h-12 md:h-12 lg:w-16;
		min-height: 2.5rem;
		min-width: 2.5rem;
	}
</style>
