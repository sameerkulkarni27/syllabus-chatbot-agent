<script>
    import { enhance } from '$app/forms';

    // result from +page.server.js
    let { form } = $props();

    let uploading = $state(false);
    let asking = $state(false);
</script>

<h1>Syllabus Chatbot API Test</h1>

<section>
    <h2>POST /upload</h2>
    <p>Upload a PDF syllabus.</p>
    
    <form 
        method="POST" 
        action="?/upload" 
        use:enhance={() => {
            uploading = true;
            return async ({ update }) => {
                await update();
                uploading = false;
            };
        }}
        enctype="multipart/form-data"
    >
        <label>
            Namespace:<br />
            <input type="text" name="namespace" placeholder="e.g. cs200-f24" required />
        </label>
        <br />
        <label>
            PDF File:<br />
            <input type="file" name="file" accept=".pdf" required />
        </label>
        <br />
        <button type="submit" disabled={uploading}>
            {uploading ? 'Uploading...' : 'Send'}
        </button>
    </form>

    {#if form?.uploadSuccess}
        <pre>{JSON.stringify(form.data, null, 2)}</pre>
    {:else if form?.uploadSuccess === false}
        <p style="color:red">Error: {form.error}</p>
    {/if}
</section>

<hr />

<section>
    <h2>POST /ask</h2>
    <p>Ask a question.</p>

    <form 
        method="POST" 
        action="?/ask" 
        use:enhance={() => {
            asking = true;
            return async ({ update }) => {
                await update();
                asking = false;
            };
        }}
    >
        <label>
            Namespace:<br />
            <input type="text" name="namespace" placeholder="cs200-f24" required />
        </label>
        <br />
        <label>
            Question:<br />
            <textarea name="query" required></textarea>
        </label>
        <br />
        <button type="submit" disabled={asking}>
            {asking ? 'Searching...' : 'Send'}
        </button>
    </form>

    {#if form?.askSuccess}
        <pre>{JSON.stringify(form.data, null, 2)}</pre>
    {:else if form?.askSuccess === false}
        <p style="color:red">Error: {form.error}</p>
    {/if}
</section>