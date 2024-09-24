<!-- src\lib\components\navbars\NarrativesFiltersNavbar.svelte -->
<script lang="ts">
	import { page } from '$app/stores';
	import { orientation, currentComponent } from '$lib/stores/stores';
	import Home from '$lib/components/pages/Home.svelte';
	import Settings from '$lib/components/pages/Settings.svelte';
	import BootstrapFillIcon from '$lib/components/icons/BootstrapFillIcon.svelte';
	import HomeIcon from '$lib/components/icons/HomeIcon.svelte';
	import SearchIcon from '$lib/components/icons/SearchIcon.svelte';
	import EnvelopeIcon from '$lib/components/icons/EnvelopeIcon.svelte';
	import BellIcon from '$lib/components/icons/BellIcon.svelte';
	import SettingsIcon from '$lib/components/icons/GearWideIcon.svelte';
	import ProfileIcon from '$lib/components/icons/ProfileIcon.svelte';
	import InfoIcon from '$lib/components/icons/InfoIcon.svelte';

	import ProjectsIcon from '$lib/components/icons/FolderOpenIcon.svelte';
	import DatabaseIcon from '$lib/components/icons/DatabaseIcon.svelte';
	import DatabaseAddIcon from '$lib/components/icons/DatabaseAddIcon.svelte';
	import TableIcon from '$lib/components/icons/TableIcon.svelte';
	import ArrowClockwise from '$lib/components/icons/ArrowClockwise.svelte';
	import FunnelIcon from '$lib/components/icons/FunnelIcon.svelte';
	import AlarmIcon from '$lib/components/icons/AlarmIcon.svelte';
	import ShareIcon from '$lib/components/icons/ShareIcon.svelte';

	import { updateNarrativesDatabase } from '$lib/api/narratives-api';

	import {
		isNarrativesFilterWindowOpen,
		isNarrativesDatabaseWindowOpen,
		isNarrativesDatabaseAddWindowOpen,
		isShareNarrativesPostWindowOpen,
		isUpdatingDatabase
	} from '$lib/stores/narratives-stores';

	let currentPath = '';
	$: currentPath = $page.url.pathname;

	function navigate(component) {
		currentComponent.set(component);
	}

	async function handleUpdateClick() {
		isUpdatingDatabase.set(true); // Show the pop-up
		try {
			await updateNarrativesDatabase();
		} catch (error) {
			isUpdatingDatabase.set(false);
			console.error('An error occurred:', error);
		} finally {
			isUpdatingDatabase.set(false); // Ensure the pop-up is hidden after the operation
		}
	}
	$: IsUpdatingDatabase = $isUpdatingDatabase;

	function toggleFilterWindow() {
		isNarrativesFilterWindowOpen.update((n) => !n);
	}
	$: IsNarrativesFilterWindowOpen = $isNarrativesFilterWindowOpen;

	function toggleDatabaseWindow() {
		isNarrativesDatabaseWindowOpen.update((n) => !n);
	}
	$: IsNarrativesDatabaseWindowOpen = $isNarrativesDatabaseWindowOpen;

	function toggleDatabaseAddWindow() {
		isNarrativesDatabaseAddWindowOpen.update((n) => !n);
	}
	$: IsNarrativesDatabaseAddWindowOpen = $isNarrativesDatabaseAddWindowOpen;

	function toggleSharePostWindow() {
		isShareNarrativesPostWindowOpen.update((n) => !n);
	}
	$: IsShareNarrativesPostWindowOpen = $isShareNarrativesPostWindowOpen;
</script>

<div class="social-navbar" class:landscape={$orientation === 'landscape'} class:portrait={$orientation === 'portrait'}>
	<button class="icon" on:click={toggleDatabaseAddWindow} aria-label="Home">
		<DatabaseAddIcon />
	</button>
	<button class="icon" on:click={handleUpdateClick} aria-label="Search">
		<ArrowClockwise />
	</button>
	<button class="icon" on:click={toggleFilterWindow} aria-label="Messages">
		<FunnelIcon />
	</button>
	<button class="icon" on:click={toggleDatabaseWindow} aria-label="Notifications">
		<TableIcon />
	</button>
	<button class="icon" on:click={() => navigate(Settings)} aria-label="Settings">
		<ProjectsIcon />
	</button>
	<button class="icon" on:click={() => navigate(Settings)} aria-label="Settings">
		<BellIcon />
	</button>
	<button class="icon" on:click={() => navigate(Settings)} aria-label="Settings">
		<AlarmIcon />
	</button>
	<button class="icon" on:click={toggleSharePostWindow} aria-label="Settings">
		<ShareIcon />
	</button>

	<div class="flex-grow"></div>

	<button class="icon" on:click={navigate} aria-label="About">
		<InfoIcon />
	</button>
	<button class="icon" on:click={navigate} aria-label="Settings">
		<SettingsIcon />
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
