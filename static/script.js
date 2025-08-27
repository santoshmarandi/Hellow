document.addEventListener('DOMContentLoaded', () => {
    const summarizeBtn = document.getElementById('summarize-btn');
    const copyBtn = document.getElementById('copy-btn');
    const youtubeUrlInput = document.getElementById('youtube-url');
    const customCommandInput = document.getElementById('custom-command');
    const summaryContainer = document.getElementById('summary-container');
    const summaryText = document.getElementById('summary-text');
    const loading = document.getElementById('loading');
    const errorContainer = document.getElementById('error-container');
    const errorMessage = document.getElementById('error-message');

    summarizeBtn.addEventListener('click', async () => {
        const youtubeUrl = youtubeUrlInput.value.trim();
        const customCommand = customCommandInput.value.trim();

        if (!youtubeUrl) {
            alert('Please fill in the YouTube URL field.');
            return;
        }

        // Hide previous results and show loading
        summaryContainer.classList.add('hidden');
        errorContainer.classList.add('hidden');
        loading.classList.remove('hidden');

        try {
            const response = await fetch('/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    youtube_url: youtubeUrl,
                    custom_command: customCommand,
                }),
            });

            const data = await response.json();

            if (response.ok) {
                summaryText.innerText = data.summary;
                summaryContainer.classList.remove('hidden');
            } else {
                errorMessage.innerText = `Error: ${data.error}`;
                errorContainer.classList.remove('hidden');
            }
        } catch (error) {
            errorMessage.innerText = `An unexpected error occurred: ${error.message}`;
            errorContainer.classList.remove('hidden');
        } finally {
            loading.classList.add('hidden');
        }
    });

    copyBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(summaryText.innerText)
            .then(() => {
                alert('Summary copied to clipboard!');
            })
            .catch(err => {
                console.error('Failed to copy text: ', err);
                alert('Failed to copy summary.');
            });
    });
});
