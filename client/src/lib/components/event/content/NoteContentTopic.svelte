<!-- src\lib\components\event\content\NoteContentTopic.svelte -->

<script lang="ts">
	export let value = '';
</script>

<a href="/t/{value}" on:click>#{value}</a>
