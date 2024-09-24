<!-- src\lib\components\event\content\EventContent.svelte -->

<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import Kind1 from '$lib/components/event/content/Kind1.svelte';
	import Kind9999 from '$lib/components/event/content/Kind9999.svelte';

	export let ndk;
	export let event;

	export let anchorId = null;
	export let maxLength = 700;
	export let showEntire = true;
	export let showMedia = true;
	export let mediaCollectionComponent = undefined;
	export let eventCardComponent = undefined;

	export let content = event?.content;
</script>

{#if event}
	{#if event.kind === 1}
		<Kind1
			{ndk}
			{content}
			{event}
			{anchorId}
			{maxLength}
			{showEntire}
			{showMedia}
			on:click
			class={$$props.class}
			{mediaCollectionComponent}
			{eventCardComponent}
		/>
	{:else if event.kind === 9999}
		<Kind9999
			{ndk}
			{content}
			{event}
			{anchorId}
			{maxLength}
			{showEntire}
			{showMedia}
			on:click
			class={$$props.class}
			{mediaCollectionComponent}
			{eventCardComponent}
		/>
	{/if}
{/if}
