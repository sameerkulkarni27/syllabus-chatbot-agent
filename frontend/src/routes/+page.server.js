import { API_KEY, API_URL } from '$env/static/private';
import { client } from '$lib/client/client.gen';
import { uploadSyllabusUploadPost, askQuestionAskPost } from '$lib/client';

client.setConfig({ baseUrl: API_URL || 'http://localhost:8000' });

export const actions = {
    upload: async ({ request }) => {
        const data = await request.formData();
        const file = data.get('file');
        const namespace = data.get('namespace');

        const formData = new FormData();
        formData.append('file', file, file.name);

        const result = await fetch(
            `${API_URL || 'http://localhost:8000'}/upload?namespace=${namespace.trim()}`,
            {
                method: 'POST',
                headers: { 'api-key': API_KEY },
                body: formData
            }
        );

        const json = await result.json();

        if (!result.ok) {
            console.log("body:", json);
            return { uploadSuccess: false, error: json.detail ?? result.statusText };
        }

        return { uploadSuccess: true, data: json };
    },

    ask: async ({ request }) => {
        const data = await request.formData();
        const namespace = data.get('namespace');
        const query = data.get('query');

        const result = await fetch(
            `${API_URL || 'http://localhost:8000'}/ask`,
            {
                method: 'POST',
                headers: {
                    'api-key': API_KEY,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ namespace, query })
            }
        );

        const json = await result.json();

        if (!result.ok) {
            console.log("Ask error:", json);
            return { askSuccess: false, error: json.detail ?? result.statusText };
        }

        return { askSuccess: true, data: json };
    }
};