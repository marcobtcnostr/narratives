<!-- src\lib\components\user\Name.svelte -->

<script lang="ts">
	import { truncatedBech32 } from "$lib/utils/utils";

	export function prettifyNip05(nip05, maxLength) {
		const trimmedNip05 = nip05.startsWith('_@') ? nip05.substring(2) : nip05;
		if (maxLength) {
			return trimmedNip05.slice(0, maxLength);
		} else {
			return trimmedNip05;
		}
	}

	export let ndk: any;
	export let npub = undefined;
	export let pubkey = undefined;
	export let user = undefined;
	export let userProfile = undefined;
	export let npubMaxLength = undefined;
	/**
	 * Optionally specify the attribute to use for the name
	 * @default 'display_name'
	 */
	export let attribute = 'display_name';
	if (!userProfile && !user && ndk) {
		let opts = npub ? { npub } : { pubkey };
		try {
			user = ndk?.getUser(opts);
			npub = user.npub;
		} catch (e) {
			console.error(`error trying to get user`, { opts }, e);
		}
	}
	const _npub = npub || user?.npub;
	const truncatedNpub = (npubMaxLength && _npub) ? truncatedBech32(_npub, npubMaxLength) : _npub;
	function chooseNameFromDisplay(profile) {
		if (profile && profile[attribute]) return profile[attribute];
		return (
			profile?.displayName ||
			profile?.name ||
			(profile?.nip05 && prettifyNip05(profile.nip05, undefined)) ||
			truncatedNpub
		);
	}
</script>

<span class="name {$$props.class}" style={$$props.style}>
	{#if userProfile}
		{chooseNameFromDisplay(userProfile)}
	{:else if user}
		{#await user.fetchProfile({ closeOnEose: true, groupable: true, groupableDelay: 200 })}
			{chooseNameFromDisplay()}
		{:then}
			{chooseNameFromDisplay(user.profile)}
		{:catch error}
			<span class="name--error {$$props.class}" data-error={error} title={_npub}>
				{truncatedNpub}
			</span>
		{/await}
	{/if}
</span>
