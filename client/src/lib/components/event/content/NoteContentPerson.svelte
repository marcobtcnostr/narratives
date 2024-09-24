<!-- src\lib\components\event\content\NoteContentPerson.svelte -->

<script lang="ts">
	import Name from '$lib/components/user/Name.svelte';
	import { createEventDispatcher } from 'svelte';

	export let ndk;
	export let value;
    
	const dispatch = createEventDispatcher();
	function clicked() {
		dispatch('click', { type: 'pubkey', pubkey: value.pubkey });
	}
</script>

<button on:click={clicked}>
	@<Name {ndk} npubMaxLength={12} pubkey={value.pubkey} attribute="name" />
</button>
